import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def validate_api_key():
    if not API_KEY:
        raise ValueError(
            "ERROR: NEWS_API_KEY not found.\n"
            "Please set it in your environment variables or in a .env file."
        )


def fetch_articles(keyword=None, start_date=None, end_date=None):
    params = {
        "apiKey": API_KEY,
        "sources": "bbc-news",
        "q": keyword,
        "from": start_date,
        "to": end_date,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                f"API request failed with status {response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        if data.get("status") != "ok":
            raise RuntimeError(f"API Error: {data}")

        return data.get("articles", [])

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again later.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {e}")


def summarize_articles(articles):
    if not articles:
        print("No articles found for the given filters.")
        return

    for art in articles:
        print("--------------------------------------------------------")
        print("Title:", art.get("title"))
        print("Published At:", art.get("publishedAt"))
        print("Description:", art.get("description"))
        print("URL:", art.get("url"))
        print("--------------------------------------------------------\n")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="News summarizer with keyword and date filtering."
    )
    #provide this format "--k football"
    parser.add_argument(
        "--keyword",
        "-k",
    )
    #provide this format "--f YYYY-MM-DD"
    parser.add_argument(
        "--from-date",
        "-f",
    )
    #provide this format "--t YYYY-MM-DD"
    parser.add_argument(
        "--to-date",
        "-t",
    )
    return parser.parse_args()


def validate_date_format(date_text):
    if date_text:
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_text}. Use YYYY-MM-DD")


def main():
    try:
        validate_api_key()

        args = parse_arguments()

        validate_date_format(args.from_date)
        validate_date_format(args.to_date)

        articles = fetch_articles(
            keyword=args.keyword,
            start_date=args.from_date,
            end_date=args.to_date,
        )

        summarize_articles(articles)

    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()

