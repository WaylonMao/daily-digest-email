import requests
import random

import tweepy
from dotenv import load_dotenv
import os
import json
import datetime
from urllib import request

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")


# Retrieve a random quote from https://randomwordgenerator.com/motivational-quote.php
def get_random_quote():
    url = "https://randomwordgenerator.com/json/inspirational-quote_ws.json"

    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and "data" in data:
        quotes = data["data"]
        new_quotes = []

        for quote_data in quotes:
            quote_text = quote_data["inspirational_quote"]

            start_index = quote_text.index("“") + 1
            end_index = quote_text.index("” -")
            quote = quote_text[start_index:end_index].strip()

            author_start_index = quote_text.index("<small><i>") + 10
            author_end_index = quote_text.index("</i></small>", author_start_index)
            author = quote_text[author_start_index:author_end_index].strip()

            new_quote = {"quote": quote, "author": author}
            new_quotes.append(new_quote)
            return random.choice(new_quotes)

    else:
        print("No quotes found.")

    return None


def get_weather_forecast(coords={'lat': 51.0460243, 'lon': -114.0756112}):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords['lat']}&lon={coords['lon']}&appid={WEATHER_API}"
        data = json.load(request.urlopen(url))

        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "periods": list()}

        for period in data["list"][0:9]:
            forecast["periods"].append({"timestamp": datetime.datetime.fromtimestamp(period["dt"]),
                                        "temp": round(period["main"]["temp"]),
                                        "description": period["weather"][0]["description"].title(),
                                        "icon": f"http://openweathermap.org/img/wn/{period['weather'][0]['icon']}.png"})
        return forecast
    except Exception as e:
        print(e)
        return None


def get_twitter_trends(woeid=8775):
    try:
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        tweets = tweepy.API(auth).get_place_trends(woeid)[0]["trends"]
        return tweets
    except Exception as e:
        print(e)
        return None


def get_wikipedia_article():
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        data = json.load(request.urlopen(url))
        article = {
            "title": data["title"],
            "extract": data["extract"],
            "url": data["content_urls"]["desktop"]["page"]}
        return article
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # print(get_random_quote())
    # print(get_weather_forecast())
    # print(get_twitter_trends())
    print(get_wikipedia_article())
