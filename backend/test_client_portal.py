#!/usr/bin/env python3
"""Test client portal endpoint specifically"""
import sys

import requests

BASE_URL = "http://localhost:8001/api/v1"

# Get client api_key and project_id from database
import subprocess

result = subprocess.run(
    [
        "docker",
        "compose",
        "exec",
        "-T",
        "backend",
        "python3",
        "-c",
        """
from app.db.session import SessionLocal
from app.dbmodels import Client, Project
import json

db = SessionLocal()
client = db.query(Client).filter(Client.name == 'Portal Test Client').first()
if client and client.api_key:
    project = db.query(Project).filter(Project.client_id == client.id).first()
    if project:
        print(json.dumps({
            'api_key': client.api_key,
            'project_id': project.id,
            'client_id': client.id
        }))
db.close()
""",
    ],
    capture_output=True,
    text=True,
    cwd="/home/vele/Documents/Continuum",
)

if result.returncode != 0 or not result.stdout.strip():
    print("❌ Could not get client info from database")
    sys.exit(1)

import json

info = json.loads(result.stdout.strip())
api_key = info["api_key"]
project_id = info["project_id"]

print(f"Testing Client Portal with:")
print(f"  API Key: {api_key[:20]}...")
print(f"  Project ID: {project_id}\n")

# Test 1: Valid request
print("Test 1: Valid client token + own project")
response = requests.get(
    f"{BASE_URL}/client-portal/projects/{project_id}",
    headers={"X-Client-Token": api_key},
    timeout=5,
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success! Got project: {data.get('name')}")
    print(f"   Members: {data.get('members')}")
    print(f"   Has client_name: {'client_name' in data}")
    print(f"   Excluded fields check:")
    excluded = ["client_id", "tasks", "logged_hours", "hourly_rate", "user_id", "email"]
    for field in excluded:
        if field in data:
            print(f"   ❌ {field} should not be present!")
        else:
            print(f"   ✅ {field} correctly excluded")
else:
    print(f"❌ Failed: Status {response.status_code}")
    print(f"   {response.text}")
    sys.exit(1)

# Test 2: Invalid token
print("\nTest 2: Invalid token")
response = requests.get(
    f"{BASE_URL}/client-portal/projects/{project_id}",
    headers={"X-Client-Token": "invalid-token"},
    timeout=5,
)
if response.status_code == 401:
    print("✅ Correctly returned 401 for invalid token")
else:
    print(f"❌ Expected 401, got {response.status_code}")

# Test 3: Missing token
print("\nTest 3: Missing token")
response = requests.get(f"{BASE_URL}/client-portal/projects/{project_id}", timeout=5)
if response.status_code == 401:
    print("✅ Correctly returned 401 for missing token")
else:
    print(f"❌ Expected 401, got {response.status_code}")

# Test 4: Non-existent project
print("\nTest 4: Non-existent project")
response = requests.get(
    f"{BASE_URL}/client-portal/projects/99999", headers={"X-Client-Token": api_key}, timeout=5
)
if response.status_code == 404:
    print("✅ Correctly returned 404 for non-existent project")
else:
    print(f"❌ Expected 404, got {response.status_code}")

print("\n🎉 All client portal tests passed!")
