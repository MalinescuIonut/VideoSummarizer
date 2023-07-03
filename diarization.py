import re  # Import the regular expression module for pattern matching and string manipulation
from pydub import AudioSegment  # Import the AudioSegment class from pydub library for audio file manipulation
from pyannote.audio import Pipeline  # Import the Pipeline class from pyannote.audio library
import subprocess
import os
import shutil
from inaSpeechSegmenter import Segmenter

def millisec(timeStr):
    # Function to convert time string in format "HH:MM:SS.sss" to milliseconds
    spl = timeStr.split(":")  # Split the time string into hours, minutes, seconds, and milliseconds
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)  # Convert to milliseconds
    return s

######convert mkv input file to wav########
def convert_to_wav(input_file, output_file):
    subprocess.run(['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', output_file])

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    return float(result.stdout)

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
    max_speaker = '00'
    with open('diarizationoutput.txt', 'r') as content:
        for line in content:
            current_speaker = re.search(r'SPEAKER_(\d+)', line)
            if current_speaker:
                speaker_nr = current_speaker.group(1)
                if speaker_nr > max_speaker:
                    max_speaker = speaker_nr
    nr_of_speakers = int(max_speaker)
    print("there are: ", nr_of_speakers + 1, " speakers")

    origin_path = os.path.dirname(file_path)
    # print(origin_path)

    for speaker_index in range(0, nr_of_speakers + 1):

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
    for speaker_index in range(0, nr_of_speakers + 1):
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
    os.chdir(origin_path)
    wav_file = "audio.wav"
    convert_to_wav(file_path, wav_file)
    audio = AudioSegment.from_wav(wav_file)  # Load the audio file from the given path
    spacermilli = 10
    spacer = AudioSegment.silent(duration=spacermilli)

    for speaker_index in range(0, nr_of_speakers + 1):
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

    ########inaSpeech statistics#########
    for speaker_index in range(0, nr_of_speakers + 1):
        folder_name = f"SPEAKER_{speaker_index:02}"
        new_path = os.path.join(origin_path, folder_name)
        os.chdir(new_path)
        input_path = os.path.join(new_path, f"SPEAKER_audio_{speaker_index:02}.wav")
        print("SPEAKER_", speaker_index)

        seg = Segmenter()
        segmentation = seg(input_path)
        #result -> list = label (male/female/noEnergy), start time, end time of the segment
        #print(segmentation)

        #write results into a .txt file
        with open(f"SPEAKER_analysis_{speaker_index:02}.txt", "w") as file:
            for input_det in segmentation:
                label, start_time, end_time = input_det
                line = f"{label}: {start_time} --> {end_time}"
                file.write(line + '\n')


        #print results - optional
        #try:
        #    with open("myseg.txt", "r") as file:
        #        contents = file.read()
        #        print(contents)
        #except FileNotFoundError:
        #    print(f"File not found")
        #except Exception as e:
        #    print("Error reading file")

    #extracting statistics from dx.wav - contains all the spoken lines detected by the diarization process
    os.chdir(origin_path)
    input_path = os.path.join(origin_path, "audio.wav")
    seg = Segmenter()
    total_segmentation = seg(input_path)
    labels = []  # list defined for storing the labels

    with open("inaSpeech_results.txt", "w") as file:
        for input_det in total_segmentation:
            label, start_time, end_time = input_det
            line = f"{label}: {start_time} --> {end_time}"
            labels.append(label)
            file.write(line + '\n')

    # list -> dictionary => eliminates duplicates
    labels = dict.fromkeys(labels)
    for key in labels:
        labels[key] = 0

    with open("statistics.txt", 'w') as output:
        for current_label in labels:
            with open("inaSpeech_results.txt", 'r') as input:
                for line in input:
                    if current_label in line.strip("\n"):
                        start_time, end_time = tuple(re.findall(r'\d+\.\d*', line))
                        labels[current_label] += float(end_time) - float(start_time)
                percentage = (100*labels[current_label])/get_length("audio.wav")
                line = f"{current_label} --> screentime = {str(labels[current_label])} => {str(percentage)}%\n"
                output.write(line)
                print(current_label, " --> screentime = ", labels[current_label], " => ", percentage, "%")

    return

file_path = input("Enter the file path of the MKV file (include file name + extension): ")
name = "output"  # Prompt the user to enter the name for the diarized output

#DIARIZA(file_path, name)  # Call the DIARIZA function with the provided file path and name
separate_diarization(file_path)