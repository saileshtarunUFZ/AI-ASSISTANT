import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes

# Optional: Uncomment if you integrate OpenAI for ChatGPT
# import openai
# openai.api_key = "YOUR_OPENAI_API_KEY"

def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output error.")

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

# Example function to query ChatGPT if standard commands don't match
def ask_chatgpt(prompt):
    try:
        # Using OpenAI API
        client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return "I couldn't reach ChatGPT right now."

if __name__ == "__main__":
    wish_user()
    while True:
        query = take_command()

        if query == "none":
            continue

        # 1. Wikipedia Integration
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception as e:
                speak("I couldn't find anything on Wikipedia for that.")

        # 2. Website / Browser Integration
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")
            
        elif 'search for' in query:
            search_term = query.replace("search for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            speak(f"Here are the search results for {search_term}")

        # 3. Time & Utilities
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        # 4. Exit
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break
            
        # 5. Fallback to AI (ChatGPT/Gemini) if command isn't recognized locally
        else:
            speak("Let me check that for you...")
            # ai_response = ask_chatgpt(query)
            # speak(ai_response)
            speak("I heard: " + query)
