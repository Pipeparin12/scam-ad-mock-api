import asyncio
import aiohttp
from tqdm import tqdm
import random
import time
import os
import json
from supabase import create_client

# === Supabase Setup ===

SUPABASE_TABLE = "api_data"
STORAGE_BUCKET = "adsimages/ads"

# Make API URL configurable - use environment variable or default to localhost
MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8000/ads")

# === Config ===
TOTAL_RECORDS = 1000
BATCH_SIZE = 100
CONCURRENT_TASKS = 2

# 50 scam-related keywords for generating varied data
SCAM_KEYWORDS = [
    "investment", "money", "crypto", "forex", "bitcoin", "profit", "income", "earn",
    "winner", "prize", "lottery", "free", "gift", "congratulations", "selected",
    "urgent", "suspended", "verify", "security", "alert", "warning", "expired",
    "police", "FBI", "IRS", "government", "refund", "tax", "audit", "warrant",
    "virus", "infected", "hacked", "breach", "malware", "support", "microsoft",
    "apple", "google", "amazon", "paypal", "bank", "credit", "card", "payment",
    "account", "login", "password", "confirm", "update", "click", "download"
]

inserted = 0
lock = asyncio.Lock()
start_time = time.time()

async def fetch_mock_batch(session, limit, keywords_subset=None):
    try:
        # Use random subset of keywords if none provided
        if not keywords_subset:
            keywords_subset = random.sample(SCAM_KEYWORDS, min(10, len(SCAM_KEYWORDS)))
            
        request_body = {
            "keyword": keywords_subset,  # Now sending array of keywords
            "category": None,  # all categories
            "location": "thailand",
            "language": "thai", 
            "advertiser": "all",
            "platform": "all",
            "media_type": "all",
            "status": "all",
            "start_date": "June 18,2018",
            "end_date": "today",
            "limit": limit
        }
        
        async with session.post(MOCK_API_URL, json=request_body) as resp:
            if resp.status == 200:
                response_data = await resp.json()
                return response_data.get("ads", [])
            else:
                print(f"[ERROR] Failed to fetch mock data: HTTP {resp.status}")
                return []
    except Exception as e:
        print(f"[ERROR] Exception fetching mock data: {e}")
        return []

async def download_and_upload_image(session, url, seed):
    filename_local = f"temp_{seed}.jpg"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename_local, "wb") as f:
                    f.write(await resp.read())
                remote_path = f"ads/{seed}_{random.randint(1000,9999)}.jpg"
                with open(filename_local, "rb") as f:
                    result = supabase.storage.from_(STORAGE_BUCKET).upload(remote_path, f, {"upsert": True})
                os.remove(filename_local)
                if result.get("error"):
                    print(f"[UPLOAD ERROR] {result['error']['message']}")
                    return None
                return supabase.storage.from_(STORAGE_BUCKET).get_public_url(remote_path)
    except Exception as e:
        print(f"[IMAGE ERROR] {e}")
    return None

async def transform_batch(session, raw_batch):
    transformed = []
    for item in raw_batch:
        # Handle image_urls which is now a JSON string
        try:
            image_urls_list = json.loads(item.get("image_urls", "[]"))
            new_image_urls = []
            for img_url in image_urls_list:
                seed = img_url.split("/seed/")[1].split("/")[0] if "/seed/" in img_url else str(random.randint(1,10000))
                supa_url = await download_and_upload_image(session, img_url, seed)
                if supa_url:
                    new_image_urls.append(supa_url)
            # Convert back to JSON string
            item["image_urls"] = json.dumps(new_image_urls)
        except (json.JSONDecodeError, KeyError):
            item["image_urls"] = "[]"
        
        transformed.append(item)
    return transformed

async def insert_batch(batch):
    global inserted
    try:
        supabase.table(SUPABASE_TABLE).insert(batch).execute()
        async with lock:
            inserted += len(batch)
            if inserted % 100 == 0:
                elapsed = time.time() - start_time
                print(f"[INFO] Inserted {inserted:,} rows in {elapsed:.1f}s")
    except Exception as e:
        print(f"[INSERT ERROR] {e}")

async def worker(records_to_fetch):
    async with aiohttp.ClientSession() as session:
        remaining = records_to_fetch
        while remaining > 0:
            current_batch_size = min(BATCH_SIZE, remaining)
            # Use different keyword combinations for variety
            keywords_subset = random.sample(SCAM_KEYWORDS, min(random.randint(5, 15), len(SCAM_KEYWORDS)))
            raw = await fetch_mock_batch(session, current_batch_size, keywords_subset)
            if not raw:
                print(f"[WARNING] No data returned for keywords: {keywords_subset[:3]}...")
                remaining -= current_batch_size  # Skip this batch
                continue
            batch = await transform_batch(session, raw)
            await insert_batch(batch)
            remaining -= len(batch)

async def main():
    print(f"[INIT] Starting insert of {TOTAL_RECORDS:,} records with image download + upload...")
    print(f"[INFO] Using mock API at: {MOCK_API_URL}")
    print(f"[INFO] Using {len(SCAM_KEYWORDS)} different scam keywords for variety")
    chunk_size = TOTAL_RECORDS // CONCURRENT_TASKS
    tasks = []
    for i in range(CONCURRENT_TASKS):
        records_for_worker = chunk_size if i < CONCURRENT_TASKS - 1 else TOTAL_RECORDS - (i * chunk_size)
        tasks.append(asyncio.create_task(worker(records_for_worker)))
    await asyncio.gather(*tasks)
    print(f"[DONE] Inserted {inserted:,} total records")

if __name__ == "__main__":
    asyncio.run(main())
