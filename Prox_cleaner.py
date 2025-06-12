import requests

def check_proxy(proxy):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        r = requests.get('https://auth.roblox.com', proxies=proxies, timeout=5)
        if r.status_code == 200:
            print(f"✅ Proxy works: {proxy}")
            return True
        else:
            print(f"❌ Proxy failed (status {r.status_code}): {proxy}")
    except Exception as e:
        print(f"❌ Proxy error: {proxy} | {e}")
    return False

def clean_proxies(file_path='proxies.txt'):
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    working_proxies = []
    for proxy in proxies:
        if check_proxy(proxy):
            working_proxies.append(proxy)

    with open(file_path, 'w') as f:
        for wp in working_proxies:
            f.write(wp + '\n')

    print(f"\nDone! {len(working_proxies)} working proxies saved to {file_path}")

if __name__ == "__main__":
    clean_proxies()
