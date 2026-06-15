#!/usr/bin/env python3.13
"""
Test different CEIDG API endpoints to find working one.
"""

import asyncio
import httpx

TEST_NIP = "9511604749"

API_ENDPOINTS = [
    "https://dane.biznes.gov.pl/api/ceidg/v2/firma",
    "https://dane.biznes.gov.pl/api/ceidg/v1/firma",
    "https://dane.biznes.gov.pl/api/ceidg/firma",
    "https://api.ceidg.gov.pl/api/ceidg/v2/firma",
    "https://api.ceidg.gov.pl/api/ceidg/v1/firma",
]

async def main():
    print(f"Testing CEIDG API endpoints for NIP: {TEST_NIP}")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        for url in API_ENDPOINTS:
            print(f"\nTesting: {url}")
            try:
                response = await client.get(
                    url,
                    params={"nip": TEST_NIP},
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; Nevumo-Bot/1.0; +https://nevumo.com)",
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                print(f"  Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"  ✅ SUCCESS!")
                    print(f"  Response type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"  Keys: {list(data.keys())[:10]}")
                    print(f"  Sample data: {str(data)[:500]}")
                    break
                else:
                    print(f"  Error: {response.text[:100]}")
            except Exception as e:
                print(f"  Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
