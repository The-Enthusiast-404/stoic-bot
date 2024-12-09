import os
import requests
import tweepy

def get_quote():
    response = requests.get('https://stoic-quotes.com/api/quote')
    if response.status_code == 200:
        data = response.json()['data']
        return f"{data['body']} — {data['author']}"
    return None

def post_to_x(quote):
    api_key = os.environ['TWITTER_API_KEY']
    api_secret_key = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(quote)

def main():
    quote = get_quote()
    if quote:
        post_to_x(quote)

if __name__ == '__main__':
    main()