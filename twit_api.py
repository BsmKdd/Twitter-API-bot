"""
Just shutting up pylint
"""
import os
import json
import time
import asyncio
from tweepy import TweepyException, StreamingClient, StreamRule, Client
from dotenv import load_dotenv
from bot import push_message, bot

load_dotenv("var.env")

accounts_file = open("accounts.json", encoding="utf-8")
accounts_dict = json.load(accounts_file)
accounts = list(list(accounts_dict.values()))
accounts_file.close()

client = Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
)


class TweetFeeder(StreamingClient):
    """
    Just shutting up pylint
    """

    def __init__(self, bearer_token):
        super().__init__(
            bearer_token, wait_on_rate_limit=True, daemon=True, max_retries=2
        )

        self.bearer_token = bearer_token

    def on_tweet(self, tweet):
        author_id = tweet.author_id

        user = client.get_user(id=author_id)

        screen_name = user.data.name
        username = user.data.username

        status_url = f"{screen_name} tweeted:\nhttps://twitter.com/{username}/status/{tweet.id}"
        asyncio.run_coroutine_threadsafe(push_message(status_url), bot.loop)

    def on_connection_error(self):
        print("TweetCreep disconnected!")
        self.disconnect()

    def on_request_error(self, status_code):
        print("Request Error:", status_code)
        self.disconnect()

    def on_exception(self, exception):
        print("Exception:", exception)
        self.disconnect()

    def on_connect(self):
        print("Connected to Twitter API v2!")
        asyncio.run_coroutine_threadsafe(
            push_message("Connected to Twitter API v2!"), bot.loop
        )

    def on_disconnect(self):
        print("Disconnected from Twitter API!")
        asyncio.run_coroutine_threadsafe(
            push_message("Disconnected from Twitter API!"), bot.loop
        )
        time.sleep(20)

        try:
            self.filter(tweet_fields=["author_id"], threaded=True)

        except TweepyException as exc:
            print(str(exc))

    def on_closed(self, response):
        print("Stream has been closed by Twitter,", response)
        self.disconnect()
        time.sleep(20)

        try:
            self.filter(tweet_fields=["author_id"], threaded=True)
        except TweepyException as exception:
            print(str(exception))


tweet_feeder = TweetFeeder(bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"))

######## DELETE RULES AND RERUN CLIENT
result = tweet_feeder.get_rules()
time.sleep(2)
rule_ids = []

if result.data:
    for rule in result.data:
        print(f"Rule marked for deletion: {rule.id} - {rule.value}")
        rule_ids.append(rule.id)

if len(rule_ids) > 0:
    tweet_feeder.delete_rules(rule_ids)
    time.sleep(2)
    tweet_feeder = TweetFeeder(
        bearer_token=os.environ.get("TWITTER_BEARER_TOKEN")
    )
else:
    print("no rules to delete")

for account in accounts:
    tweet_feeder.add_rules(StreamRule(f"from:{account}"))
    time.sleep(2)


tweet_feeder.filter(tweet_fields=["author_id"], threaded=True)
