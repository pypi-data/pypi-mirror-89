import os
import time
import traceback

import feedparser
from youtube_dl import YoutubeDL, setproctitle

__version__ = "0.1.1"

TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
FEED_URL = "https://video.aktualne.cz/rss/dvtv/"
LAST_PUB_DATE_FILE = os.path.expanduser("~/.dvtv.pub_date.txt")


def main():
    # set process title
    setproctitle("dvtv-dl")

    # parse last publication date stored in file
    try:
        with open(LAST_PUB_DATE_FILE) as f:
            last_pub_date = time.strptime(f.read().strip(), TIME_FORMAT)
    except Exception:
        last_pub_date = None

    # fetch and parse RSS feed
    feed = feedparser.parse(FEED_URL)

    for entry in sorted(feed["entries"], key=lambda entry: entry["published_parsed"]):
        try:
            # skip previously downloaded entries
            pub_date = time.strptime(entry["published"], TIME_FORMAT)
            if last_pub_date and last_pub_date >= pub_date:
                continue

            print(entry["published"], entry["title"])

            # download the entry
            with YoutubeDL() as ytdl:
                ytdl.download([entry["link"]])

            # store publication date
            temp_filename = f"{LAST_PUB_DATE_FILE}.{os.getpid()}"
            with open(temp_filename, "w") as f:
                f.write(entry["published"])
            os.rename(temp_filename, LAST_PUB_DATE_FILE)
        except Exception:
            # print traceback on exception
            traceback.print_exc()
