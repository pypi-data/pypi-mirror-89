from configparser import ConfigParser
from datetime import date
import os
from os import path
# You can configure here or in the generated config.ini file
# If you configure here, make sure to delete existing config.ini

if not os.path.exists("config.ini"):

    DATE = str(date.today()).replace("-","")
    RAW_PARENT_PATH = f"YouTube_RAW_{DATE}/"
    CHANNEL_PARENT_PATH = f"YouTube_CHANNEL_{DATE}/"

    rawfilepath = {
        "DATE": DATE,
        "PARENT_PATH": f"YouTube_RAW_{DATE}/",
        "VIDEO_LIST_WORKFILE": f"{RAW_PARENT_PATH}/video_list.csv",
        "VIDEO_LIST_DIR": f"{RAW_PARENT_PATH}/video_list/",
        "VIDEO_DATA_DIR": f"{RAW_PARENT_PATH}/video_data/"
    }

    channelfilepath = {
        "DATE": DATE,
        "PARENT_PATH": f"YouTube_RAW_{DATE}/",
        "CHANNEL_LIST_WORKFILE": f"{CHANNEL_PARENT_PATH}/channel_list.csv",
        "CHANNEL_VIDEO_LIST_WORKFILE": f"{CHANNEL_PARENT_PATH}/channel_video_list.csv",
        "CHANNEL_LIST_DIR": f"{CHANNEL_PARENT_PATH}/channel_list/",
        "CHANNEL_DATA_DIR": f"{CHANNEL_PARENT_PATH}/channel_data/"
    }

    api = {
        "KEYS_PATH": "DEVELOPER_KEY.txt",
        "YOUTUBE_API_SERVICE_NAME": "youtube",
        "YOUTUBE_API_VERSION": "v3",
        "YOUTUBE_URL": "https://www.googleapis.com/youtube/v3/"
    }

    config = ConfigParser()
    config.read('config.ini')

    config.add_section('rawfilepath')
    for k,v in rawfilepath.items():
        config.set("rawfilepath", k, v)

    config.add_section('channelfilepath')
    for k, v in channelfilepath.items():
        config.set("channelfilepath", k, v)

    config.add_section('api')
    for k,v in api.items():
        config.set("api", k, v)

    with open('config.ini', 'w') as f:
        config.write(f)