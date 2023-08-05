## Import and configuration
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
from clarku_youtube_crawler.crawlerObject import CrawlerObject

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)
TIME_DELTA = int(config.get("main", "default_time_crawler"))

class RawCrawler(CrawlerObject):
    def __init__(self):
        super().__init__()
        self.PARENT_PATH = config.get("rawfilepath", "parent_path")
        self.video_list_workfile = config.get("rawfilepath", "video_list_workfile")
        self.video_list_dir = config.get("rawfilepath", "video_list_dir")
        self.video_data_dir = config.get("rawfilepath", "video_data_dir")

    def __build__(self):
        try:
            os.mkdir(self.PARENT_PATH)
        except OSError:
            print("Directory already exists %s" % self.PARENT_PATH)
        else:
            print("Successfully created the directory %s " % self.PARENT_PATH)

        try:
            os.mkdir(self.video_list_dir)
        except OSError:
            print("Directory already exists %s" % self.video_list_dir)
        else:
            print("Successfully created the directory %s " % self.video_list_dir)

        try:
            os.mkdir(self.video_data_dir)
        except OSError:
            print("Directory already exists %s" % self.video_data_dir)
        else:
            print("Successfully created the directory %s " % self.video_data_dir)
        super().__build__()

    # Crawl a list of videos which matches {search_key}. Save the data in {video_list_dir}
    # JSON returned from https://developers.google.com/youtube/v3/docs/search/list
    def search_data(self, file_path, start_time, end_time, page_token=None):
        #     print("CURRENT_API: " + DEVELOPER_KEY)
        part = "snippet"
        try:
            if page_token:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      q=self.search_key,
                                                      pageToken=page_token,
                                                      type="video",
                                                      publishedAfter=start_time.isoformat(),
                                                      publishedBefore=end_time.isoformat(),
                                                      regionCode="US"
                                                      ).execute()
            else:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      q=self.search_key,
                                                      type="video",
                                                      publishedAfter=start_time.isoformat(),
                                                      publishedBefore=end_time.isoformat(),
                                                      regionCode="US"
                                                      ).execute()
            self.write_item(file_path, response["items"])
            return response
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            print(error)
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self.try_next_id()
                return self.search_data(file_path, start_time, end_time, page_token)
        except Exception as e:
            sys.exit(0)
            return "error"

    def crawl_data(self, start_time, end_time):
        response = self.search_data(self.video_list_path, start_time, end_time)
        total_result = response["pageInfo"]["totalResults"]
        while True:
            response = self.search_data(self.video_list_path, start_time, end_time, response["nextPageToken"])
            if "nextPageToken" in response:
                page_token = response["nextPageToken"]
            else:
                print(f"total results:{str(total_result)} between {start_time.isoformat()} and {end_time.isoformat()}")
                break

    def crawl_one_day_video(self, start_datetime):
        delta = timedelta(hours=24)
        print(f"crawl video list")
        print(start_datetime.isoformat())
        self.crawl_data(start_datetime, start_datetime + delta)

