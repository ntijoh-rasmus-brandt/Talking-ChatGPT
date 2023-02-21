import subprocess #För windows media player
import speech_recognition as sr #Används för att förvanlda det muntliga till skriftlig text
import requests #Behövs för att skicka till ChatGPT/HTTP requests
from gtts import gTTS #Importerar google text to speech classen från gtts library
import os #Används för att spela upp svaret

api_key = "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" #Nyckeln för tillgång till ChatGPT

r = sr.Recognizer() #r är nu en recognizer class och kan göra "speech recognition" på ljud

while True:
    try:
        
        with sr.Microphone() as source:
            print("Say something")
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print("Listening completed")

        recognized_text = r.recognize_google(audio)
        print("Recognized text: " + recognized_text)
        if not recognized_text:
            print("No text recognized.")
            continue

        # The API endpoint for the GPT-2 model
        url = "https://api.openai.com/v1/engines/text-davinci-002/completions"

        # The headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # The data for the API request
        data = {
            "prompt": recognized_text,
            "max_tokens": 512 #En token ~4 engleska bokstäver
        }

        # Send the request to the API
        response = requests.post(url, headers=headers, json=data)

        # Get the generated text from the API response
        generated_text = response.json()["choices"][0]["text"]

        print("Generated text: " + generated_text)

        # subprocess.call("taskkill /IM wmplayer.exe /F", shell=True)
        # os.remove("generated_text.mp3")

        tts = gTTS(generated_text)
        tts.save("generated_text.mp3")
        os.system("start generated_text.mp3")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    again = input("Do you want to continue? (y/n)")
    if again == 'n':
        subprocess.call("taskkill /IM wmplayer.exe /F", shell=True)
        break
    
