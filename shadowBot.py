"""
ShadowBot.py
A simple Tkinter-based voice assistant with a typed-command fallback.

Users need to do:
    pip install speechrecognition pyttsx3 wikipedia pyjokes

                                                                        - K.Sohith
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import tkinter as tk
from threading import Thread


# 1) engine

listener = sr.Recognizer()       
engine = pyttsx3.init()         


# 2) speaking

def talk(text):
 
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)
    text_output.insert(tk.END, "Assistant: " + text + "\n")
    text_output.see(tk.END)



# 3) taking commands

def take_command():
   
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            text_output.insert(tk.END, "Listening...\n")
            text_output.see(tk.END)
            audio = listener.listen(source, timeout=5, phrase_time_limit=6)
            command = listener.recognize_google(audio)   # Uses Google API (internet required)
            command = command.lower()
            text_output.insert(tk.END, "You: " + command + "\n")
            text_output.see(tk.END)
            return command
    except sr.WaitTimeoutError:
        text_output.insert(tk.END, "Listening timed out. Try again.\n")
        text_output.see(tk.END)
        return ""
    except Exception as e:
        text_output.insert(tk.END, f"Could not understand (error: {e}).\n")
        text_output.see(tk.END)
        return ""



# 4) executing

def process_command(command):
  
    if not command:
        talk("I didn't catch anything. Try again.")
        return

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        talk("The time is " + now)

    elif "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        talk("Opening Google")
        webbrowser.open("https://google.com")

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        if topic:
            try:
                summary = wikipedia.summary(topic, sentences=1)
                talk(summary)
            except Exception as e:
                talk("Sorry, I couldn't find that on Wikipedia.")
                print("Wikipedia error:", e)
        else:
            talk("Please say 'wikipedia' followed by a topic.")

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "stop" in command or "exit" in command or "quit" in command:
        talk("Assistant shutting down. Goodbye!")
        root.destroy()

    else:
        talk("Sorry, I didn't get that. Try commands like 'time', 'open youtube', 'wikipedia <topic>', or 'joke'.")



# 5) GUI glich solving

def run_assistant():
    command = take_command()
    process_command(command)

def start_listening_thread():

    Thread(target=run_assistant, daemon=True).start()



# 6) typed commands

def handle_typed_command():

    cmd = type_entry.get().strip()
    if cmd:
        text_output.insert(tk.END, "You (typed): " + cmd + "\n")
        text_output.see(tk.END)
        type_entry.delete(0, tk.END)
        Thread(target=process_command, args=(cmd,), daemon=True).start()


# 7) Tkinter GUI setup

root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("520x460")

title = tk.Label(root, text="🎤 AI Voice Assistant", font=("Arial", 16, "bold"))
title.pack(pady=8)

text_output = tk.Text(root, height=18, width=62, wrap="word")
text_output.pack(padx=8)

controls_frame = tk.Frame(root)
controls_frame.pack(pady=6)

speak_btn = tk.Button(controls_frame, text="🎙 Speak (mic)", command=start_listening_thread, font=("Arial", 11))
speak_btn.grid(row=0, column=0, padx=6)

type_entry = tk.Entry(controls_frame, width=35, font=("Arial", 11))
type_entry.grid(row=0, column=1, padx=6)

send_btn = tk.Button(controls_frame, text="Send (type)", command=handle_typed_command, font=("Arial", 11))
send_btn.grid(row=0, column=2, padx=6)


# 8) greetings

def initial_greeting():
    talk("Hello, I am your assistant. Click Speak to start or type a command.")

Thread(target=initial_greeting, daemon=True).start()

root.mainloop()

