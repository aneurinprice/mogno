from plexapi.server import PlexServer
import plexapi
import os
import requests
import shutil
import yaml
import re

def LoadConfig():
	with open('config.yaml', 'r') as file:
	    config = yaml.safe_load(file)
	plex = PlexServer(config['PlexHost'], config['PlexToken'])
	plex.resources()
	return config, plex

def DownloadPoster (movie):
	Poster = re.sub("[^a-zA-Z0-9]+", "",movie.title)
	Poster = Poster + '.jpg'
	result = requests.get(config['PlexHost']+movie.thumb, headers={'X-PLEX-TOKEN': config['PlexToken']}, stream = True)
	result.decode_content = True
	with open('tmp/' + Poster,'wb') as f:
		shutil.copyfileobj(result.raw, f)
	return Poster

def AddBanner (movie, category, Poster):
	os.system('magick tmp/' + Poster + ' assets/' + category + '.png -resize %[fx:u.w]x%[fx:u.h] -gravity north -composite output/' + Poster)
	

def UploadPoster (movie, Poster):
	movie.uploadPoster(filepath='./output/' + Poster)
	print(Poster + " Uploaded")	
def TidyUp (movie, Poster):
	if not (config['KeepPoster']):
		os.remove('output/' + Poster) 
	os.remove('tmp/' + Poster)

def RunMain (movie, category):
	Poster = DownloadPoster(movie)
	AddBanner(movie, category, Poster)
	if (config['UploadPoster']):
		UploadPoster(movie, Poster)
	TidyUp(movie, Poster)
	print("Completed " + movie.title)


config, plex = LoadConfig()
movies = plex.library.section(config['PlexMoviesLibrary'])


for movie in movies.search(collection=config['BlurayCollection'], resolution="4k"):
	RunMain(movie, "UHD")

for movie in movies.search(collection=config['BlurayCollection'], resolution="1080p"):
	RunMain(movie, "Bluray")
