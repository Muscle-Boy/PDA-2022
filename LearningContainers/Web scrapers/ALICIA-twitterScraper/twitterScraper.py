import os
import json
import random
from datetime import datetime
from twython import Twython
from twython import TwythonError
from scweet import scrap
from scweet import scrape_url
from time import sleep
from utils import init_driver
from utils import get_data
from utils import keep_scroling

class Tweet():
    def __init__(self, tweet):
        self.id = tweet['id_str']
        self.url = "https://twitter.com/{}/status/{}".format(tweet['user']['id_str'], tweet['id_str'])
        self.site = "twitter"
        self.title = None
        self.username = tweet['user']['name']
        self.datetime = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        self.content = tweet['full_text']
        self.comments = []
        self.num_comments = 1
        self.in_reply_to_status_id_str = tweet['in_reply_to_status_id_str']
        self.tweet = tweet

    def add_comments(self, tweet):
        self.num_comments += tweet.num_comments
        self.comments.append(tweet)
    
    def has_comment(self, tweet_id):
        for com in self.comments:
            if com.id == tweet_id:
                return True
        return False

    def is_reply(self):
        return self.in_reply_to_status_id_str != None

    def copy(self):
        # Create deep copy of comments
        comments_copy = []
        for c in self.comments:
            comments_copy.append(c.copy())
        tweet_copy = Comment(self.tweet)
        tweet_copy.comments = comments_copy
        return tweet_copy

    def get_comments(self):
        comments = []
        for i in range(len(self.comments)):
            comments.append(self.comments[i].get_json_object(i + 1))
        return comments
    
    def get_json_object(self):
        return {
            'url': self.url,
            'site': self.site,
            'title': self.title,
            'username': self.username,
            'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'content': self.content,
            'comments': self.get_comments() if self.comments else None
        }

class Comment(Tweet):

    def get_json_object(self, i, is_original=False):
        if is_original:
            return super().get_json_object()
        else:
            return {
                'commentID': i,
                'username': self.username,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'content': self.content,
                'comments': self.get_comments() if self.comments else None
            }

# Scrape THREAD for comments and returns a list of tweet cards
# Refer to output of utils.get_data() for output format
def load_page(driver, tweet_url):
    print("Loading site: {}".format(tweet_url), flush=True)
    driver.get(tweet_url)
    sleep(random.uniform(1, 2))

    last_position = driver.execute_script("return window.pageYOffset;")

    driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position = \
                keep_scroling(driver=driver, data=[], tweet_ids=set(), scrolling=True, last_position=last_position)

    return data

# Recursively fill tweet with comments (downwards)
def fill_comments(driver, tweet):
    data = load_page(driver, tweet.url)
    comments = []
    for comment_card in data:
        if comment_card:
            comment_id = comment_card[-1].split('/')[-1]
            if comment_id in cache:
                comment = cache[comment_id]
            else:
                comment = get_tweet(comment_id)
            if comment.in_reply_to_status_id_str == tweet.id: # Comment is a reply to current tweet
                reply_cnt = int(comment_card[5]) if comment_card[5] else 0
                if reply_cnt > 0: # Has replies
                    print("{} has {} replies".format(tweet.url, reply_cnt), flush=True)
                    comment = fill_comments(driver, comment)
                comments.append(comment) # Only include direct replies
            else:
                add_to_cache(comment)
    for c in comments:
        tweet.add_comments(c)

    return tweet

def remove_children(tweet_id):
    lower_comments = id_to_tweet[tweet_id].comments
    id_to_delete = []
    while lower_comments:
        c = lower_comments.pop(0)
        if c.id in id_to_tweet:
            id_to_delete.append(c.id)
            if id_to_tweet[c.id].comments:
                lower_comments.extend(id_to_tweet[c.id].comments)
    for i in id_to_delete:
        del id_to_tweet[i]
    if tweet_id in id_to_tweet:
        del id_to_tweet[tweet_id]

def get_tweet(status_id):
    global api_call_count
    api_call_count += 1
    if api_call_count % 50 == 0:
        print("API call count: {}".format(api_call_count), flush=True)
    try:
        return Comment(twitter.show_status(id=status_id, tweet_mode='extended'))
    except TwythonError as e:
        print(e, flush=True)

def add_to_cache(tweet):
    if len(cache) == 200:
        del cache[list(cache.keys())[0]]
    cache[tweet.id] = tweet

# Create JSON file containing url, username, datetime and content
# If this function is called, fill in the values for APP_KEY and APP_SECRET to provide authentication for Twython
def write_to_json(tweets, path, get_comments=False):
    output = {"data": []}

    # Initialise webdriver for scraping comments
    if get_comments:
        driver = init_driver(True, None)

    for user_screen_name, username, timestamp, text, emojis, comments, likes, retweets, image_links, tweet_url in tweets:
        status_id = tweet_url.split('/')[-1]
        print("Scraping {}".format(tweet_url), flush=True)
        original_tweet = get_tweet(status_id)

        # Scrape comments for each tweet
        if get_comments:
            data = load_page(driver, tweet_url)

            for comment_card in data:
                if comment_card:
                    #print("Comment: \n" + comment[3])
                    comment_id = comment_card[-1].split('/')[-1]
                    if original_tweet.has_comment(comment_id): # Skip comment if it's already present
                        print("original_tweet has comment", flush=True)
                        continue
                    if comment_id in id_to_tweet: # Comment has been scraped as a root tweet before
                        # Add comment as child to parent tweet
                        original_tweet.add_comments(id_to_tweet[comment_id].copy())
                        # Delete all child tweets stored
                        remove_children(comment_id)
                    else: # Comment has not been scraped before
                        comment = get_tweet(comment_id)
                        if comment.in_reply_to_status_id_str == original_tweet.id: # Comment is a reply to current tweet
                            comment = fill_comments(driver, comment)
                            original_tweet.add_comments(comment)

        id_to_tweet[status_id] = original_tweet # Tweets with the same parent are replaced (assumption: later tweets are replies to earlier tweets)

    for tweet in id_to_tweet.values():
        output["data"].append(tweet.get_json_object(0, True))

    with open(os.path.join(path, 'outputs', 'data.json'), 'w') as outfile:
        json.dump(output, outfile)

    # Close driver if initialised earlier
    if get_comments:
        driver.close()

# Paste key and secret from Developer Portal over here
APP_KEY = "lBtf2pW3LXm3b61Bqlv3b7Tp0"
APP_SECRET = "Eqyz4r8kwBkifw0U1Ga3iVTXFAVrKj5ibg1ty30vaiU716a6gx"

twitter = Twython(APP_KEY, APP_SECRET)

# Uncomment the bottom 2 lines to scrape with the various scraper options
# search_query = "\"covid vaccine\""
# tweets = scrap(words=search_query, start_date="2021-03-25", max_date="2021-03-27", interval=2, headless=True, limit=200, display_type="Latest", hashtag=None)
id_to_tweet = {}
cache = {}
api_call_count = 0

def run_scraper(url, path, limit, get_json):
    tweets = scrape_url(url, path, headless=True, limit=limit, display_type="Latest")
    if get_json:
        if APP_KEY and APP_SECRET:
            write_to_json(tweets, path)
        else:
            print("APP_KEY and/or APP_SECRET not supplied. JSON file is NOT created.", flush=True)