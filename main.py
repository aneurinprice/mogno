from plexapi.server import PlexServer
import os
import requests
import shutil

PlexHost = 'PLEX HOST HERE'
PlexToken = 'PLEX TOKEN HERE'
PlexMoviesLibrary = "NAME OF MOVIE LIBRARY"

plex = PlexServer(PlexHost, PlexToken)

movies = plex.library.section(PlexMoviesLibrary)
movies = movies.search(resolution=2160)
# Film Index number here --------------| I will fix this at some point
result = requests.get(PlexHost+movies[122].thumb, headers={'X-PLEX-TOKEN': PlexToken}, stream = True)
result.decode_content = True
with open("image.jpg",'wb') as f:
	shutil.copyfileobj(result.raw, f)
	os.system('magick image.jpg assets/UHD.png -resize %[fx:u.w]x%[fx:u.h] -gravity north -composite output.jpg')
