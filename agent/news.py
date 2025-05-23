import requests
from time import sleep
from django.conf import settings


class NewsDataFetchFailed(Exception):
    pass


def fetch_latest_news(query: str):

    for i in range(10):
        print(f"KEY: {settings.NEWS_DATA_API_KEY}")

        res = requests.get(
            "https://newsdata.io/api/1/latest",
            params={"apikey": settings.NEWS_DATA_API_KEY, "q": query},
        )

        if res.status_code == 200:
            break

        sleep(2 * (i + 1))

    else:
        raise NewsDataFetchFailed("Fetch failed.")

    return res.json()
