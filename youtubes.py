import urllib.request as ur
import json, os, sys
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time


def look_for_new_video():
    api_key = os.getenv("API_KEY")
    channel_id = os.getenv("CHAN_ID")

    base_url = "https://www.youtube.com/watch?v="
    base_search = "https://www.googleapis.com/youtube/v3/search?"

    url = base_search + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(api_key, channel_id)
    print(url)
    inp = ur.urlopen(url)
    resp = json.load(inp)

    vidID = resp['items'][0]['id']['videoId']

    video_exists = False
    with open('videoid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['videoId'] != vidID:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(base_url + vidID)
            video_exists = True

    if video_exists:
        with open('videoid.json', 'w') as json_file:
            data = {'videoId': vidID}
            json.dump(data, json_file)
            print('Saved .json')


try:
    while True:
        look_for_new_video()
        time.sleep(100)
except KeyboardInterrupt:
    print(" Stopping")
