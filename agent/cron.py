from django_cron import CronJobBase, Schedule
from django.utils.timezone import now


from agent.news import fetch_latest_news
from agent.scraper import fetch_article
from agent.llm import generate_tweet, summarise_page


class Tweeter(CronJobBase):
    RUN_EVERY_MINS = 1  # every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "agent.tweeter"  # a unique code for the job

    def do(self):
        try:
            links = fetch_latest_news("Crypto")
            links = [item["link"] for item in links["results"]][:3]
            print(f"{len(links)} links got")

            articles = []
            for link in links:
                try:
                    articles.append(summarise_page(fetch_article(link)))
                    print(f"Fetched article [{link}]")
                except:
                    print(f"Failed to fetch article [{link}]")

            print("Generating tweet")

            if articles:
                tweet = generate_tweet(articles)
                print("Tweet generated")
            else:
                print("No articles fetched")

            print(tweet)
        except Exception as e:
            print(e)
