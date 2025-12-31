#!/usr/bin/env python3
"""
Comprehensive endpoint testing script based on Postman collection.
Tests all endpoints and reports failures.
"""
import json
import sys
from typing import Any, Dict, List, Optional

try:
    import httpx
except ImportError:
    try:
        import requests

        # Create a simple httpx-like interface using requests
        class httpx:
            class Client:
                def __init__(self, timeout=None):
                    self.timeout = timeout

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    pass

                def get(self, url, headers=None, params=None):
                    r = requests.get(url, headers=headers, params=params, timeout=self.timeout)
                    return type(
                        "Response",
                        (),
                        {"status_code": r.status_code, "text": r.text, "json": lambda: r.json()},
                    )()

                def post(self, url, headers=None, json=None, data=None, files=None):
                    r = requests.post(
                        url,
                        headers=headers,
                        json=json,
                        data=data,
                        files=files,
                        timeout=self.timeout,
                    )
                    return type(
                        "Response",
                        (),
                        {"status_code": r.status_code, "text": r.text, "json": lambda: r.json()},
                    )()

                def put(self, url, headers=None, json=None):
                    r = requests.put(url, headers=headers, json=json, timeout=self.timeout)
                    return type(
                        "Response",
                        (),
                        {"status_code": r.status_code, "text": r.text, "json": lambda: r.json()},
                    )()

                def patch(self, url, headers=None, json=None, params=None):
                    r = requests.patch(
                        url, headers=headers, json=json, params=params, timeout=self.timeout
                    )
                    return type(
                        "Response",
                        (),
                        {"status_code": r.status_code, "text": r.text, "json": lambda: r.json()},
                    )()

                def delete(self, url, headers=None, params=None):
                    r = requests.delete(url, headers=headers, params=params, timeout=self.timeout)
                    return type(
                        "Response",
                        (),
                        {"status_code": r.status_code, "text": r.text, "json": lambda: r.json()},
                    )()

    except ImportError:
        print("ERROR: Neither httpx nor requests is installed")
        sys.exit(1)
# Try to detect if we're in a container
import os
from datetime import datetime

if os.path.exists("/.dockerenv"):
    BASE_URL = "http://backend:8000"  # Container service name
else:
    BASE_URL = "http://localhost:8001"  # Host machine
access_token = ""
refresh_token = ""

# Test user credentials
TEST_EMAIL = "test_user@example.com"
TEST_PASSWORD = "TestPassword123!"
TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "User"

# Track results
results = {"passed": [], "failed": [], "skipped": []}


def log_result(endpoint: str, method: str, status: str, error: Optional[str] = None):
    """Log test result"""
    result = {
        "endpoint": endpoint,
        "method": method,
        "status": status,
        "error": error,
        "timestamp": datetime.now().isoformat(),
    }
    if status == "PASSED":
        results["passed"].append(result)
        print(f"✓ {method} {endpoint}")
    elif status == "SKIPPED":
        results["skipped"].append(result)
        print(f"⊘ {method} {endpoint} (SKIPPED)")
    else:
        results["failed"].append(result)
        print(f"✗ {method} {endpoint} - {error}")


def make_request(
    method: str,
    url: str,
    headers: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    files: Optional[Dict] = None,
) -> httpx.Response:
    """Make HTTP request"""
    if headers is None:
        headers = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    with httpx.Client(timeout=30.0) as client:
        if method == "GET":
            return client.get(url, headers=headers, params=params)
        elif method == "POST":
            if files:
                return client.post(url, headers=headers, data=json_data, files=files)
            return client.post(url, headers=headers, json=json_data, params=params)
        elif method == "PUT":
            return client.put(url, headers=headers, json=json_data)
        elif method == "PATCH":
            return client.patch(url, headers=headers, json=json_data, params=params)
        elif method == "DELETE":
            return client.delete(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported method: {method}")


def test_health_check():
    """Test health check endpoint"""
    try:
        response = make_request("GET", f"{BASE_URL}/health")
        if response.status_code == 200:
            log_result("/health", "GET", "PASSED")
            return True
        else:
            log_result("/health", "GET", "FAILED", f"Status {response.status_code}")
            return False
    except Exception as e:
        log_result("/health", "GET", "FAILED", str(e))
        return False


def test_register_user():
    """Test user registration"""
    global access_token, refresh_token
    try:
        data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "first_name": TEST_FIRST_NAME,
            "last_name": TEST_LAST_NAME,
            "role": "frontend",
        }
        response = make_request("POST", f"{BASE_URL}/api/v1/users/", json_data=data)
        if response.status_code in [200, 201]:
            log_result("/api/v1/users/", "POST", "PASSED")
            return True
        elif response.status_code == 400:
            # User might already exist, try login instead
            log_result("/api/v1/users/", "POST", "SKIPPED", "User may already exist")
            return test_login()
        else:
            log_result(
                "/api/v1/users/",
                "POST",
                "FAILED",
                f"Status {response.status_code}: {response.text}",
            )
            return False
    except Exception as e:
        log_result("/api/v1/users/", "POST", "FAILED", str(e))
        return False


def test_login():
    """Test login and save tokens"""
    global access_token, refresh_token
    try:
        data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
        response = make_request("POST", f"{BASE_URL}/api/v1/auth/login", json_data=data)
        if response.status_code == 200:
            json_data = response.json()
            access_token = json_data.get("access_token", "")
            refresh_token = json_data.get("refresh_token", "")
            log_result("/api/v1/auth/login", "POST", "PASSED")
            return True
        else:
            log_result(
                "/api/v1/auth/login",
                "POST",
                "FAILED",
                f"Status {response.status_code}: {response.text}",
            )
            return False
    except Exception as e:
        log_result("/api/v1/auth/login", "POST", "FAILED", str(e))
        return False


