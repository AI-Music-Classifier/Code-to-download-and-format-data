# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:44:21 2022

@author: Tom
"""

from pydub import AudioSegment
import sys, getopt

def cut_file(inputfile, duration):
    try:
        segment = AudioSegment.from_wav(inputfile)
    except FileNotFoundError:
        print("File not found :", inputfile)
        sys.exit(3)
    
    print("Information:")
    print("* Channels:", segment.channels)
    print("* Bits per sample:", segment.sample_width * 8)
    print("* Sampling frequency:", segment.frame_rate)
    print("* Length:", segment.duration_seconds, "seconds")
    
    start = int(segment.duration_seconds / 3) * 1000
    end = start + duration * 1000
    
    print("Start:", start / 1000)
    print("End:", end / 1000)
    
    chunk = segment[start:end]
    return chunk

def printUsage():
    print("Usage : cut_data2 -i <input> -o <output> -d <duration>")

def main(argv):
    inputfile = ''
    outputfile = ''
    duration = 0
    
    commands = "hi:o:d:"
    full_commands = ["input=", "output=", "duration="]
    try:
        opts, args = getopt.getopt(argv, commands, full_commands)
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
        elif opt in ('-i', '--input'):
            inputfile = arg
        elif opt in ('-o', '--output'):
            outputfile = arg
        elif opt in ('-d', '--duration'):
            duration = int(arg)
        
    if inputfile == '' or outputfile == '' or duration == 0:
        printUsage()
        sys.exit(2)
        
    chunk = cut_file(inputfile, duration)    
    chunk.export(outputfile, format="wav")

if __name__ == "__main__":
    main(sys.argv[1:])
    