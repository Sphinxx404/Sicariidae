#Sicariidae Web Crawler   </Z3r0X>
#Note: this tool is open source, for testing and educational usage only!
import sys
import random
import aiohttp
import asyncio
import pyfiglet
from bs4 import BeautifulSoup
from cache import CacheHandler, Clear
from colorama import Fore, Style, init
from urllib.parse import urlparse

init(autoreset=True)

#colors
red = Fore.RED
blue = Fore.BLUE
yellow = Fore.YELLOW
green = Fore.GREEN
white = Fore.WHITE
cyan = Fore.CYAN

class WebScraper:
    def __init__(self):
        self.cache = CacheHandler()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1"
        ]

    async def fetch_page(self, url, session):
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive"
        }

        cached_page = self.cache.get(url)
        if cached_page:
           print(green + f"\n[+] CACHE: Using saved data for {url}")
           return url, cached_page

        print(green + f"\n[+] FETCHING: Downloading {url}")
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                   html = await response.text()
                   self.cache.set(url, html)
                   await asyncio.sleep(2)
                   return url, html
                else:
                   print(red + f"\n[!] Error: Status {response.status} for {url}")
                   return None
        except Exception as e:
            print(red + f"\n[!] An Error occurred: {e}")
            return None

    def extract(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.title.string.strip() if soup.title else "yellow + [?] No page title found."

            h1 = [tag.text.strip() for tag in soup.find_all("h1")]
            h2 = [tag.text.strip() for tag in soup.find_all("h2")]
            h3 = [tag.text.strip() for tag in soup.find_all("h3")]
            h4 = [tag.text.strip() for tag in soup.find_all("h4")]
            h5 = [tag.text.strip() for tag in soup.find_all("h5")]
            h6 = [tag.text.strip() for tag in soup.find_all("h6")]

            headers = {
                "h1": h1, "h2": h2, "h3": h3,
                "h4": h4, "h5": h5, "h6": h6
            }

            links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
            if not links:
                print(yellow + f"\n[?] No links found in the page.\n")

            return {
                "title": title,
                "headers": headers,
                "links": links
            }

        except Exception as e:
            print(red + f" \n[!] HTML Parsing Error: {e}\n")
            return None

    async def scrape_url(self, urls):
        results = {}
        async with aiohttp.ClientSession() as session:
            tsk = [self.fetch_page(url, session) for url in urls]
            res = await asyncio.gather(*tsk)
            for i, result in enumerate(res):
               if result:
                  url, html = result
                  info = self.extract(html)
                  results[url] = info
               else:
                  results[urls[i]] = None
        return results

if __name__ == "__main__":
    print(blue + pyfiglet.figlet_format("SICARIIDAE"))
    print(cyan + "[+] Tip: use comma to separate multiple URLs\n")

    if "-C" in sys.argv or "--clear-cache" in sys.argv:
       print("[DEBUG] Clear-cache argument detected.\n")
       Clear()

    url_input = str(input("\turl > "))
    urls = [u.strip() for u in url_input.split(",") if u.strip()]

    if url_input.strip().lower() == "exit":
         sys.exit(1)

    invalid_url = [u for u in urls if not (urlparse(u).scheme in ("https", "http") and (urlparse(u).netloc))]

    if invalid_url:
        print(red + f"\n[!] Invalid URL(s): {'' .join(url_input)}\n")
        sys.exit(1)

    scraper = WebScraper()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        results = loop.run_until_complete(scraper.scrape_url(urls))

    except KeyBoardInterrupt:
        print(yellow + "\n[?] Program interrupted by user")
        sys.exit(1)
    print("\n--- Results ---")
    for url, info in results.items():
        if info:
            print(f"\n[URL] {url}")
            print(f"Title  : {info['title']}")
            print("Headers:")
            for h_tag, tags in info['headers'].items():
                print(f"  {h_tag.upper()}: {tags}")
            print(f"Links  : {info['links'][:10]} ...")
        else:
            print(red + f"[!] Could not scrape: {url}"
