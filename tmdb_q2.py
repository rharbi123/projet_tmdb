import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")


def masquer_cle(url: str) -> str:
    return url.replace(API_KEY, "***")


async def fetch_movie_async(session, movie_id, max_retries=3, timeout=10):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=fr-FR"

    for tentative in range(max_retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:

                if response.status == 200:
                    data = await response.json()
                    return {"id": movie_id, "titre": data.get("title")}

                elif response.status in [429, 500, 503]:
                    print(f"Erreur {response.status}. Pause... (ID {movie_id}, essai {tentative + 1})")
                    await asyncio.sleep(2 ** tentative)

                elif response.status in [400, 401, 403, 404]:
                    return {"id": movie_id, "titre": f"Erreur fatale {response.status}"}

                else:
                    return {"id": movie_id, "titre": f"Erreur inattendue {response.status}"}

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Erreur réseau : {e}. Pause... (ID {movie_id}, essai {tentative + 1})")
            await asyncio.sleep(2 ** tentative)

    return {"id": movie_id, "titre": "Échec après plusieurs tentatives"}


async def fetch_route_async(session, url, idx, max_retries=3, timeout=10):
    for tentative in range(max_retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"route": idx, "status": 200, "apercu": str(data)[:80] + "..."}
                elif response.status in [429, 500, 503]:
                    print(f"Erreur {response.status}. Pause... (route {idx}, essai {tentative + 1})")
                    await asyncio.sleep(2 ** tentative)
                else:
                    return {"route": idx, "status": response.status, "apercu": "erreur fatale"}
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Erreur réseau : {e}. Pause... (route {idx}, essai {tentative + 1})")
            await asyncio.sleep(2 ** tentative)

    return {"route": idx, "status": "échec", "apercu": "après plusieurs tentatives"}


async def main():
    routes = [
        f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/551?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/550/credits?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/550/reviews?api_key={API_KEY}&language=fr-FR",
        f"https://api.themoviedb.org/3/movie/552?api_key={API_KEY}&language=fr-FR",
    ]

    print(f"Lancement de {len(routes)} requêtes en parallèle...")

    async with aiohttp.ClientSession() as session:
        taches = [fetch_route_async(session, url, i) for i, url in enumerate(routes)]
        resultats = await asyncio.gather(*taches)

        print("\n--- Résultats ---")
        for res in resultats:
            print(res)


if __name__ == "__main__":
    asyncio.run(main())