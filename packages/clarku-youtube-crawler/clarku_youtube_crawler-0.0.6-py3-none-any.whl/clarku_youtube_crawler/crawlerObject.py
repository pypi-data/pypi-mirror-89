from googleapiclient.discovery import build
import json
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz
import pandas as pd
from configparser import ConfigParser
import sys
import os
import math
from youtube_transcript_api import YouTubeTranscriptApi

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)
TIME_DELTA = int(config.get("main", "default_time_crawler"))


class CrawlerObject():
    def __init__(self):
        self.code_index = -1
        self.DEVELOPER_KEY = None
        self.youtube = None
        self.search_key = None
        self.codes = []
        self.PARENT_PATH = None
        self.video_list_workfile = None
        self.video_list_dir = None
        self.video_list_path = None  # for individual video

        self.YOUTUBE_API_SERVICE_NAME = config.get("api", "youtube_api_service_name")
        self.YOUTUBE_API_VERSION = config.get("api", "youtube_api_version")
        self.KEYS_PATH = config.get("api", "keys_path")

        with open(self.KEYS_PATH, 'r+') as fp:
            self.codes = fp.readlines()

    # maybe write get youtube api service so everytime rebuild it's updated
    def __build__(self):
        self.try_next_id()
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY,
            cache_discovery=False)
        # the rest of build are checking dir path, and are in other classes since they have different path name

    # Try update the API
    def try_next_id(self):
        if self.code_index + 1 < len(self.codes):
            self.code_index += 1
            self.DEVELOPER_KEY = self.codes[self.code_index].strip()  # Update a new key
            self.youtube = build(
                self.YOUTUBE_API_SERVICE_NAME,
                self.YOUTUBE_API_VERSION,
                developerKey=self.DEVELOPER_KEY,
                cache_discovery=False)
            print(f"Update Developer Key:{self.DEVELOPER_KEY}")
        else:
            print("running out keys")
            os._exit(0)
        self.DEVELOPER_KEY = self.codes[self.code_index].strip()  # Use your own Keys.

    # The field crawler will use the video_list_workfile.csv to crawl video data of each video id.
    def merge_to_workfile(self, filepath, destination):
        video_list = set()
        for filename in os.listdir(filepath):
            if filename.endswith(".json"):
                # Save video meta data of all the videos saved in {video_list_path}
                with open(filepath + filename, 'r') as fp:
                    line = fp.readline()
                    while line and line != "":
                        search_result = json.loads(line)
                        if "videoId" in search_result["id"]:
                            video_id = ":" + search_result["id"]["videoId"]
                            channel_id = search_result["snippet"]["channelId"]
                            date = search_result["snippet"]["publishedAt"].split("T")[0]
                            search_key = self.search_key
                            video_list.add((video_id, channel_id, date))
                        line = fp.readline()
            else:
                continue
        df = pd.DataFrame(data=video_list, columns=["videoId", "channelId", "publishedAt","searchKey"])
        df.to_csv(destination, index=False)

    def write_item(self, file_path, items):
        with open(file_path, 'a+') as fp:
            for item in items:
                fp.write(json.dumps(item) + "\n")