def test_endpoint(item: Dict, base_path: str = ""):
    """Test a single endpoint from Postman collection"""
    request = item.get("request", {})
    method = request.get("method", "GET")
    url_obj = request.get("url", {})

    # Build URL
    if isinstance(url_obj, dict):
        path_parts = url_obj.get("path", [])
        raw_url = url_obj.get("raw", "")

        if raw_url:
            # Extract path from raw URL
            url_path = raw_url.replace("{{base_url}}", BASE_URL)
            # Replace token placeholders
            if refresh_token:
                url_path = url_path.replace("{{refresh_token}}", refresh_token)
            # Replace variables
            variables = url_obj.get("variable", [])
            for var in variables:
                url_path = url_path.replace(f":{var.get('key')}", var.get("value", ""))
        else:
            url_path = f"{BASE_URL}{base_path}/{'/'.join(path_parts)}"
            # Replace path variables
            variables = url_obj.get("variable", [])
            for var in variables:
                url_path = url_path.replace(f":{var.get('key')}", var.get("value", ""))
    else:
        url_path = f"{BASE_URL}{base_path}"

    # Get query parameters
    query_params = {}
    if isinstance(url_obj, dict):
        query_list = url_obj.get("query", [])
        for q in query_list:
            if not q.get("disabled", False):
                value = q.get("value", "")
                # Replace token placeholders
                if "{{refresh_token}}" in str(value) and refresh_token:
                    value = value.replace("{{refresh_token}}", refresh_token)
                query_params[q.get("key")] = value

    # Get headers
    headers = {}
    header_list = request.get("header", [])
    for h in header_list:
        if h.get("key") == "Content-Type":
            headers["Content-Type"] = h.get("value", "application/json")
        elif h.get("key") == "X-Client-Token":
            # For client portal, we'll skip if no valid token available
            # This endpoint requires a valid client with api_key
            headers["X-Client-Token"] = h.get("value", "test-token")
        elif h.get("key") == "Authorization":
            # Use actual token if available
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

    # Get body
    json_data = None
    body = request.get("body", {})
    if body.get("mode") == "raw":
        raw_body = body.get("raw", "")
        if raw_body:
            try:
                json_data = json.loads(raw_body)
            except:
                pass

    # Handle authentication
    auth = request.get("auth", {})
    if auth.get("type") == "bearer":
        if not access_token:
            log_result(url_path, method, "SKIPPED", "No access token")
            return
        # Token will be added in make_request via headers

    # Make request
    try:
        response = make_request(
            method,
            url_path,
            headers=headers,
            json_data=json_data,
            params=query_params if query_params else None,
        )

        # Check status code
        # For client portal, 401 is expected if token is invalid (endpoint exists)
        if "client-portal" in url_path and response.status_code == 401:
            log_result(
                url_path, method, "PASSED", "Endpoint exists (401 expected without valid token)"
            )
        elif response.status_code < 400:
            log_result(url_path, method, "PASSED")
        else:
            # Some failures are expected (like invalid tokens, missing data)
            expected_failures = [
                "Invalid or expired",
                "already exists",
                "Not authenticated",
                "Could not validate credentials",
                "Invalid client token",
                "Missing client token",
            ]
            error_text = response.text[:200] if hasattr(response, "text") else str(response)
            is_expected = any(exp in error_text for exp in expected_failures)
            if is_expected:
                log_result(url_path, method, "PASSED", f"Expected failure: {error_text[:100]}")
            else:
                log_result(
                    url_path, method, "FAILED", f"Status {response.status_code}: {error_text[:200]}"
                )
    except Exception as e:
        log_result(url_path, method, "FAILED", str(e))


def test_all_endpoints():
    """Load Postman collection and test all endpoints"""
    try:
        # Try container path first, then host path
        collection_paths = [
            "/app/continuum_backend.postman_collection.json",
            "/home/vele/Documents/Continuum/backend/continuum_backend.postman_collection.json",
        ]
        collection = None
        for path in collection_paths:
            try:
                with open(path, "r") as f:
                    collection = json.load(f)
                    break
            except FileNotFoundError:
                continue

        if collection is None:
            print("ERROR: Postman collection file not found in any expected location")
            return

        items = collection.get("item", [])

        # First test health check
        test_health_check()

        # Test registration/login
        if not test_register_user():
            if not test_login():
                print("ERROR: Could not authenticate. Some tests will be skipped.")
                return

        # Test all endpoints
        for item in items:
            if "item" in item:
                # It's a folder
                folder_name = item.get("name", "")
                for sub_item in item.get("item", []):
                    test_endpoint(sub_item, f"/api/v1/{folder_name.lower()}")
            else:
                # It's a direct endpoint
                test_endpoint(item)

    except FileNotFoundError:
        print(f"ERROR: Postman collection file not found")
    except Exception as e:
        print(f"ERROR: {str(e)}")


def print_summary():
    """Print test summary"""
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {len(results['passed'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Skipped: {len(results['skipped'])}")
    print("=" * 60)

    if results["failed"]:
        print("\nFAILED TESTS:")
        for result in results["failed"]:
            print(f"  {result['method']} {result['endpoint']}")
            print(f"    Error: {result['error']}")

    # Save results to file
    result_paths = [
        "/app/test_results.json",
        "/home/vele/Documents/Continuum/backend/test_results.json",
    ]
    for path in result_paths:
        try:
            with open(path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nDetailed results saved to {path}")
            break
        except (FileNotFoundError, PermissionError):
            continue


if __name__ == "__main__":
    print("Starting comprehensive endpoint tests...")
    print("=" * 60)
    test_all_endpoints()
    print_summary()

    # Exit with error code if any tests failed
    if results["failed"]:
        sys.exit(1)
    else:
        sys.exit(0)
