# https://developer.twitter.com/en/docs/tutorials/how-to-analyze-the-sentiment-of-your-own-tweets

import requests
import json
import yaml
import os

def process_yaml():
    try:
        with open("config.yaml") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        #use environment variable
        bearer_token = os.environ['TWITTER_BEARER_TOKEN']
        return {'search_tweets_api': {'bearer_token': bearer_token}}

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def twitter_auth_and_connect_post(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("POST", url, headers=headers)
    return response.json()

def print_tweet(tweet):
    print('-----------------------------------------------------')
    print('TWEET ID: ', tweet['id'])
    print(tweet['text'])
    print('-----------------------------------------------------')

#inifinite method
def connect_to_endpoint(url, headers, test=False):
    response = requests.request("GET", url, headers=headers, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if 'data' in json_response:
                print_tweet(json_response["data"])
        if test:
            break

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

# retrieve most recent tweets from @name
def create_twitter_url_most_recent_tweets(name, max_results):
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(name)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        mrf, q
    )
    return url

# retrieve most recent tweets from @name
def get_most_recent_tweets(name, max_results):
    url = create_twitter_url_most_recent_tweets(name, max_results)
    data = process_yaml()
    bearer_token = create_bearer_token(data)

    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json

# retrieve the trendiest tweets from location ID
def get_trending_tweets_by_location(locationID):
    url = "https://api.twitter.com/1.1/trends/place.json?id={}".format(
        locationID
    )
    
    data = process_yaml()
    bearer_token = create_bearer_token(data)

    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json

def post_status(status):
    url = "https://api.twitter.com/1.1/statuses/update.json?status={}".format(
        status
    )
    
    data = process_yaml()
    bearer_token = create_bearer_token(data)

    res_json = twitter_auth_and_connect_post(bearer_token, url)
    return res_json

# get the content of a tweet by its ID
def get_tweet_by_id(tweet_id):
    url = "https://api.twitter.com/2/tweets?ids={}".format(
        tweet_id
    )
    
    data = process_yaml()
    bearer_token = create_bearer_token(data)

    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json

# Functions to interact with my twitter stream:

# look up current stream rules:
def get_twitter_stream_rules():
    url = "https://api.twitter.com/2/tweets/search/stream/rules"
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json

# add a new rule to the twitter stream:
def add_twitter_stream_rule(rule):
    url = "https://api.twitter.com/2/tweets/search/stream/rules"
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    
    headers = {"Authorization": "Bearer {}".format(bearer_token),
              "Content-type": "application/json"}

    data = json.loads('{"add":[{"value":"' + rule + '"}]}')
    response = requests.request("POST", url, headers=headers, json=data)
    
    return response.json()

# helper function to request deletion of rule ids
def delete_twitter_stream_rules(rule_id_string):
    url = "https://api.twitter.com/2/tweets/search/stream/rules"
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    
    headers = {"Authorization": "Bearer {}".format(bearer_token),
              "Content-type": "application/json"}

    data = '{"delete":{"ids":[' + rule_id_string + ']}}'
    response = requests.request("POST", url, headers=headers, data=data)
    
    return response.json()

#clear out old stream rules
def clear_twitter_stream_rules():
    rules_json = get_twitter_stream_rules()
    rule_ids = []

    if 'data' in rules_json:
        for rule in rules_json['data']:
            rule_id = '"' + rule['id'] + '"'
            rule_ids.append(rule_id)
        rule_id_string = ','.join(rule_ids)

        delete_twitter_stream_rules(rule_id_string)

# Run the live twitter stream that I configured filters for
def run_twitter_strem():
    url = "https://api.twitter.com/2/tweets/search/stream"
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    # infinite loop
    connect_to_endpoint(url, headers)
    
if __name__ == "__main__":

    # Get most recent tweets from a user and print them out
    res_json = get_most_recent_tweets('Christo84553156',10) # get 10 most recent tweets from me
    if 'data' in res_json:
        for tweet in res_json['data']:
            print_tweet(tweet)

    # Look up a tweet by its ID and print out the tweet contents
    res_json = get_tweet_by_id('1310231452743864321')
    if 'data' in res_json:
        for tweet in res_json['data']:
            print_tweet(tweet)

    # Get the trendiest hashtags from a location
    # location ID = 1 is worldwide
    # Location ID is WOEID https://www.findmecity.com/
    res_json = get_trending_tweets_by_location(2367105) # Use Boston's location ID
    print('Trending in {}:'.format(res_json[0]['locations'][0]['name']))
    for trend in res_json[0]['trends']:
        print(trend['name'])

    # Try to post a tweet (didn't work)
    # res_json = post_status('OK')
    # {'errors': [{'code': 220, 'message': 'Your credentials do not allow access to this resource.'}]}

    # More compicated example: Create a filtered stream and run it
    clear_twitter_stream_rules()
    res_json = add_twitter_stream_rule('election')
    res_json = get_twitter_stream_rules()

    #infinite loop
    res_json = run_twitter_strem()















