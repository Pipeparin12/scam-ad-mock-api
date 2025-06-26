
import asyncio
import aiohttp
from tqdm import tqdm
import random
import time
import os
from supabase import create_client

# === Supabase Setup ===
SUPABASE_URL = "https://hpizxkrurgzlxbryfhzv.supabase.co"         # replace
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwaXp4a3J1cmd6bHhicnlmaHp2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODUyNTI3MywiZXhwIjoyMDY0MTAxMjczfQ.81mZFKrEj2T-AAGa0xTODHzSpZ6k2670pt1KqfK7e5Q"                    # replace
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SUPABASE_TABLE = "api_data"
STORAGE_BUCKET = "adsimages"
MOCK_API_URL = "http://localhost:8000/ads"

# === Config ===
TOTAL_RECORDS = 10000
BATCH_SIZE = 100
CONCURRENT_TASKS = 5

inserted = 0
lock = asyncio.Lock()
start_time = time.time()

async def fetch_mock_batch(session, offset, limit):
    try:
        async with session.get(f"{MOCK_API_URL}?offset={offset}&limit={limit}") as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"[ERROR] Failed to fetch mock data: HTTP {resp.status}")
                return []
    except Exception as e:
        print(f"[ERROR] Exception fetching mock data: {e}")
        return []

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

async def worker(start_offset, end_offset):
    async with aiohttp.ClientSession() as session:
        for offset in range(start_offset, end_offset, BATCH_SIZE):
            raw = await fetch_mock_batch(session, offset, BATCH_SIZE)
            if not raw:
                continue
            await insert_batch(raw)

async def main():
    print(f"[INIT] Starting insert of {TOTAL_RECORDS:,} records without image upload...")
    chunk_size = TOTAL_RECORDS // CONCURRENT_TASKS
    tasks = []
    for i in range(CONCURRENT_TASKS):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, TOTAL_RECORDS)
        tasks.append(asyncio.create_task(worker(start, end)))
    await asyncio.gather(*tasks)
    print(f"[DONE] Inserted {inserted:,} total records")

if __name__ == "__main__":
    asyncio.run(main())

