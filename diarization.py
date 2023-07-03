import re  # Import the regular expression module for pattern matching and string manipulation
from pydub import AudioSegment  # Import the AudioSegment class from pydub library for audio file manipulation
from pyannote.audio import Pipeline  # Import the Pipeline class from pyannote.audio library
import subprocess
import os
import shutil
from inaSpeechSegmenter import Segmenter
from inaSpeechSegmenter.export_funcs import seg2csv
import pandas as pd
import seaborn as sns

def millisec(timeStr):
    # Function to convert time string in format "HH:MM:SS.sss" to milliseconds
    spl = timeStr.split(":")  # Split the time string into hours, minutes, seconds, and milliseconds
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)  # Convert to milliseconds
    return s

######convert mkv input file to wav########
def convert_to_wav(input_file, output_file):
    subprocess.run(['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', output_file])


#######generate a wav file for each speaker###########
#def generate_speaker_files(dz_file, audio_file):
#    dz = open(dz_file).read().splitlines()
#    speaker_files = {}  #dictionary to store speaker files

#    for l in dz:
#        #[ 00:00:01.172 -->  00:00:02.235] P SPEAKER_02 - a line from the txt file
#        start, end, speaker = re.findall(r"(\d+:\d+:\d+\.\d+) --> (\d+:\d+:\d+\.\d+).*?(\w+)", l)[0]
#        start_ms = millisec(start)
#        end_ms = millisec(end)
#        speaker = speaker.upper()
#        speaker_label = "SPEAKER_" + speaker
#
#        if speaker_label not in speaker_files:
#            speaker_files[speaker_label] = AudioSegment.silent()
#
#        speaker_files[speaker_label] += audio_file[start_ms:end_ms]
#
#    for speaker_label, audio_segment in speaker_files.items():
#        output_file = f"dz_{speaker_label}.wav"
#        audio_segment.export(output_file, format="wav")

def DIARIZA(file_path, name):
    # Function to perform diarization on an audio file
    t1 = 0 * 1000  # Start time of audio segment in milliseconds (here, 0 seconds)
    t2 = 20 * 60 * 1000  # End time of audio segment in milliseconds (here, 20 minutes)

    wav_file = "audio.wav"
    convert_to_wav(file_path, wav_file)

    newAudio = AudioSegment.from_wav(wav_file)  # Load the audio file from the given path
    a = newAudio[t1:t2]  # Extract the audio segment from t1 to t2
    a.export(wav_file, format="wav")  # Export the audio segment as a WAV file with the name "audio.wav"

    # Initialize the speaker diarization pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                        use_auth_token="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")

    DEMO_FILE = {"uri": "blabal", "audio": wav_file}  # Define the input file information for diarization
    dz = pipeline(DEMO_FILE)  # Perform speaker diarization on the input file
    print(*list(dz.itertracks(yield_label=True))[:10], sep="\n")  # Print the first 10 diarization labels

    with open("diarization" + name + ".txt", "w") as text_file:
        text_file.write(str(dz))  # Write the diarization result to a text file with the given name

    spacermilli = 10  # Duration of silent spacer in milliseconds
    spacer = AudioSegment.silent(duration=spacermilli)  # Generate a silent spacer segment

    dz = open("diarization" + name + ".txt").read().splitlines()  # Read the diarization text file
    dzList = []
    for l in dz:
        start, end = tuple(re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=l))  # Extract start and end times from each line
        start = millisec(start) - spacermilli  # Convert start time to milliseconds and subtract spacer duration
        end = millisec(end) - spacermilli  # Convert end time to milliseconds and subtract spacer duration
        lex = not re.findall("SPEAKER_01", string=l)  # Check if the line does not contain "SPEAKER_01"
        dzList.append([start, end, lex])  # Add the start time, end time, and lex (True/False) to the list

    print(*dzList[:10], sep='\n')  # Print the first

    # Print the first 10 items in dzList (start time, end time, and lex)
    print(*dzList[:10], sep='\n')

    sounds = spacer  # Initialize sounds with the spacer segment
    segments = []  # Initialize segments list

    dz = open("diarization" + name + ".txt").read().splitlines()  # Read the diarization text file again
    for l in dz:
        start, end = tuple(re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=l))  # Extract start and end times from each line
        start = int(millisec(start))  # Convert start time to milliseconds
        end = int(millisec(end))  # Convert end time to milliseconds

        segments.append(len(sounds))  # Add the length of sounds to segments list
        sounds = sounds.append(newAudio[start:end], crossfade=0)  # Append the audio segment to sounds without crossfade
        sounds = sounds.append(spacer, crossfade=0)  # Append the spacer segment to sounds without crossfade

    sounds.export("dz.wav", format="wav")  # Export the combined audio segments as a WAV file with the name "dz.wav"

    print(segments[:8])  # Print the first 8 items in the segments list

    return

