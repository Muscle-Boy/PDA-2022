import os
import re
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from PIL import Image
import datetime
import pandas as pd
import requests


def get_data(card):
    """Extract data from tweet card"""
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        return

    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except:
        return

    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except:
        return

    try:
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        if "Replying to" in comment:
            comment = ""
    except:
        comment = ""

    try:
        if comment == "":
            responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        else:
            responding = ""
    except:
        responding = ""

    text = comment + responding

    try:
        reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0

    try:
        like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    except:
        like_cnt = 0

    try:
        #element = card.find_element_by_xpath('.//div[2]/div[2]//img[contains(@src, "twimg")]')
        element = card.find_element_by_xpath('.//div[2]/div[2]//img[contains(@src, "format=jpg")]')
        image_link = element.get_attribute('src')
    except:
        image_link = ""

    # handle promoted tweets
    try:
        promoted = card.find_element_by_xpath('.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = card.find_element_by_xpath('.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return

    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, image_link, tweet_url)
    return tweet


def init_driver(headless=True, proxy=None):
    """ initiate a chromedriver instance """

    # create instance of web driver
    options = Options()
    capabilities = DesiredCapabilities.CHROME.copy()
    if headless is True:

        print("Scraping on headless mode.", flush=True)
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Remote(command_executor="http://10.130.2.23:5555/wd/hub", desired_capabilities=capabilities ,options=options)
    driver.set_page_load_timeout(100)
    return driver


def log_search_page(driver, start_date, end_date, lang, display_type, words, to_account, from_account, hashtag):
    """ Search for this query between start_date and end_date"""

    if from_account is not None:
        from_account = "(from%3A" + str(from_account) + ")%20"
    else:
        from_account = ""
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
    hash_tags = "(%23" + hashtag + ")%20" if hashtag is not None else ""

    if words is not None:
        words = '(' + words.replace(' ', '%20') + ')%20'
    else:
        words = ""

    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""

    end_date = "until%3A" + end_date + "%20"
    start_date = "since%3A" + start_date + "%20"

    # to_from = str('%20'.join([from_account,to_account]))+"%20"
    # print('https://twitter.com/search?q=' + words + from_account + to_account + hash_tags + end_date + start_date + lang + '&src=typed_query')
    # driver.get(
    #     'https://twitter.com/search?q=' + words + from_account + to_account + hash_tags + end_date + start_date + lang + '&src=typed_query')
    link = 'https://twitter.com/search?q=(%22covid-19%22%20OR%20%22covid19%22%20OR%20%22covid%22%20OR%20%22coronavirus%22)%20(%22vaccine%22%20OR%20%22vaccination%22%20OR%20%22vaccinate%22%20OR%20%22vaccinating%22%20OR%20%22vaccinated%22)%20near%3Asingapore%20within%3A10mi%20-from%3A%40ChannelNewsAsia%20-from%3A%40straits_times%20-from%3A%40STForeignDesk%20-from%3A%40TODAYonline%20-from%3A%40HIREMAIDEA%20lang%3Aen&src=typed_query&f=live'
    print(link, flush=True)
    driver.get(link)

    sleep(random.uniform(0.5, 1.5))

    # navigate to historical 'Top' or 'Latest' tab
    try:
        driver.find_element_by_link_text(display_type).click()
    except:
        print("%s Button doesnt exist.", display_type, flush=True)

def log_search_page_url(driver, link, display_type):
    driver.get(link)
    sleep(random.uniform(0.5, 1.5))
    # navigate to historical 'Top' or 'Latest' tab
    try:
        driver.find_element_by_link_text(display_type).click()
    except:
        print("%s Button doesnt exist.", display_type, flush=True)

def get_last_date_from_csv(path):
    df = pd.read_csv(path)
    return datetime.datetime.strftime(max(pd.to_datetime(df["Timestamp"])), '%Y-%m-%dT%H:%M:%S.000Z')

#def keep_scroling(driver, data, writer=None, tweet_ids, scrolling, tweet_parsed=0, limit=float("inf"), scroll=0, last_position):
def keep_scroling(driver, images_path, data, tweet_ids, scrolling, last_position, writer=None, tweet_parsed=0, limit=float("inf"), scroll=0):
    """ scrolling function for tweets crawling"""

    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))

        click_show_more_replies(driver)
        click_show_replies(driver)
        click_show_offensive(driver)

        # get the card of tweets
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        for card in page_cards:
            tweet = get_data(card)
            if tweet:
                # check if the tweet is unique
                tweet_id = ''.join(tweet[:-1])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.", flush=True)
                    if writer: # Added by Ben (for default arg)
                        writer.writerow(tweet)
                        save_image(tweet, images_path)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            print("scroll", scroll, flush=True)
            # sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            scroll += 1
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.5, 1.5))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position

def click_show_more_replies(driver):
    # Click on "Show more replies" if present
    button = driver.find_elements_by_xpath('//span[text()="Show more replies"]/../../..')
    if len(button) != 0:
        driver.execute_script("arguments[0].click();", button[0])
        print("Showing more replies", flush=True)
        sleep(random.uniform(1, 2))

def click_show_replies(driver):
    # Click on "Show replies" if present (added by Ben)
    button = driver.find_elements_by_xpath('//span[text()="Show replies"]/../../../..')
    if len(button) != 0:
        #button = driver.find_element_by_xpath('//span[text()="Show more replies"]/../../..')
        driver.execute_script("arguments[0].click();", button[0])
        print("Showing replies", flush=True)
        sleep(random.uniform(1, 2))

def click_show_offensive(driver):
    # Click on "Show additional replies...offensive content" if present
    offensive_button = driver.find_elements_by_xpath('//span[text()="Show"]/../../..')
    if len(offensive_button) != 0:
        driver.execute_script("arguments[0].click();", offensive_button[0])
        print("Showing offensive replies", flush=True)
        sleep(random.uniform(1, 2))

def save_image(tweet, images_path):
    image_link = tweet[-2]
    tweet_url = tweet[-1]
    if image_link:
        tweet_id = tweet_url.split('/')[-1]
        try:
            im = Image.open(requests.get(image_link, stream=True).raw)
        except Exception as err:
            print(err, flush=True)
            print(image_link, flush=True)
            print(tweet_url, flush=True)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(os.path.join(images_path, str(tweet_id) + '.jpg'))