"""Python Script for Bulk edits of plex posters to add Bluray/UHD Banners."""
import os
import shutil
import argparse
import re
import requests
import yaml
from plexapi.server import PlexServer

def load_config(config_file='config.yaml'):
    """Load config from yaml file"""
    with open(config_file, mode='r', encoding='UTF-8') as file:
        parsed_config = yaml.safe_load(file)
    plex_server = PlexServer(parsed_config['PlexHost'], parsed_config['PlexToken'])
    plex_server.resources()
    return parsed_config, plex_server

def download_poster (get_movie):
    """Download the poster for a given movie and return path to poster on disk"""
    poster = re.sub("[^a-zA-Z0-9]+", "",get_movie.title)
    poster = poster + '.jpg'
    # pylint: disable=line-too-long
    result = requests.get(config['PlexHost']+movie.thumb, headers={'X-PLEX-TOKEN': config['PlexToken']}, timeout=5, stream = True)
    result.decode_content = True
    with open('tmp/' + poster,'wb') as image:
        shutil.copyfileobj(result.raw, image)
    return poster

def add_banner (category, poster):
    """Add banner to poster image with imagemagick"""
    # pylint: disable=line-too-long
    os.system('magick tmp/' + poster + ' assets/' + category + '.png -resize %[fx:u.w]x%[fx:u.h] -gravity north -composite output/' + poster)

def upload_poster (upload_movie, poster):
    """Upload poster to plex"""
    upload_movie.uploadposter(filepath='./output/' + poster)
    print(poster + " Uploaded")

def tidy_up (poster):
    """Remove temporary files if Keepposter is not configured"""
    if not config['KeepPoster']:
        os.remove('output/' + poster)
    os.remove('tmp/' + poster)

def run_main (selected_movie, category):
    """ Main Function """
    poster = download_poster(selected_movie)
    add_banner(category, poster)
    if config['UploadPoster']:
        upload_poster(movie, poster)
    tidy_up(poster)
    print("Completed " + selected_movie.title)

# pylint: disable=line-too-long
parser = argparse.ArgumentParser(description='Python Script for Bulk edits of plex posters to add Bluray/UHD Banners.')
parser.add_argument("-c", "--config", help="Set config file location")
args = parser.parse_args()

config, plex = load_config(args.config)
movies = plex.library.section(config['PlexMoviesLibrary'])


for movie in movies.search(collection=config['BlurayCollection'], resolution="4k"):
    run_main(movie, "UHD")

for movie in movies.search(collection=config['BlurayCollection'], resolution="1080p"):
    run_main(movie, "Bluray")
