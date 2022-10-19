# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:00:43 2022

@author: Tom
"""

import os

def move_files(input_directory="tmp", output_directory="./data"):
    # list to store files
    styles = {}
    
    # Iterate directory
    for style in os.listdir(input_directory):
        style_dir = os.path.join(input_directory, style)
        
        if os.path.isdir(style_dir):
            for playlist in os.listdir(style_dir):
                for file in os.listdir(os.path.join(style_dir, playlist)):
                    res.append(file)
            
    print(res)

if __name__ == "__main__":
    move_files()