#!/usr/bin/env python3
"""
Quick endpoint tester for the chatbot API.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("\n🏥 Testing /api/health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_initialize():
    """Test the initialize endpoint."""
    print("\n🚀 Testing /api/initialize endpoint...")
    print("This may take 2-5 minutes. Initializing backend, scraping website, generating embeddings...")
    try:
        response = requests.post(f"{BASE_URL}/api/initialize", timeout=300)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query():
    """Test the query endpoint."""
    print("\n💬 Testing /api/query endpoint...")
    print("Query: 'Tell me about Nintendo Switch games'")
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": "Tell me about Nintendo Switch games"},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_history():
    """Test the history endpoint."""
    print("\n📋 Testing /api/history endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/history", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Test the stats endpoint."""
    print("\n📊 Testing /api/stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Nintendo Chatbot API Test Suite")
    print("=" * 60)
    
    # Test health first
    if test_health():
        print("\n✅ Health check passed! Server is responsive.")
        
        # Ask user for next steps
        print("\n" + "=" * 60)
        print("What would you like to test next?")
        print("1. Initialize backend (scrape, embed, store)")
        print("2. Query endpoint (requires initialization)")
        print("3. History endpoint")
        print("4. Stats endpoint")
        print("5. Run all tests")
        print("=" * 60)
        
        choice = input("Enter choice (1-5) or 'q' to quit: ").strip()
        
        if choice == "1":
            test_initialize()
        elif choice == "2":
            if test_initialize():
                time.sleep(2)
                test_query()
        elif choice == "3":
            test_history()
        elif choice == "4":
            test_stats()
        elif choice == "5":
            test_initialize()
            time.sleep(2)
            test_query()
            time.sleep(1)
            test_history()
            time.sleep(1)
            test_stats()
    else:
        print("\n❌ Health check failed. Server is not responding.")
        print("Make sure the Flask server is running:")
        print("  PORT=8000 python3 app.py")
