#!/usr/bin/env python3
"""
Test script to call initialize endpoint
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_initialize():
    """Test initialize endpoint"""
    print("\n=== Testing Initialize Endpoint ===")
    print("Starting initialization (this may take 2-5 minutes)...")
    response = requests.post(f"{BASE_URL}/initialize", timeout=600)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    try:
        if test_health():
            print("\n✓ Health check passed!")
            if test_initialize():
                print("\n✓ Initialization successful!")
            else:
                print("\n✗ Initialization failed")
        else:
            print("\n✗ Health check failed")
    except Exception as e:
        print(f"\n✗ Error: {e}")
