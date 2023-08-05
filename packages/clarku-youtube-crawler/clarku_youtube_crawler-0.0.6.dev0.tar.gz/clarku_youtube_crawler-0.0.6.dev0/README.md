# clarku-youtube-crawler

### ``Version 0.0.1->0.0.3 ``

This is beta without testing since python packaging is a pain. Please don't install these versions.

### ``Version 0.0.5``
Finally figured out testing. It works okay. More documentation to come. To install:

``pip install clarku-youtube-crawler``


### Example usage
```
import clarku_youtube_crawler.RawCrawler as cr
```
After running import, go to ``config.ini`` to configure file paths. Make sure DEVELOPER_KEY.txt (or if the filename differs, configure also in ``config.ini``) is in the same folder. Then run:

```
test = cr.RawCrawler()
test.__build__()
test.crawl("asmr",start_date=1, start_month=1, start_year=2020, day_count=1)
test.crawl_videos_in_list(comment_page_count=1)
test.merge_all()
```

If missing requirements (I already include all dependencies so it shouldn't happen), download ``requirements.txt`` here on this repo
and run 

``$ pip install -r requirements.txt``


