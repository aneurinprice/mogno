Images stolen from https://github.com/djpisbionic/Movie-Poster-Banner-Adder - The inspiration behind this project

Requires:
  - imagemagick (Installed on host)
  - plexapi (Python module)


# How to run
  `python3 main.py`
# Function

This script is designed to add bluray and 4k  banners onto movie posters in plex. I doubt many people will want this, but it's of mild interest ot me.

## How it works

  - This script uses the plex API to search for 1080p and 4k content in a given library + collection
  - The CURRENT poster being used in plex is then download
  - The corresponding bluray header is applied
  - The newly generated poster can then be uploaded automagically to plex (This is configurable)

## Before
![Before](assets/before.jpg?raw=true "Before")

## After
![After](assets/after.jpg?raw=true "After")


# Configuration

All config is handed in the `config.yaml` file. it is pre-populated with example data

```
PlexHost: "http://192.168.1.1:32400"	(You can aim this at an SSL frontend e.g. https://plex.example.com - This can lead to timeout issues if you have a large library)

PlexToken: "AnExampleToken"		(https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

PlexMoviesLibrary: "Blurays" 		(The library containing all of your Blurays, Script is not clever enough to know if the file is actually bluray or not, it will apply to any eligable movies in the library)

UploadPoster: False			(Replace the current poster associated with the given movie in plex)

KeepPoster: True			(Keep the generated posters in the `output` directory. This is useful to check content before uploading)

BlurayCollection: "Blurays"		(The Plex collection in the provided library that contains your Blurays)
```

# FAQ

  - How do I choose which poster is used for the new art?	MOGNO will use whatever poster is currently in plex. Setting the desired image
  - Can I use this for TV Shows?				Not yet. I do intend to add support for TV shows as I have a large number of TV Shows on bluray. It is more complex due to the existence of the `Season` entities with thier own posters
  - I am seeing timeouts when performing the poster operations?	This can happen when trying to run this against a host not on your network , for best results please make sure you are on the same LAN and use the servers IP address
