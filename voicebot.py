import openai
import pyttsx3
import speech_recognition as sr
import pvporcupine
import struct
import pyaudio

from api_key import API_KEY

openai.api_key = API_KEY

print(pvporcupine.KEYWORDS)


engine = pyttsx3.init()
porcupine = None
pa = None
audio_stream = None

r= sr.Recognizer()
mic = sr.Microphone(device_index=0)


conversation = ""
user_name = "Joe"

#Paste Picovoice API Key Below
access_key = ""

porcupine = pvporcupine.create(access_key, keywords=["picovoice", "bumblebee"])

pa = pyaudio.PyAudio()

audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        print("Hotword Detected")

        from api_key import API_KEY

        while True:
            with mic as source:
                print("\nlistening... speak clearly into mic.")
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
            print("no longer listening.\n")

            try:
                user_input = r.recognize_google(audio)
            except:
                continue

            prompt = user_name + ": " + user_input + "\n Ethicai:"

            conversation += prompt

            response = openai.Completion.create(engine='text-davinci-002', prompt=conversation, max_tokens=100)
            response_str = response["choices"][0]["text"].replace("\n", "")
            response_str = response_str.split(user_name + ": ", 1)[0].split("Ethicai: ", 1)[0]


            conversation += response_str + "\n"
            print(response_str)

            engine.say(response_str)
            engine.runAndWait()

        porcupine.delete()