import os
import time
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")


def masquer_cle(url: str) -> str:
    return url.replace(API_KEY, "***")


cache = {}          # url -> (données, timestamp de stockage)
locks = {}          # url -> asyncio.Lock (un verrou par URL)
CACHE_TTL = 3600    # 1 heure


async def fetch_with_cache(session, url, max_retries=3, timeout=10):
    # 1. Vérification rapide (sans verrou) : si le cache est frais, on renvoie direct
    if url in cache:
        data, stored_at = cache[url]
        if time.time() - stored_at < CACHE_TTL:
            print(f"[CACHE HIT] {masquer_cle(url)}")
            return data
        else:
            print(f"[CACHE EXPIRÉ] {masquer_cle(url)}")
            del cache[url]

    # 2. On prend le verrou de CETTE url
    if url not in locks:
        locks[url] = asyncio.Lock()

    async with locks[url]:
        # 3. Double vérification : une autre tâche a peut-être rempli le cache pendant qu'on attendait
        if url in cache:
            data, stored_at = cache[url]
            if time.time() - stored_at < CACHE_TTL:
                print(f"[CACHE HIT après lock] {masquer_cle(url)}")
                return data

        # 4. Appel API (une seule fois par URL, grâce au lock)
        print(f"[API CALL] {masquer_cle(url)}")
        for tentative in range(max_retries):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        cache[url] = (data, time.time())
                        return data
                    elif response.status in [429, 500, 503]:
                        print(f"Erreur {response.status}. Pause... (essai {tentative + 1})")
                        await asyncio.sleep(2 ** tentative)
                    else:
                        return {"error": f"statut {response.status}"}
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Erreur réseau : {e}. Pause... (essai {tentative + 1})")
                await asyncio.sleep(2 ** tentative)

        return {"error": "échec après plusieurs tentatives"}


async def main():
    urls = [
        f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/551?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}&language=fr-FR",
    ]

    async with aiohttp.ClientSession() as session:
        print("=== Premier passage ===")
        await asyncio.gather(*[fetch_with_cache(session, u) for u in urls])
        print(f"\nTaille du cache : {len(cache)}\n")

        print("=== Deuxième passage (tout doit venir du cache) ===")
        await asyncio.gather(*[fetch_with_cache(session, u) for u in urls])
        print(f"\nTaille du cache : {len(cache)}")


if __name__ == "__main__":
    asyncio.run(main())