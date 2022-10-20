# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:33:28 2022

@author: Tom
"""

import os
import json
import sys
import re
import subprocess
from shutil import rmtree
from cut_file import cut_file, save_chunk

def move_files(style_table, duration, input_directory="tmp", output_directory="./data"):
    
    # Create the output directory
    if os.path.exists(output_directory):
        rmtree(output_directory)
    
    os.mkdir(output_directory)
    
    # Iterate in directories
    for style in os.listdir(input_directory):
        n = 0
        style_dir = os.path.join(input_directory, style)
        
        if not os.path.isdir(style_dir): continue
           
        for playlist in os.listdir(style_dir):
            playlist_dir = os.path.join(style_dir, playlist)
            
            if not os.path.isdir(playlist_dir): continue
            
            for file in os.listdir(playlist_dir):
                file_path = os.path.join(playlist_dir, file)
                
                # Getting the style id
                style_id = style_table[style]
                name = str(style_id) + "_" + str(n) + ".wav"
                n += 1
                
                out_path = os.path.join(output_directory, name)

                # Convert to wav and moving the file
                parameters = ["ffmpeg", "-i", file_path, out_path]
                subprocess.call(parameters,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)

                # Cutting the file to the correct duration
                chunk = cut_file(out_path, duration)
                save_chunk(chunk, out_path, "wav")


def create_style_lookup_table(configuration_file):
    style_lookup_table = {}
    
    with open(configuration_file, 'r') as json_file:
        configuration = json.load(json_file)
        music_styles = configuration["music_styles"]
    
        for style in music_styles:
            style_lookup_table[style["name"]] = style["id"]
            
    return style_lookup_table

def download_spotify_playlist(link, output_directory):
    subprocess.call(["spotify_dl", "-l", link, "-o", "tmp/" + output_directory, "-m"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

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
    
    style_lookup_table = create_style_lookup_table(configuration_file)
    
    with open(configuration_file, 'r') as json_file:
        print("Fetching playlists")
        configuration = json.load(json_file)
        print("Done")
    
        print("Downloading playlists")
        music_styles = configuration["music_styles"]
        for style in music_styles:
                
            name = style["name"]
            playlists = style["playlists"]
            
            for i, playlist in enumerate(playlists):
                print("[", name, "] Downloading playlist", (i + 1), "/", len(playlists))
                download_playlist(playlist, name)
            
        print("Done")
        print("Starting formating, moving and cutting")
        
        move_files(style_lookup_table, 15)
        
        print("Done")
        print("Starting cleanup")
        
        rmtree('tmp/')
        
        print("Done")
            
    
if __name__ == "__main__":
    main(sys.argv[1:])