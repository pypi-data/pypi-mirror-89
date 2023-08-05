# ## Import and configuration
# import json
# from googleapiclient.errors import HttpError
# from datetime import datetime, timedelta
# import pytz
# import pandas as pd
# from configparser import ConfigParser
# import sys
# import os
# import math
# from youtube_transcript_api import YouTubeTranscriptApi
# from clarku_youtube_crawler.crawlerObject import CrawlerObject
#
# CONFIG = "config.ini"
# config = ConfigParser(allow_no_value=True)
# config.read(CONFIG)
#
#
# class ChannelCrawler(CrawlerObject):
#     def __init__(self):
#         super().__init__()
#
#     def __build__(self):
#         super().__build__("channel")
#
#     # read a raw json file and save all channels with subscriber greater than 10k
#     # Save the channels to channel_list_workfile
#     raw_file = parent_path + "/result_raw_0608_1020.json"
#     channel_list = []
#     with open(raw_file, "r") as fp:
#         line = fp.readline()
#         jobj = json.loads(line)
#         while line:
#             jobj = json.loads(line)
#             if "id" in jobj["channel"]:
#                 title = jobj["channel"]["snippet"]["title"] + jobj["channel"]["snippet"]["description"]
#                 if re.search("ASMR", title) and "subscriberCount" in jobj["channel"]["statistics"]:
#                     channel_list.append({
#                         "channelId": jobj["channel"]["id"],
#                         "subscriberCount": int(jobj["channel"]["statistics"]["subscriberCount"])
#                     })
#             line = fp.readline()
#
#     df = pd.DataFrame(channel_list)
#     # Find all unique channels
#     result = df.groupby(by=df.channelId).subscriberCount.first()
#     result = result.sort_values(ascending=False)
#     result = pd.DataFrame(result)
#     # only keep channels with no less than 10,000 subscribers
#     result = result.loc[result.subscriberCount >= 10000]
#     result.to_csv(channel_list_workfile)
#
#
