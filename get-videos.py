import requests
import urllib.request
import sys
import getopt
from dotenv import load_dotenv
from pathlib import Path
import os


def main(argv):
    dotenv_path = Path('./config.env')
    load_dotenv(dotenv_path=dotenv_path)

    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

    arg_category = ""
    arg_num_per_page = ""
    arg_help = "{0} -c <category> -npp <num_per_page>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hc:npp:", ["help", "category=",
                                                         "num_per_page="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-c", "--category"):
            arg_category = arg
        elif opt in ("-npp", "--num_per_page"):
            arg_num_per_page = arg

    headers = {
        'Authorization': PEXELS_API_KEY
    }
    response = requests.get(
        f'https://api.pexels.com/videos/search?query={arg_category}&per_page={arg_num_per_page}', headers=headers)

    # get hd quality of video
    quality = {
        "width": [1920, 1280, 3840],
        "height": [1080, 720, 2160]
    }

    for index, video_obj in enumerate(response.json()['videos']):
        link = get_video_url_by_quality_from_video_object(
            video_obj, quality)

        if link:
            urllib.request.urlretrieve(link, f'./videos/{index}.mp4')


def get_video_url_by_quality_from_video_object(video_obj, quality):
    for video_file in video_obj['video_files']:
        if video_file['height'] in quality['height'] and video_file['width'] and quality['width']:
            return video_file['link']


if __name__ == "__main__":
    main(sys.argv)
