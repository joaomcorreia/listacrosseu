#!/usr/bin/env python3
"""
Test script for the new assistant endpoint /assistant/api/ask/
This tests all the requirements for Step 11
"""
import requests
import json

BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/assistant/api/ask/"

def test_assistant_endpoint():
    print("🧪 Testing Assistant API Endpoint")
    print("=" * 50)
    
    # Test 1: Valid message
    print("\n1️⃣ Testing valid message...")
    try:
        response = requests.post(
            ENDPOINT, 
            json={"message": "Hello, can you help me find businesses in Amsterdam?"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert "status" in data
        assert data["status"] == "ok"
        print("✅ Valid message test PASSED")
    except Exception as e:
        print(f"❌ Valid message test FAILED: {e}")
    
    # Test 2: Empty message
    print("\n2️⃣ Testing empty message...")
    try:
        response = requests.post(
            ENDPOINT,
            json={"message": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
        data = response.json()
        assert data["reply"] == "Empty message"
        assert data["status"] == "error"
        print("✅ Empty message test PASSED")
    except Exception as e:
        print(f"❌ Empty message test FAILED: {e}")
    
    # Test 3: Missing message field
    print("\n3️⃣ Testing missing message field...")
    try:
        response = requests.post(
            ENDPOINT,
            json={"other_field": "test"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        data = response.json()
        assert data["status"] == "error"
        print("✅ Missing message field test PASSED")
    except Exception as e:
        print(f"❌ Missing message field test FAILED: {e}")
    
    # Test 4: GET method (should return 405)
    print("\n4️⃣ Testing GET method...")
    try:
        response = requests.get(ENDPOINT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 405
        print("✅ GET method test PASSED")
    except Exception as e:
        print(f"❌ GET method test FAILED: {e}")
    
    # Test 5: Complex business question
    print("\n5️⃣ Testing complex business question...")
    try:
        response = requests.post(
            ENDPOINT,
            json={"message": "I want to start a restaurant in Portugal. Can you help me understand the requirements?"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        assert response.status_code == 200
        assert data["status"] == "ok"
        assert len(data["reply"]) > 10  # Should have a meaningful response
        print("✅ Complex question test PASSED")
    except Exception as e:
        print(f"❌ Complex question test FAILED: {e}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_assistant_endpoint()