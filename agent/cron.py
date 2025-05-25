import tweepy
from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from datetime import timedelta

from agent.news import fetch_latest_news
from agent.scraper import fetch_article
from agent.llm import generate_tweet, summarise_page
from agent.models import BotStatus, Tweet

from django.conf import settings


class Tweeter(CronJobBase):
    RUN_EVERY_MINS = 1  # Runs every minute, decision logic is internal

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "agent.tweeter"

    def do(self):
        try:
            bot = BotStatus.objects.first()
            if not bot:
                print("No BotStatus record found.")
                return

            if not bot.is_active:
                print("Bot is inactive, skipping.")
                return

            if bot.last_run and now() < bot.last_run + timedelta(
                minutes=bot.interval_minutes
            ):
                print("Interval has not passed yet.")
                return

            links = fetch_latest_news("Crypto")
            links = [item["link"] for item in links["results"]][:3]
            print(f"{len(links)} links got")

            articles = []
            for link in links:
                try:
                    articles.append(summarise_page(fetch_article(link)))
                    # print(f"Fetched article [{link}]")
                except Exception:
                    # print(f"Failed to fetch article [{link}]")
                    pass

            # print("Generating tweet")

            if articles:
                tweet_text = generate_tweet(articles, bot.ai_prompt)
                # print("Tweet generated")

                client = tweepy.Client(
                    settings.TWITTER_BEARER_TOKEN,
                    settings.TWITTER_API_KEY,
                    settings.TWITTER_API_SECRET,
                    settings.TWITTER_ACCESS_TOKEN,
                    settings.TWITTER_ACCESS_SECRET,
                )

                tweet = client.create_tweet(text=tweet_text)

                tweet = Tweet.objects.create(
                    twitter_id=tweet.data["id"],
                    content=tweet_text,
                )
                # print(f"Tweet saved with ID {tweet.twitter_id}")
            else:
                print("No articles fetched")
                pass

            # Update last run
            bot.last_run = now()
            bot.save()

        except Exception as e:
            print("Error in Tweeter cron job:", e)
            raise e
            pass
