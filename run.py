import os
import tldextract
from urllib import request
from pprint import pprint as pp
from urllib.error import URLError, HTTPError, ContentTooShortError

URL = (r'https://cdn.jsdelivr.net/'
       r'gh/hagezi/dns-blocklists@latest/'
       r'domains/native.xiaomi.txt')
url_lists = []

try:
    with request.urlopen(URL) as res:
        txt_bytes = res.read().decode('utf-8')
        for i in txt_bytes.split('\n'):
            if len(i) > 0 and i[0] == '#':
                continue
            url_lists.append(i.replace('\n', ''))
except URLError | HTTPError | ContentTooShortError as e:
    pp(f'ERROR: {e}')

dns_blocker_urls = set()
for url in url_lists:
    extracted = tldextract.extract(url)
    sld = extracted.domain
    tld = extracted.suffix
    if sld and tld:
        dns_blocker_urls.add(f"{sld}.{tld}")

os.remove('./dns_blocker_urls.txt') if \
    os.path.exists('./dns_blocker_urls.txt') else None

with open('./dns_blocker_urls.txt', 'w') as f:
    for i in dns_blocker_urls:
        f.write(f"{i}\n")

pp(dns_blocker_urls)
