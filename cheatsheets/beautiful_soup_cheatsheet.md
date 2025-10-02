# Basic Beautiful Soup Web Scraping — Cheatsheet

> **Always** check a site's Terms of Service and `robots.txt`, set a User-Agent, add delays, and avoid heavy parallel requests.

## Install
```bash
pip install requests beautifulsoup4 lxml
# optional
pip install requests-cache
```

## Fetch HTML (politely)
```python
import requests

headers = {"User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0; +https://example.com/contact)"}
url = "https://example.com"

resp = requests.get(url, headers=headers, timeout=15)
resp.raise_for_status()          # error if 4xx/5xx
html = resp.text                 # use resp.content for bytes
```

## Parse HTML
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "lxml")   # or "html.parser"
```

## Core selection patterns
### By tag / attributes
```python
title_tag = soup.find("h1")                              # first <h1>
links = soup.find_all("a", href=True, limit=10)          # list of <a> with href
btns = soup.find_all("a", {"class": "btn primary"})      # attrs dict
```

### CSS selectors (powerful & concise)
```python
cards = soup.select("div.card")                          # all .card
first_price = soup.select_one(".price .amount")          # first match
product_links = soup.select('a[href*="/product/"]')      # href contains "/product/"
```

### Text, attributes, and cleaning
```python
text = first_price.get_text(strip=True)
href = product_links[0].get("href", "")
raw_html = product_links[0].decode()                     # original HTML of tag
```

## Navigating the tree
```python
card = soup.select_one("div.card")
heading = card.find("h2")
next_card = card.find_next_sibling("div")
parent = card.parent
descendants = list(card.descendants)                     # iterate children/deeper
```

## Attribute queries + regex
```python
import re
imgs = soup.find_all("img", src=re.compile(r"\.jpg$"))
items = soup.find_all("div", class_=re.compile(r"^item(-\w+)?$"))
```

## Build absolute URLs
```python
from urllib.parse import urljoin

base = "https://example.com/category/"
for a in soup.select("a"):
    absolute = urljoin(base, a.get("href", ""))
```

## Pagination loop (pattern)
```python
import time
from urllib.parse import urljoin

results = []
base = "https://example.com/blog/"
url = base
while url:
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # extract items per page
    for article in soup.select("article.post"):
        title = article.select_one("h2 a").get_text(strip=True)
        link = urljoin(url, article.select_one("h2 a")["href"])
        results.append({"title": title, "url": link})

    # find next page
    nxt = soup.select_one('a[rel="next"], a.next, a:contains("Next")')
    url = urljoin(url, nxt["href"]) if nxt and nxt.get("href") else None

    time.sleep(1.5)  # be nice
```

## Save to CSV
```python
import csv

with open("articles.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["title","url"])
    w.writeheader()
    w.writerows(results)
```

## Sessions, timeouts, retries
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update(headers)

retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

resp = session.get("https://example.com", timeout=15)
```

## Speed ups with caching (development)
```python
import requests_cache
requests_cache.install_cache("cache", expire_after=3600)
# now requests.get(...) will be cached for 1 hour
```

## Quick end-to-end example
```python
import time, csv, requests, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {"User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0)"}
start_url = "https://example.com/products/"

def scrape_listing(url):
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    rows = []
    for card in soup.select("div.product-card"):
        name = card.select_one(".name").get_text(strip=True)
        price = card.select_one(".price").get_text(strip=True)
        link = urljoin(url, card.select_one("a")["href"])
        rows.append({"name": name, "price": price, "url": link})

    next_link = soup.select_one('a[rel="next"], .pagination a.next')
    next_url = urljoin(url, next_link["href"]) if next_link and next_link.get("href") else None
    return rows, next_url

all_rows, url = [], start_url
while url:
    rows, url = scrape_listing(url)
    all_rows.extend(rows)
    time.sleep(1.2)

with open("products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["name","price","url"])
    w.writeheader()
    w.writerows(all_rows)

print(f"Saved {len(all_rows)} products.")
```

## Common pitfalls
- Sites with heavy JS may require **Selenium**, **Playwright**, or server-side APIs.
- Avoid brittle selectors; prefer stable IDs, data-attributes, or semantic structure.
- Normalize whitespace and strip currency symbols before numeric parsing.
- Handle locales (decimal separators), encoding, and timeouts.
- Respect rate limits; use caching during dev.
- Legal: obey ToS; do not scrape data that requires authentication unless you have explicit permission.

---

**Tip:** For structured sites, also check for APIs or embedded JSON (`<script type="application/ld+json">`). Parsing JSON is often simpler than scraping HTML.
