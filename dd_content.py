import requests
import random


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


def get_weather_forecast():
    pass


def get_twitter_trends():
    pass


def get_wikipedia_article():
    pass


if __name__ == '__main__':
    print(get_random_quote())
