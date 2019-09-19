filepath = "./audio_wav/"
output = r'./audio_wav_out/'
OUTPUTFILE = r'./output_text/outputfile.csv'

from pydub import AudioSegment
import speech_recognition as sr
import io
import os
import wave
import csv


def rttm_to_dictionary():

    with open("example.rttm") as file_handler:

        a=[]
        d = {}


        for i in file_handler:
            a.append(i.split())

        for line in a:
            if line[7] in d:
                 #append the new number to the existing array at this slot
                #d[line[7]].append(float(line[3]))
                #d[line[7]].append(float(line[4]))
                d[line[7]].append([float(line[3]), float(line[4])])
            else:
                # create a new array in this slot
                d[line[7]] = [[float(line[3]),float(line[4])]]

        #print(f"{d}")
    audio_file = "3054300.wav"
    audio = AudioSegment.from_wav(audio_file)

    for speaker in d.keys():
        #print(f"{speaker}")
        list_of_timestamps = d[speaker]

        for sss, t in list_of_timestamps:
           # print(f"{sss} , {t}")
            start = sss * 1000 # pydub works in millisec
            duration = t*1000 # pydub works in millisec
            end = start + duration
           # print("split at [ {}:{}] ms".format(start, end))
            audio_chunk = audio[start:end]

            audio_chunk.export(f"./audio_wav_out/audio_chunk_{start}_{end}_{speaker}.wav".format(end), format="wav")

    """
    audio1 = os.fsencode(output)
    for chunk in os.listdir(audio1):
        filename=os.fsencode(chunk)
        #if chunk.endswith(".wav"):

        with sr.AudioFile(filename) as source:
            chunk12 = r.record(source)
        try:
            text = r.recognize_google(chunk12)
            print(text)
        except Exception as e:
            print(e)
    """

    return d

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def changer(audio_file_name):
    file_name = filepath + audio_file_name
   # mp3_to_wav(file_name)

    # The name of the audio file to transcribe

    frame_rate, channels = frame_rate_channel(file_name)

    if channels > 1:
        stereo_to_mono(file_name)



def get_file_paths(dirname):
    file_paths = []
    for root, directories, files in os.walk(dirname):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def process_file(file):
    r = sr.Recognizer()
    a = ''
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =  r.recognize_google(audio)
        except sr.UnknownValueError:
            a = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Google Speech Recognition service; {0}".format(e)
    return a

def main():
    rttm_to_dictionary()
    files = get_file_paths(output)                 # get all file-paths of all files in dirname and subdirectories
    for file in files:                              # execute for each file
        (filepath, ext) = os.path.splitext(file)    # get the file extension
        file_name = os.path.basename(file)          # get the basename for writing to output file
        if ext == '.wav':                           # only interested if extension is '.wav'
            a = process_file(file)                  # result is returned to a
            with open(OUTPUTFILE, 'a') as f:        # write results to file
                writer = csv.writer(f)
                writer.writerow(['file_name','google'])
                writer.writerow([file_name, a])

if __name__=="__main__":
   # for audio_file_name in os.listdir(filepath):
   #     change = changer(audio_file_name)
   # rttm_to_dictionary()
   main()
