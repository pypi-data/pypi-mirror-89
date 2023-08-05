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

# TODO: fix path name for videolist to include search term
# TODO: Document what each variable name means
# TODO: Look into the possible duplicate video in 2 videolist.csv


class CrawlerObject():
    def __init__(self):
        # more permanent
        self.DEVELOPER_KEY = None
        self.YOUTUBE_API_SERVICE_NAME = None
        self.YOUTUBE_API_VERSION = None
        self.KEYS_PATH = None
        self.TIME_DELTA = None
        self.codes = []

        #more changing
        self.youtube = None
        self.search_key = None
        self.code_index = -1

        #depends more on user's config
        self.RAW_PARENT_PATH = None
        self.video_list_workfile = None
        self.video_list_dir = None
        self.video_data_dir = None
        self.video_list_path = None  # for individual video, constantly changing

        self.CHANNEL_PARENT_PATH = None
        self.channel_data_dir = None
        self.channel_list_dir = None
        self.channel_list_workfile = None
        self.channel_video_list_workfile = None


    def __build__(self, objectType):
        self._fetch_vars()
        raw_dest_list = [self.RAW_PARENT_PATH, self.video_list_dir, self.video_data_dir]
        channel_dest_list = [self.CHANNEL_PARENT_PATH, self.channel_list_dir, self.channel_data_dir]
        if objectType=="raw":
            destination_list = raw_dest_list
        if objectType == "channel":
            destination_list = channel_dest_list
        for dest in destination_list:
            try:
                os.mkdir(dest)
            except OSError:
                print("Directory already exists %s" % dest)
            else:
                print("Successfully created the directory %s " % dest)

        self.try_next_id()
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY,
            cache_discovery=False)
        print("BUILD SUCCESS")

    def _fetch_vars(self):
        self.TIME_DELTA = int(config.get("main", "default_time_crawler"))
        self.YOUTUBE_API_SERVICE_NAME = config.get("api", "youtube_api_service_name")
        self.YOUTUBE_API_VERSION = config.get("api", "youtube_api_version")
        self.KEYS_PATH = config.get("api", "keys_path")
        with open(self.KEYS_PATH, 'r+') as fp:
            self.codes = fp.readlines()

        # channel
        self.CHANNEL_PARENT_PATH = config.get("channelfilepath", "channel_parent_path")
        self.channel_video_list_workfile = \
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_video_list_workfile")
        self.channel_list_workfile =\
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_list_workfile")
        self.channel_list_dir =\
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_list_dir")
        self.channel_data_dir =\
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_data_dir")

        # raw
        self.RAW_PARENT_PATH = config.get("rawfilepath", "raw_parent_path")
        self.video_list_workfile =\
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_list_workfile")
        self.video_list_dir =\
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_list_dir")
        self.video_data_dir =\
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_data_dir")

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
                            video_list.add((video_id, channel_id, date, search_key))
                        line = fp.readline()
            else:
                continue
        df = pd.DataFrame(data=video_list, columns=["videoId", "channelId", "publishedAt", "searchKey"])
        df.to_csv(destination, index=False)

    def write_item(self, file_path, items):
        with open(file_path, 'a+') as fp:
            for item in items:
                fp.write(json.dumps(item) + "\n")

    def toDayFormat(self, date):
        return f"{date.month}-{date.day}-{date.year}"