#different save location SEARCHTEMR_VIDEOLIST_date
    def crawl(self, search_key, **kwargs):
        self.search_key = search_key
        default = datetime.now() - timedelta(days=TIME_DELTA)
        start_day = kwargs.get("start_day", default.day)
        start_month = kwargs.get("start_month", default.month)
        start_year = kwargs.get("start_date", default.year)
        day_count = kwargs.get("day_count", math.inf)

        start_datetime = datetime(year=start_year, month=start_month, day=start_day, tzinfo=pytz.utc)
        date_mark = f"{start_datetime.year}-{start_datetime.month}-{start_datetime.day}"
        delta = timedelta(hours=24)

        count = 0
        while count<day_count:
            print(f"start crawling:{date_mark}")
            # Initialize the paths
            self.video_list_path = f"{self.video_list_dir}video_list_{date_mark}.json"
            # crawl data, update start date.
            self.crawl_one_day_video(start_datetime)
            start_datetime += delta
            date_mark = f"{start_datetime.year}-{start_datetime.month}-{start_datetime.day}"
            count+=1

    # The crawler will iterate each video id in video_list_workfile.csv and get video, channel,
    # comment, and caption data. Each video is saved in an individual json in video_data.
    def get_video(self, video_id):
        part = "id,snippet,statistics,contentDetails"
        try:
            response = self.youtube.videos().list(part=part, maxResults=1, id=video_id).execute()
            if len(response["items"]) == 0:
                return "error"
            return response["items"][0]
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self.try_next_id()
                return self.get_video(video_id)
        except Exception as e:
            return "error"

    # Save video comments of all the videos saved in {video_list_path}
    # JSON returned from https://developers.google.com/youtube/v3/docs/comments

    def get_comments(self, video_id, page_count):
        part = "snippet"
        try:
            response = self.youtube.commentThreads(). \
                list(part=part, maxResults=50, videoId=video_id).execute()
            comments = response["items"]
            counter = 0  # save the first page_count pages
            while "nextPageToken" in response:
                page_token = response["nextPageToken"]
                response = self.youtube.commentThreads(). \
                    list(part=part, maxResults=50, videoId=video_id, pageToken=page_token).execute()
                comments += response["items"]
                if counter == page_count:
                    return comments
                counter += 1
            return comments
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self.try_next_id()
                return self.get_comments(video_id, page_count)
        except Exception as e:
            return "error"

    # Save channel info of all the videos saved in {video_list_path}
    # JSON returned from https://developers.google.com/youtube/v3/docs/channels

    def get_channel(self, channel_id):
        try:
            part = "id,snippet,statistics,contentDetails,topicDetails,brandingSettings,contentOwnerDetails,localizations"
            response = self.youtube.channels().list(part=part, maxResults=1, id=channel_id).execute()
            return response["items"][0]
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self.try_next_id()
                return self.get_channel(channel_id)
        except Exception as e:
            return "error"

    # Save closed captions info of all the videos saved in {video_list_path}
    # JSON returned from YouTubeTranscriptApi
    def get_caption(self, video_id):
        caption = []
        try:
            caption = YouTubeTranscriptApi.get_transcript(video_id)
            return caption
        except Exception as e:
            # print(e)
            return "error"

    def check_if_crawled(self, file_name):
        return os.path.exists(self.video_data_dir + file_name)

    # comment_page_count: how many pages of comments will be crawled. Each page has 50 comments.
    def crawl_videos_in_list(self, comment_page_count):
        self.merge_to_workfile(self.video_list_dir, self.video_list_workfile)
        df = pd.read_csv(self.video_list_workfile)
        for index, row in df.iterrows():
            video_id = row["videoId"][1:]  # remove the ":" in the 1st char
            channel_id = row["channelId"]
            filename = video_id + ".json"
            print(filename)
            if not self.check_if_crawled(filename):
                video = self.get_video(video_id)
                comments = self.get_comments(video_id, comment_page_count)
                channel = self.get_channel(channel_id)
                caption = self.get_caption(video_id)
                result = {
                    "videoId": video_id,
                    "channelId": channel_id,
                    "video": video,
                    "comments": comments,
                    "channel": channel,
                    "caption": caption,
                }
                with open(self.video_data_dir + filename, 'w+') as fp:
                    fp.write(json.dumps(result) + "\n")

    def merge_all(self, **kwargs):
        # merge all video jsons into one big json
        video_result_path = kwargs.get("save_to", self.PARENT_PATH + "/FINAL_result_raw_merged.json")
        video_writer = open(video_result_path, "w+")
        df = pd.read_csv(self.video_list_workfile)
        id_list = list(df["videoId"])
        id_list = [i[1:] for i in id_list]
        id_set = set(id_list)
        print(len(id_set))
        for filename in os.listdir(self.video_data_dir):
            if filename.endswith(".json"):
                if filename.split(".")[0] not in id_set:
                    print(filename)
                # Save video meta data of all the videos saved in {video_list_path}
                with open(self.video_data_dir + filename, 'r') as fp:
                    line = fp.readline()
                    while line and line != "":
                        video_writer.write(line)
                        line = fp.readline()
            else:
                continue
        video_writer.flush()
        video_writer.close()
