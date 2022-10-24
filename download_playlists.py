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
import time
from multiprocessing import cpu_count
from rich.progress import Progress
from rich import print

VERSION = "1.1"

def get_songs_count(output_directory="./data"):
    counts = {}
    for file in os.listdir(output_directory):
        filename = file[:-4]
        
        file_id, index = filename.split("_")
        if(counts.get(file_id)):
            counts[file_id] = max(counts[file_id], int(index))
        else:
            counts[file_id] = int(index)
        
    return counts
        
        
def get_playlists_to_download(playlists, downloaded_playlists):
    
    playlists_to_download = []
    
    for playlist_to_download in playlists:
        download_playlist = True
        
        for downloaded_playlist in downloaded_playlists:
            if playlist_to_download == downloaded_playlist:
                download_playlist = False
                break
            
        if download_playlist:
            playlists_to_download.append(playlist_to_download)
    
    return playlists_to_download
    

def move_files(progress, style_table, start_indices, duration, 
               input_directory="tmp", output_directory="./data"):
    
    # Create the output directory
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
        
    # Get the total number of songs
    total_songs = 0
    for style in os.listdir(input_directory):
        style_dir = os.path.join(input_directory, style)
        
        if not os.path.isdir(style_dir): continue
           
        for playlist in os.listdir(style_dir):
            playlist_dir = os.path.join(style_dir, playlist)
            
            if not os.path.isdir(playlist_dir): continue
            
            for file in os.listdir(playlist_dir):
                total_songs += 1            
    
    task_2 = progress.add_task("[cyan]Formatting files", total=total_songs)
    
    # Iterate in directories
    for style in os.listdir(input_directory):
        n = start_indices[style]
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
                parameters = ["ffmpeg", "-i", file_path, '-ac', "1", '-ar', 
                              "22050", out_path]
                subprocess.call(parameters,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)

                # Cutting the file to the correct duration
                chunk = cut_file(out_path, duration)
                save_chunk(chunk, out_path, "wav")
                
                progress.advance(task_2)


def create_style_lookup_table(configuration_file):
    style_lookup_table = {}
    
    with open(configuration_file, 'r') as json_file:
        configuration = json.load(json_file)
        music_styles = configuration["music_styles"]
    
        for style in music_styles:
            style_lookup_table[style["name"]] = style["id"]
            
    return style_lookup_table

def download_spotify_playlist(link, output_directory):    
    subprocess.call(
        ["spotify_dl", "-l", link, "-o", "tmp/" + output_directory, "-m", 
         "-mc", str(cpu_count())],
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
    print("Starting downloading data. Version [bold magenta]" +
          VERSION + "[/bold magenta]\n")
    
    if len(argv) == 0:
        printUsage()
        sys.exit(1)
    
    configuration_file = argv[0]
    
    style_lookup_table = create_style_lookup_table(configuration_file)
    starting_indices = {}
    music_styles = {}
    
    with open(configuration_file, 'r') as json_file:
        print("Fetching playlists ... ", end="")
        configuration = json.load(json_file)
        music_styles = configuration["music_styles"]
        print("done")
        
    # Getting total amount of playlists
    total_playlists = 0
    for style in music_styles:
        playlists = style["playlists"]
        already_downloaded_playlists = style["downloaded_playlists"]
        
        playlists_to_download = get_playlists_to_download(
            playlists, already_downloaded_playlists)
        
        total_playlists += len(playlists_to_download)
    
    if total_playlists == 0:
        print("All playlists are downloaded. Use [i][yellow]--force[/i][/yellow]"+
              " to ignore already downloaded playlists.")
        return
    
    with Progress() as progress:
        task_1 = progress.add_task("[cyan]Downloading playlists", 
                                   total=total_playlists)
        
        for i, style in enumerate(music_styles):
            
            name = style["name"]
            starting_indices[name] = style["downloaded_songs"]
            playlists = style["playlists"]
            already_downloaded_playlists = style["downloaded_playlists"]
            
            playlists_to_download = get_playlists_to_download(
                playlists, already_downloaded_playlists)
            
            for playlist in playlists_to_download:
                download_playlist(playlist, name)
                
                music_styles[i]["downloaded_playlists"].append(playlist)
                progress.advance(task_1)
        
        move_files(progress, style_lookup_table, starting_indices, 15)
        rmtree('tmp/')
    
        # Get the new song number for each style
        counts = get_songs_count()
        for style in music_styles:
            style["downloaded_songs"] = int(counts[str(style["id"])]) + 1
        
        # Save the new configuration file
        with open(configuration_file, 'w') as json_file:
            configuration = {}
            configuration["music_styles"] = music_styles
            
            json_file.write(json.dumps(configuration, indent=4))   
    
if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv[1:])
    elapsed_time = "{:.2f}".format(time.time() - start_time)
    
    print("Program ended in [bold green]" + str(elapsed_time) + 
          "[/bold green] seconds.")