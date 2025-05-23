import requests
from time import sleep


class ArticleFetchFailed(Exception):
    pass


def fetch_article(url: str):
    for i in range(10):
        res = requests.get(url)

        if res.status_code == 200:
            break

        sleep(2 * (i + 1))

    else:
        raise ArticleFetchFailed("Fetch failed.")

    return res.text
