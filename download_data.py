# importing packages
from pytube import YouTube
from pytube import Playlist
import os
  
n=125
p = Playlist('https://www.youtube.com/playlist?list=PLmPB89JPdlhZ87vPCrpT0B7D9RHEiQrdV')
print(len(p.video_urls))
for url in p.video_urls[126:463]:
    
    # url input from user
    yt = YouTube(
        str(url))
      
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
      
    # check for destination to save file
    
    destination = "C:/Users/matte/Desktop/IA/HIP_HOP_MUSIC"
      
    # download the file
    out_file = video.download(output_path=destination)
      
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = "HIP_HOP_" + str(n) + '.wav'
    os.rename(out_file, destination+ "/" + new_file)
      
    # result of success
    print(new_file + " has been successfully downloaded.")
    n=n+1