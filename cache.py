#main caching system   </Z3r0X>
import os
import time
import pickle
import json

class CacheHandler:
    def __init__(self, filename="cache.pkl", expiry_seconds=3600, minimal_init=False):
        self.filename = filename
        self.expiry_seconds = expiry_seconds
        self.cache = {} if minimal_init else self.load_cache()

    def load_cache(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "rb") as cache:
                    print("[+] CACHE: Loaded from disk.")
                    return pickle.load(cache)
            except Exception as e:
                print(f"[!] Failed to load cache: {e}")
                return {}
        else:
            print("[!] No existing cache found, rebuilding cache.")
            return {}

    def save_cache(self):
        try:
            with open(self.filename, "wb") as cache:
                pickle.dump(self.cache, cache)
                print("[+] CACHE: Saved to disk.")
        except Exception as e:
            print(f"[!] Failed to save cache: {e}")

    def get(self, url):
        entry = self.cache.get(url)
        if not entry:
            return None
        age = time.time() - entry["timestamp"]
        if age < self.expiry_seconds:
            return entry["content"]
        else:
            print(f"[!] CACHE EXPIRED: Re-fetching {url}")
            return None

    def set(self, url, content):
        self.cache[url] = {
            "content": content,
            "timestamp": time.time()
        }
        self.save_cache()

class Clear(CacheHandler):
    def __init__(self, filename="cache.pkl"):
        super().__init__(filename=filename, minimal_init=True)
        self.cache = {}
        print("[+] CACHE: Emptied successfully.")
        self.save_cache()
        print("[*] Exiting...")
        exit()

class FileSystem():
    def __init__(self, filename="output.json", log_file=True):
        self.filename = filename
        self.cache = {}

    def save_file(self, results):
        try:
            with open(self.filename, "w") as jsonfile:
                json.dump(results, jsonfile, indent=4)
        except Exception as e:
            print(f"\n[!] FileSavingError: {e}")￼Enter
