def test_proxy(proxy_url):
    proxy = get_proxy_dict(proxy_url)
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=5)
        if r.status_code == 200:
            print(f"[✔️] Proxy working: {proxy_url}")
            return True
    except:
        pass
    print(f"[✖️] Proxy failed: {proxy_url}")
    return False

def filter_working_proxies(proxy_file='proxies.txt'):
    working_proxies = []
    proxies = load_proxies(proxy_file)
    for p in proxies:
        if test_proxy(p):
            working_proxies.append(p)
    with open('working_proxies.txt', 'w') as f:
        for wp in working_proxies:
            f.write(wp + '\n')
    print(f"Saved {len(working_proxies)} working proxies to working_proxies.txt")