def separate_diarization(file_path):

    dz1 = open("diarization" + name + ".txt").read().splitlines()
    global nr_of_speakers
    nr_of_speakers = 0
    for l in dz1:
        nr_of_speakers = max(nr_of_speakers, int(l[-2:]))  # slices the last 2 characters from that line

    nr_of_speakers = nr_of_speakers + 1  # Speaker counting starts from 0
    print("Nr of speakers: "+str(nr_of_speakers))

    origin_path = os.path.dirname(file_path)
    # print(origin_path)

    for speaker_index in range(0, nr_of_speakers):

        # step1: make folders for each speaker
        folder_name = f"SPEAKER_{speaker_index:02}"  # Format folder name with leading zeros
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # step2: copy the diarizationoutput.txt in each folder
        new_path = os.path.join(origin_path, folder_name)
        os.makedirs(new_path, exist_ok=True)
        current_path = os.path.join(new_path, "diarizationoutput.txt")
        shutil.copyfile("diarizationoutput.txt", current_path)

    # step3: eliminate all lines that don't contain information about current speaker
    for speaker_index in range(0, nr_of_speakers):
        folder_name = f"SPEAKER_{speaker_index:02}"
        new_path = os.path.join(origin_path, folder_name)
        os.chdir(new_path)

        current_speaker = f"SPEAKER_{speaker_index:02}"
        with open("diarizationoutput.txt", 'r') as input:
            with open("temp.txt", 'w') as output:
                for line in input:
                    if current_speaker in line.strip("\n"):
                        output.write(line)
        os.replace("temp.txt", "diarizationoutput.txt")

    #step4: for each diarizationoutput.txt copied, scrape the original video
    # and combine only the voice segments specified in the correponding txt
    os.chdir(origin_path) # change working directory
    wav_file = "audio.wav"
    convert_to_wav(file_path, wav_file)
    audio = AudioSegment.from_wav(wav_file)  # Load the audio file from the given path
    spacermilli = 10
    spacer = AudioSegment.silent(duration=spacermilli)

    for speaker_index in range(0, nr_of_speakers):
        folder_name = f"SPEAKER_{speaker_index:02}"
        new_path = os.path.join(origin_path, folder_name)
        os.chdir(new_path)

        sounds = spacer  # Initialize sounds with the spacer segment
        segments = []  # Initialize segments list
        dz = open("diarizationoutput.txt").read().splitlines()
        for l in dz:
            start, end = tuple(re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=l))  # Extract start and end times from each line
            start = int(millisec(start))  # Convert start time to milliseconds
            end = int(millisec(end))  # Convert end time to milliseconds

            segments.append(len(sounds))  # Add the length of sounds to segments list
            os.chdir(origin_path)
            sounds = sounds.append(audio[start:end], crossfade=0)  # Append the audio segment to sounds without crossfade
            sounds = sounds.append(spacer, crossfade=0)  # Append the spacer segment to sounds without crossfade

        sounds.export(f"SPEAKER_audio_{speaker_index:02}.wav", format="wav")  # Export the combined audio segments as a WAV file with the name "dz.wav"

        # final step: move the .wav files in each folder correspondingly
        new_path = os.path.join(origin_path, folder_name)
        os.makedirs(new_path, exist_ok=True)
        current_path = os.path.join(new_path, f"SPEAKER_audio_{speaker_index:02}.wav")
        shutil.move(f"SPEAKER_audio_{speaker_index:02}.wav", current_path)

    return

#not used - cannot install the library
def INA_Speech_Voice(file_path):

    origin_path = os.path.dirname(file_path)

    for l in range(int(nr_of_speakers)):
        if l < 10:
            new_path = origin_path + f"\SPEAKER_0{str(l)}"
            os.chdir(new_path)  # change working directory
            # print(new_path)
            new_path = os.path.join(new_path, f"SPEAKER_audio_0{str(l)}.wav")
            # print(new_path)
        else:
            new_path = origin_path + f"\SPEAKER_{str(l)}"
            os.chdir(new_path)  # change working directory
            new_path = os.path.join(new_path, f"SPEAKER_audio_{str(l)}.wav")

    v = VoiceFemininityScoring(gd_model_criteria="bgc") # Multi layer perceptron trained on all data giving best BGC
    vf_score, speech_detected, nb_retained_vectors = v(new_path)
    with open(file_path + "\\INA_Speech_Results.txt", 'a') as file: #create file if it doesn't exist or append to it
        file.write("Speaker " +str(l) +" Femininity:  %.9f"  % vf_score +"\n")
    return


