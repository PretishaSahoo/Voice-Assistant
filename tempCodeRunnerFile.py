import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary

recognizer = sr.Recognizer() 
engine = pyttsx3.init()

music = {
   "nadaniya" : "https://www.youtube.com/watch?v=gPpQNzQP6gE" , 
   "Tumhare hi rahenge" : "https://www.youtube.com/watch?v=cxKAtmvf-uM" , 
   "Khoobsurat" : "https://youtu.be/1-nnEM8chwo?si=aoOsdhOYaWO7NSoK"
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

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
        speak("playing")
        song = c.lower()[1:]
        speak(f"playing {song}")
        webbrowser.open(music[song])
    else:
        speak("I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2)
            word = recognizer.recognize_google(audio)
            print(word)
            if 'jarvis' in word.lower():
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis active and listening...")
                    audio = recognizer.listen(source, timeout=5)
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
