"""Test script to verify the keep-alive server is working"""

import requests
import sys

def test_health_check(url):
    """Test the health check endpoint"""
    
    print(f"Testing health check at: {url}")
    print("=" * 60)
    
    endpoints = ['/', '/health', '/ping']
    
    for endpoint in endpoints:
        full_url = url.rstrip('/') + endpoint
        try:
            print(f"\n📡 Testing: {full_url}")
            response = requests.get(full_url, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS")
            else:
                print(f"   ❌ FAILED")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://graduatingcounterbot.onrender.com"
    
    test_health_check(url)