def speakerStatistics(file_path):

    origin_path = os.path.dirname(file_path)

    audio = AudioSegment.from_file(origin_path + "\\audio.wav")# Load the audio file
    duration_ms = len(audio)# Calculate the duration in milliseconds
    # print(f"The audio file duration is {duration_ms} milliseconds.")

    audio1 = AudioSegment.from_file(origin_path + "\\dz.wav")  # Load the audio file
    duration_totalSpekaing_ms = len(audio1)  # Calculate the duration in milliseconds

    # INA Segmenter
    seg = Segmenter()
    segmentationList = []


    with open(origin_path + "\General_Statistics.txt", 'w') as file:
        file.write("Kingdom of Heaven - Movie Sequence\n")
    for l in range(int(nr_of_speakers)):
        if l < 10:
            new_path = origin_path + f"\SPEAKER_0{str(l)}"
            os.chdir(new_path)  # change working directory
            # print(new_path)
            new_path = os.path.join(new_path, f"SPEAKER_audio_0{str(l)}.wav")
            # print(new_path)
        else:
            new_path = origin_path + f"\SPEAKER_{str(l)}"
            os.chdir(new_path)  # change working directory
            new_path = os.path.join(new_path, f"SPEAKER_audio_{str(l)}.wav")

        audio2 = AudioSegment.from_file(new_path)  # Load the audio file
        duration_speaker_ms = len(audio2)  # Calculate the duration in milliseconds


        segmentation = seg(new_path)
        segmentationList.extend(segmentation)
        tuple_segmentation = tuple(segmentation)

        with open(origin_path + "\General_Statistics.txt", 'a') as file: #create file if it doesn't exist or append to it
           file.write("Speaker " +str(l) +" Total Speaking Percentage: %.4f"  %(duration_speaker_ms/duration_totalSpekaing_ms *100) +"%\t")
           file.write("Speaker " + str(l) + " Total Speaking Time: " +str(duration_speaker_ms)  + "(ms)\t")
           for item in tuple_segmentation:
               file.write(f"{item}\t")
           file.write("\n")


    # calculating procentages of each gender speaking  + noise

    # time periods for different categories
    male_per = 0
    female_per = 0
    noise_per = 0
    music_per = 0
    noEnergy_per = 0

    print(segmentationList)

    for l in range(len(segmentationList)):
        print(len(segmentationList))
        field1 = segmentationList[l][0] # 0 - acceses the first field
        time = segmentationList[l][2] - segmentationList[l][1]
        print(len(segmentationList))
        # tuple_segmentation = (('type', start of the segment, end of the segment)...
        if field1 == 'male':
            male_per = male_per + time
        elif field1 == 'female':
            female_per = female_per + time
        elif field1 == 'noise':
            noise_per = noise_per + time
        elif field1 == 'music':
            music_per = music_per + time
        elif field1 == 'noEnergy':
            noEnergy_per = noEnergy_per + time


    with open(origin_path + "\General_Statistics.txt", 'a') as file:  # create file if it doesn't exist or append to it
      file.write("Total Speaking Percentage: %.5f" %(duration_totalSpekaing_ms/duration_ms * 100) +"%\t")
      file.write("Total Speaking Duration: " + str(duration_totalSpekaing_ms) + "(ms)\t")
      file.write("Total Duration of the Sample: " + str(duration_ms) + "(ms)\n")

      file.write("Male Speaking Duration: %.3f"  %(male_per) + "(s)\t" +"Percentage: %.5f" %(male_per*1000/duration_totalSpekaing_ms *100) +"%\n")
      file.write("Female Speaking Duration: %.3f"  %(female_per) + "(s)\t" +"Percentage: %.5f" %(female_per*1000/duration_totalSpekaing_ms *100) +"%\n")
      file.write("Noise Duration: %.3f" %(noise_per) + "(s)\t\t" +"Percentage: %.5f" %(noise_per*1000/duration_totalSpekaing_ms *100) +"%\n")
      file.write("Music Duration: %.3f" %(music_per) + "(s)\t\t" +"Percentage: %.5f" %(music_per*1000/duration_totalSpekaing_ms *100) +"%\n")
      file.write("NoEnergy Duration: %.3f" %(noEnergy_per) + "(s)\t\t" + "Percentage: %.5f" % (noEnergy_per*1000/ duration_totalSpekaing_ms * 100) + "%\n")
    return


file_path = input("Enter the file path of the MKV file: ")
name = "output"  # Prompt the user to enter the name for the diarized output

# DIARIZA(file_path, name)  # Call the DIARIZA function with the provided file path and name
separate_diarization(file_path)

#INA_Speech_Voice(file_path)

speakerStatistics(file_path)