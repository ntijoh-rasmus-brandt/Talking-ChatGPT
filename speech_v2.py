import subprocess  # To kill windows media player
import speech_recognition as sr # Used to transform the spoken input to a string
import requests  # To send HTTP requests
from gtts import gTTS  # Googles text to speech library
import os  # To play the mp3 file


def audio_in():
    """
# Input:
    No input or arguments (only run)
# Output: 
    3 Possibles returns:

    Return 1: recognized_text - Recognized audio in text format

    Return 2: None - UnkownValueError

    Return 3: None - RequestError

# Functionality
Uses the speech_recognition library to record the users voice.
Then uses the google tts library to recognize audio and assign value to variable recognized_text
    """

    r = sr.Recognizer()

    with sr.Microphone() as source:
            print("Say something")
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print("Listening completed")
    try:
        recognized_text = r.recognize_google(audio)
        print("Recognized text: " + recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
        return None

def chatgpt_answer(prompt):
    """
    # Input: 
        Argument 1: prompt - prompt to send to ChatBot

    # Output:
        Return 1: generated_text - Text generated from ChatBot

    # Functionality:
        Establishes connection with OpenAI servers via requests library.
        Sends recognized_text as a prompt to ChatBot
        Recognizes response from ChatBot and assigns answer to variable generated_text

    """
     # Nyckeln för tillgång till ChatGPT
    api_key = "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"

        # The API endpoint for the GPT-2 model
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"

        # The headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # The data for the API request
    data = {
        "prompt": prompt,
        "max_tokens": 512
    }

        # Send the request to the API
    response = requests.post(url, headers=headers, json=data)

        # Get the generated text from the API response
    generated_text = response.json()["choices"][0]["text"]

    print("Generated text: " + generated_text)
    return generated_text


def text_to_speech(generated_text):
    """
    # Input:
        Argument 1: generated_text - Answer generated from ChatBot


    # Output:
        Return 1: generated_text.mp3 - Generated answer read by a Google assistant

    # Functionality:
        Creates variable tts which is assigned the value from "gTTS(generated_text)" a function
        from googles text to speech library that transforms text to speech, in this case
        the string "generated_text". It then proceeds to save the tts variable as an mp3 file.
        Atlast i plays the saved mp3.
      
    """

    tts = gTTS(generated_text)
    tts.save("generated_text.mp3")
    os.system("start generated_text.mp3")


def is_wmp_running():
        """
    # Input:
        No input or arguments (only run)


    # Output:
        Return 1: True - If wmplayer.exe is open
        Return 2: False - If wmplayer.exe is not open

    # Functionality:
        Creates a
      
    """
        tasklist = subprocess.check_output(['tasklist']).decode('utf-8')
        if 'wmplayer.exe' in tasklist:
            return True
        else:
            return False

    # Here is the main loop of the program which ends if you again == n.
while True:
    if is_wmp_running():
        subprocess.call("taskkill /IM wmplayer.exe /F", shell=True)

    recognized_text = audio_in()
    if recognized_text:
        generated_text = chatgpt_answer(recognized_text)
        text_to_speech(generated_text)

    again = input("Do you want to continue? (y/n)")
    if again == 'n':
        subprocess.call("taskkill /IM wmplayer.exe /F", shell=True)
        break