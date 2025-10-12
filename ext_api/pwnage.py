import httpx
import asyncio
from hashlib import sha1
from typing import List

async def check_pwnage(password: str):
    async with httpx.AsyncClient() as client:
        sha1pwd = sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1pwd[:5], sha1pwd[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = await client.get(url)
        response.raise_for_status()
        for line in response.text.splitlines():
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return True
        return False
    
async def collect_results(password_list: List[str]):
    pwnage_map = {}
    tasks = [check_pwnage(password) for password in password_list]
    results = await asyncio.gather(*tasks)

    for i, pwnage in enumerate(results):
        pwnage_map[password_list[i]] = pwnage

    return pwnage_map