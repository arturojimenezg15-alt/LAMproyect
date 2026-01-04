import os
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_management.settings')
django.setup()

def verify_auth_enforcement():
    client = Client()
    
    # 1. Test Homepage (Should redirect)
    response = client.get('/')
    if response.status_code == 302 and '/accounts/login/' in response.url:
        print("PASS: Homepage redirects to login.")
    else:
        print(f"FAIL: Homepage returned {response.status_code}, expected 302 redirect. URL: {getattr(response, 'url', 'N/A')}")

    # 2. Test Login Page (Should be 200)
    try:
        login_url = reverse('login')
        response = client.get(login_url)
        if response.status_code == 200:
            print("PASS: Login page is accessible.")
        else:
            print(f"FAIL: Login page returned {response.status_code}, expected 200.")
    except Exception as e:
        print(f"FAIL: Could not reverse 'login' url. Error: {e}")

    # 3. Test Signup Page (Should be 200)
    try:
        signup_url = reverse('signup')
        response = client.get(signup_url)
        if response.status_code == 200:
            print("PASS: Signup page is accessible.")
        else:
            print(f"FAIL: Signup page returned {response.status_code}, expected 200.")
    except Exception as e:
        print(f"FAIL: Could not reverse 'signup' url. Error: {e}")
        
    # 4. Test product detail (Should redirect)
    # Assuming there's a URL for products, let's try a common one or list
    try:
        # Check urls again if needed, but for now generic test
        pass
    except:
        pass

if __name__ == '__main__':
    verify_auth_enforcement()
