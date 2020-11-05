from TwitterAPI import *

def test_process_yaml():
    yaml = process_yaml()
    assert type(yaml["search_tweets_api"]["bearer_token"]) is str

def test_create_bearer_token():
    dic = {"search_tweets_api":{"bearer_token":"X"}}
    assert create_bearer_token(dic) is "X"

def test_twitter_auth_and_connect():
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    url = "https://api.twitter.com/2/tweets/search/stream/rules"
    response = twitter_auth_and_connect(bearer_token, url)
    assert 'meta' in response

def test_connect_to_endpoint():
    url = "https://api.twitter.com/2/tweets/search/stream"
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    # just run this to make sure no exceptions.
    # test=True to break out of infinite loop
    connect_to_endpoint(url, headers, test=True)

def test_create_twitter_url_most_recent_tweets():
    url = create_twitter_url_most_recent_tweets('cat',10)
    assert 'max_results=10' in url
    assert 'query=from:cat' in url

def test_get_most_recent_tweets():
    # functional test only. Output is too volatile to test for accuracy
    res_json = get_most_recent_tweets('Christo84553156',10)
    assert 'meta' in res_json

def test_get_most_recent_tweets_negative():
    # functional test only. Output is too volatile to test for accuracy
    res_json = get_most_recent_tweets('notAvalid-usernamee',10)
    assert 'meta' in res_json

def test_get_trending_tweets_by_location():
    boston_loc_id = 2367105
    res_json = get_trending_tweets_by_location(boston_loc_id)
    assert 'trends' in res_json[0]

def test_get_trending_tweets_by_location_negative_1():
    invalid_loc_id = 92017482348392532
    res_json = get_trending_tweets_by_location(invalid_loc_id)
    assert 'errors' in res_json

def test_get_trending_tweets_by_location_negative_2():
    invalid_loc_id = 0
    res_json = get_trending_tweets_by_location(invalid_loc_id)
    assert 'errors' in res_json

def test_get_tweet_by_id():
    # static test tweet
    res_json = get_tweet_by_id('1310231452743864321')
    assert res_json['data'][0]['id'] == '1310231452743864321'
    assert res_json['data'][0]['text'] == 'Overcast skies in Boston today.'

def test_get_tweet_by_id_negative():
    # static test tweet
    res_json = get_tweet_by_id('9310231452743864321') # not valid
    assert 'errors' in res_json
    
def test_clear_twitter_stream_rules():
    clear_twitter_stream_rules()
    res_json = get_twitter_stream_rules()
    assert 'meta' in res_json

def test_add_twitter_stream_rules():
    clear_twitter_stream_rules()
    res_json = add_twitter_stream_rule('election')
    assert 'data' in res_json
    assert 'meta' in res_json
    assert res_json['data'][0]['value'] == 'election'

def test_add_get_clear_twitter_stream_rules():
    clear_twitter_stream_rules()
    add_twitter_stream_rule('B')
    add_twitter_stream_rule('C')
    res_json = get_twitter_stream_rules()
    assert 'data' in res_json
    assert 'meta' in res_json
    assert len(res_json['data']) == 2
    assert res_json['data'][0]['value'] == 'B'
    assert res_json['data'][1]['value'] == 'C'
    clear_twitter_stream_rules()
    res_json = get_twitter_stream_rules()
    assert not 'data' in res_json

def test_duplicate_add_twitter_stream_rules():
    clear_twitter_stream_rules()
    add_twitter_stream_rule('B')
    res_json = add_twitter_stream_rule('B')
    assert 'errors' in res_json
    assert 'meta' in res_json
    assert res_json['meta']['summary']['not_created'] == 1

