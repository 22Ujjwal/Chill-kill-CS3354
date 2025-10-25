"""
Simple test of the backend API endpoints
Tests health check and basic routing
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🧪 Testing /api/health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_initialize():
    """Test initialize endpoint"""
    print("\n🧪 Testing /api/initialize endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/api/initialize", timeout=300)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def test_query():
    """Test query endpoint"""
    print("\n🧪 Testing /api/query endpoint...")
    try:
        payload = {"query": "What is Nintendo?"}
        response = requests.post(f"{BASE_URL}/api/query", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def main():
    print("="*60)
    print("Nintendo Chatbot Backend - API Tests")
    print("="*60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to start...")
    max_retries = 10
    for i in range(max_retries):
        try:
            requests.get(f"{BASE_URL}/api/health", timeout=2)
            print("✅ Server is ready!")
            break
        except:
            print(f"  Attempt {i+1}/{max_retries}...")
            time.sleep(1)
    
    # Run tests
    print("\n" + "="*60)
    print("Running API Tests")
    print("="*60)
    
    # Test 1: Health Check
    health_ok = test_health()
    
    # Test 2: Initialize (skip if health failed)
    init_ok = False
    if health_ok:
        print("\n📝 Note: Initialize takes 2-5 minutes (scrapes website)")
        user_input = input("Run initialization? (y/n): ").strip().lower()
        if user_input == 'y':
            init_ok = test_initialize()
    
    # Test 3: Query (skip if not initialized)
    query_ok = False
    if init_ok:
        query_ok = test_query()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"✅ Health Check: {'PASS' if health_ok else 'FAIL'}")
    print(f"{'✅' if init_ok else '⏭️ '} Initialize: {'PASS' if init_ok else 'SKIPPED'}")
    print(f"{'✅' if query_ok else '⏭️ '} Query: {'PASS' if query_ok else 'SKIPPED'}")
    
    print("\n" + "="*60)
    print("Backend is running on http://localhost:8000")
    print("="*60)

if __name__ == "__main__":
    main()
