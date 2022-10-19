# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:33:28 2022

@author: Tom
"""

import json
import sys
import re
import subprocess
import os

import spotify_dl

def download_spotify_playlist(link, output_directory):
    print("Downloading spotify playlist :", link)
    subprocess.call(["spotify_dl", "-l", link, "-o", "tmp/" + output_directory, "-m"])

def download_youtube_playlist(link, output_directory):
    print("Downloading youtube playlist :", link)

def download_playlist(link, output_directory):
    if re.search("(spotify)\w*", link):
        download_spotify_playlist(link, output_directory)
    elif re.search("(youtube)\w*", link):
        download_youtube_playlist(link)
    else:
        print("Unsupported playlist :", link, output_directory)


def printUsage():
    print("Usage : download_playlists <configuration file>")


def main(argv):
    if len(argv) == 0:
        printUsage()
        sys.exit(1)
    
    configuration_file = argv[0]
    
    with open(configuration_file, 'r') as json_file:
        configuration = json.load(json_file)
    
        music_styles = configuration["music_styles"]
        for style in music_styles:
                
            name = style["name"]
            playlists = style["playlists"]
            
            for playlist in playlists:
                download_playlist(playlist, name)
                
            print("Finished downloading playlists")
            print("Starting formating and cutting")
            
    
if __name__ == "__main__":
    main(sys.argv[1:])