import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

recognizer = sr.Recognizer() 
engine = pyttsx3.init()

apiUrl = f'https://gnews.io/api/v4/top-headlines?&lang=en&country=us&apikey={NEWS_API_KEY}'


client = Groq(
    api_key=GROQ_API_KEY,
)


def groq_response(command):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": command
        }
    ],
        model="llama3-8b-8192",
    )
    speak(chat_completion.choices[0].message.content)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_news():
    try:
        r = requests.get(apiUrl)
        r.raise_for_status()  
        data = r.json()

        if 'articles' in data:
            articles = data['articles']
            if articles:
                speak("Here are the top headlines.")
                for i, article in enumerate(articles[:5]): 
                    speak(f"Headline {i + 1}: {article['title']}")
            else:
                speak("Sorry, I couldn't find any news articles at the moment.")
        else:
            speak("I couldn't retrieve the news right now, please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news due to a network issue.")


def processCommand(c):
    command = c.lower()
    if 'open google' in command:
        speak("Here you go to Google")
        webbrowser.open("https://google.com")

    elif 'open youtube' in command:
        speak("Here you go to Youtube")
        webbrowser.open("https://youtube.com")

    elif 'open linkedin' in command:
        speak("Here you go to Linkedin")
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower()[5:]
        speak(f"playing {song}")
        webbrowser.open(musicLibrary.music[song])

    elif "news" in c.lower():
       get_news() 

    else:
        groq_response(c)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio)
            print(word)
            if 'jarvis' in word.lower():
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis active and listening...")
                    audio = recognizer.listen(source, timeout=10)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
            if 'stop' in word.lower():
                speak("Shutting down")
                break 
        except sr.UnknownValueError:
            print("Can't understand, sorry!")
            speak("I couldn't understand what you said, could you please repeat?")
        except sr.RequestError:
            print("Could not request results, please check your internet connection.")
            speak("There was an issue with the network connection. Please check your internet.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")
