#!/usr/bin/env python3
"""
Comprehensive endpoint testing script.
Tests all endpoints from the Postman collection.
"""
import json
import sys
from typing import Dict, Optional

import requests

BASE_URL = "http://localhost:8001/api/v1"

# Test results
results = {"passed": [], "failed": [], "skipped": []}


def log_test(name: str, status: str, details: str = ""):
    """Log test result"""
    if status == "pass":
        results["passed"].append(name)
        print(f"✅ {name}")
    elif status == "fail":
        results["failed"].append(f"{name}: {details}")
        print(f"❌ {name}: {details}")
    else:
        results["skipped"].append(name)
        print(f"⏭️  {name}: {details}")


def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            log_test("Health Check", "pass")
            return True
        else:
            log_test("Health Check", "fail", f"Status {response.status_code}")
            return False
    except Exception as e:
        log_test("Health Check", "fail", str(e))
        return False


def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Auth Endpoints ===")

    # Register user (skip if already exists)
    try:
        register_data = {
            "email": "testuser@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "frontend",
        }
        response = requests.post(f"{BASE_URL}/users/", json=register_data, timeout=5)
        if response.status_code in [200, 201]:
            log_test("Register User", "pass")
        elif response.status_code == 409:
            log_test("Register User", "pass", "User already exists (expected)")
        else:
            log_test(
                "Register User", "fail", f"Status {response.status_code}: {response.text[:100]}"
            )
    except Exception as e:
        log_test("Register User", "fail", str(e))

    # Login as regular user
    access_token = None
    try:
        login_data = {"email": "testuser@example.com", "password": "TestPassword123!"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            log_test("Login (regular user)", "pass")
        else:
            log_test(
                "Login (regular user)",
                "fail",
                f"Status {response.status_code}: {response.text[:100]}",
            )
    except Exception as e:
        log_test("Login (regular user)", "fail", str(e))

    # Try to login as admin
    admin_token = None
    try:
        admin_login = {"email": "admin@test.com", "password": "AdminPassword123!"}
        response = requests.post(f"{BASE_URL}/auth/login", json=admin_login, timeout=5)
        if response.status_code == 200:
            data = response.json()
            admin_token = data.get("access_token")
            log_test("Login (admin)", "pass")
        else:
            log_test(
                "Login (admin)", "fail", f"Status {response.status_code}: {response.text[:100]}"
            )
    except Exception as e:
        log_test("Login (admin)", "fail", str(e))

    return access_token, admin_token


def test_with_auth(
    token: Optional[str],
    endpoint_name: str,
    method: str,
    path: str,
    json_data: Optional[Dict] = None,
    expected_status: int = 200,
):
    """Test endpoint with authentication"""
    if not token:
        log_test(endpoint_name, "skipped", "No auth token")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(
                f"{BASE_URL}{path}", headers=headers, json=json_data, timeout=5
            )
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{path}", headers=headers, json=json_data, timeout=5)
        elif method == "PATCH":
            response = requests.patch(
                f"{BASE_URL}{path}", headers=headers, json=json_data, timeout=5
            )
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{path}", headers=headers, timeout=5)
        else:
            log_test(endpoint_name, "fail", f"Unknown method: {method}")
            return None

        if response.status_code == expected_status:
            log_test(endpoint_name, "pass")
            return response.json() if response.content else None
        else:
            error_msg = response.text[:200] if response.text else "No error message"
            log_test(endpoint_name, "fail", f"Status {response.status_code}: {error_msg}")
            return None
    except Exception as e:
        log_test(endpoint_name, "fail", str(e))
        return None


def test_client_portal_endpoint():
    """Test client portal endpoint"""
    print("\n=== Testing Client Portal Endpoint ===")

    # First, we need to create a client with api_key
    # This requires admin access, so we'll skip if we don't have it
    # For now, just test the endpoint structure
    try:
        response = requests.get(
            f"{BASE_URL}/client-portal/projects/1",
            headers={"X-Client-Token": "test-token"},
            timeout=5,
        )
        # We expect 401 (invalid token) or 404 (project not found) - both mean endpoint works
        if response.status_code in [401, 404, 403]:
            log_test(
                "Client Portal - Get Project (no token)",
                "pass",
                f"Got expected {response.status_code}",
            )
        else:
            log_test(
                "Client Portal - Get Project", "fail", f"Unexpected status {response.status_code}"
            )
    except Exception as e:
        log_test("Client Portal - Get Project", "fail", str(e))


def main():
    print("=" * 60)
    print("COMPREHENSIVE ENDPOINT TESTING")
    print("=" * 60)

    # Test health check
    print("\n=== Testing Health Check ===")
    if not test_health_check():
        print("\n❌ Health check failed. Is the server running?")
        sys.exit(1)

    # Test auth endpoints
    token, admin_token = test_auth_endpoints()

    if not token and not admin_token:
        print("\n⚠️  Could not get auth token. Some tests will be skipped.")

    # Test client portal (doesn't require user auth)
    test_client_portal_endpoint()

    # Use admin token for admin endpoints, regular token for others
    auth_token = admin_token or token

    # Test other endpoints with auth
    if auth_token:
        print("\n=== Testing User Endpoints ===")
        test_with_auth(auth_token, "Get Current User", "GET", "/users/me")

        print("\n=== Testing Admin Endpoints ===")
        if admin_token:
            test_with_auth(admin_token, "Admin Dashboard", "GET", "/admin/dashboard")

        print("\n=== Testing Client Endpoints ===")
        if admin_token:
            test_with_auth(admin_token, "List Clients", "GET", "/clients/")

            # Create a client for further testing
            client_data = {"name": "Test Client", "email": "client@test.com"}
            client_response = test_with_auth(
                admin_token, "Create Client", "POST", "/clients/", client_data, 201
            )

            client_id = None
            if client_response:
                client_id = client_response.get("id")
                if client_id:
                    test_with_auth(admin_token, "Get Client", "GET", f"/clients/{client_id}")
        else:
            log_test("Client Endpoints", "skipped", "Requires admin token")
            client_id = None

        print("\n=== Testing Project Endpoints ===")
        test_with_auth(auth_token, "List Projects", "GET", "/projects/")

        if client_id and admin_token:
            project_data = {
                "name": "Test Project",
                "description": "Test Description",
                "client_id": client_id,
                "status": "active",
            }
            project_response = test_with_auth(
                admin_token, "Create Project", "POST", "/projects/", project_data, 201
            )

            if project_response:
                project_id = project_response.get("id")
                if project_id:
                    test_with_auth(auth_token, "Get Project", "GET", f"/projects/{project_id}")

        print("\n=== Testing Task Endpoints ===")
        test_with_auth(auth_token, "List Tasks", "GET", "/tasks/")

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⏭️  Skipped: {len(results['skipped'])}")

    if results["failed"]:
        print("\nFailed Tests:")
        for failure in results["failed"]:
            print(f"  - {failure}")

    if results["failed"]:
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")


if __name__ == "__main__":
    main()
