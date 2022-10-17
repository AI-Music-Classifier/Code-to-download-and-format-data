from pydub import AudioSegment

#import wave
#w = wave.open('HIP_HOP_0.wav', 'r')
#print(w.getnframes())
#w.readframes()


  



destination = "C:/Users/matte/Desktop/IA/HIP_HOP_MUSIC/"
  
start = 100000
end = 110000
  

  
for i in range(209, 279):
    
    audio = AudioSegment.from_wav(destination+'HIP_HOP_'+str(i)+'.wav')
  
    chunk = audio[start:end]
    
    
    # Filename / Path to store the sliced audio
    if i<10:
        
        filename = '0_000'+str(i)+'.wav'
    elif i<100:
        
        filename ='0_00'+str(i)+'.wav'
    elif i<1000:
        
        filename ='0_0'+str(i)+'.wav'
    if(len(chunk)>= 150):
        
        chunk.export(destination +filename, format ="wav")

    
   