import os
import numpy as np
from pydub import AudioSegment

def main():
    inputdir="/PyWork/FromOutputToArray/Audio"
    outputdir="/PyWork/FromOutputToArray/OUT"
    with open("example.rttm") as file_hanler:
        #a=np.genfromtxt(fname="example.rttm",dtype="str")
        #start=a[:,3]
        #lenght=a[:,4]
        #spkr=a[:,7]
        #d=a[:,[3,4,7]] #assign the colums that we need
        #print(d)
        a=[]
        start1=[]
        duration=[]
        durations=list(map(int,duration))
        spkr=[]

        for i in file_hanler:
            a.append(i.split())

        for i in a:
            start1.append(float(i[3]))
            duration.append(float(i[4]))
            spkr.append(i[7])
        #print(a)
        #print(start1)
        #print(duration)
        #print(spkr)




        starts=[int(x*1000) for x in start1]

        durations=[int(y*1000) for y in duration]
        #print(starts)

        for filename in os.listdir(inputdir):
            save_file_name = filename[:-4]
            myaudio = AudioSegment.from_file(inputdir + "/" + filename, "wav")

            for i in range(len(starts)):
                chunk_data = myaudio[starts[i]:starts[i] + durations[i]]

            for z, chunk in enumerate(chunk_data):
                chunk_name = spkr[i] + "_" + save_file_name + "_{0}.wav".format(z)
                print(chunk_name)
                parts = chunk_name.split('_')
                a = parts[-1].split('.')
                b = a[0]
                if (len(b) == 1):
                    b = "0" + b
                chunk_name = parts[0] + "_" + parts[1] + "_" + b + ".wav"
                # print(chunk_name)
            # print
            # "exporting", chunk_name
            # chunk.export(outputdir + "/" + chunk_name, format="wav")

'''
    audio_file = "test.wav"
    audio = AudioSegment.from_wav(audio_file)
    #list_of_timestamps = [10, 20, 30, 40, 50, 60, 70, 80, 90]  # and so on in *seconds*

    start = ""
    for idx, t in enumerate(starts):
        # break loop if at last element of list
        if idx == len(start1):
            break

        end = starts[t] + durations[t]  # pydub works in millisec
        print
        "split at [ {}:{}] ms".format(start, end)
        audio_chunk = audio[start:end]
        audio_chunk.export("audio_chunk_{}.wav".format(end), format="wav")

        start = starts[t] # pydub works in millisec
'''
if __name__=="__main__":
    main()