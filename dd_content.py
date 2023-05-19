import requests
import random
from dotenv import load_dotenv
import os
import json
import datetime
from urllib import request

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API")


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
    print(WEATHER_API)
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords['lat']}&lon={coords['lon']}&appid={WEATHER_API}"
        print(url)
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


def get_twitter_trends():
    pass


def get_wikipedia_article():
    pass


if __name__ == '__main__':
    print(get_random_quote())
    print(get_weather_forecast())
