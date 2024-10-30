import webbrowser
import time
import os
import sys
import speech_recognition as sr
import pyautogui
import wikipedia
import pywhatkit
import psutil
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
from datetime import datetime
import json
import threading
import requests
import pyttsx3 as ptx3
from groq import Groq
import subprocess
import cv2
import mediapipe as mp
import time
import pyautogui
import math
import pyperclip
import pickle
from datetime import datetime
import feedparser
import random
from comtypes.client import CreateObject
import comtypes.gen.SpeechLib as SpeechLib


# for API configuration
global TURBO
TURBO = False

# GROQ_API="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"
# client = Groq(
#     api_key=(GROQ_API),
# )

models=["gemma-7b-it","mixtral-8x7b-32768"]

engine = ptx3.init()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Get the home directory
home_directory = os.path.expanduser("~")
# Construct the path to the Desktop
desktop_location = os.path.join(home_directory, "Desktop")

city_name = "Lucknow"
API_K='ed4cc0502e9e415825ea58832a79f3f3'

query = ""

# folder_name = "MyNewFolder"
file_name = "example.txt"
file_content = "This is an example text file.\nIt contains multiple lines.\nHello, World!"

#gesture control
run_program=False
# Global variable for sensitivity (1 to 7)
sensitivity = 2  # Default sensitivity level
# Map sensitivity levels to distance thresholds
sensitivity_thresholds = {
    1: 10,   # Very close
    2: 20,
    3: 30,   # Default
    4: 40,
    5: 50,
    6: 60,
    7: 70    # Further away
}

# The dictionary for search
MONTHS_DICT = {
    'january': '01',
    'jan': '01',
    'february': '02',
    'feb': '02',
    'march': '03',
    'mar': '03',
    'april': '04',
    'apr': '04',
    'may': '05',
    'june': '06',
    'jun': '06',
    'july': '07',
    'jul': '07',
    'august': '08',
    'aug': '08',
    'september': '09',
    'sep': '09',
    'october': '10',
    'oct': '10',
    'november': '11',
    'nov': '11',
    'december': '12',
    'dec': '12'
}

# capabilities 
capabilities = {
    "Wikipedia Search": "Can search for information on Wikipedia and summarize it.",
    "Current Time": "Provides the current time.",
    "Current Date": "Provides the current date.",
    "Current Date and Time": "Provides both the current date and time.",
    "Person Information": "Can search for information about a person on Wikipedia.",
    "File Search": "Searches for specific files based on user input.",
    "Open YouTube": "Opens the YouTube website.",
    "Open Google": "Opens the Google website.",
    "Google Search": "Performs a search on Google based on user input.",
    "Open Notepad": "Opens the Notepad application.",
    "Play Music": "Plays a specified song on YouTube.",
    "Learning Material Handling": "Can save and manage learning materials.",
    "Knowledge Base Management": "Can clear, search, and manage a knowledge base.",
    "Latest News Retrieval": "Provides the latest news updates.",
    "Screenshot Capture": "Takes and saves screenshots.",
    "Folder Creation": "Creates new folders.",
    "Weather Information": "Provides current weather information for a specified city.",
    "Scroll Command Handling": "Handles scrolling commands.",
    "Gesture Control": "Allows control of the system via gestures.",
    "File Creation": "Creates new files with specified content.",
    "Reminder Management": "Can set, check, and delete reminders.",
    "Volume Control": "Increases or decreases system volume.",
    "Brightness Control": "Increases or decreases screen brightness.",
    "CPU Usage Monitoring": "Provides current CPU usage statistics.",
    "Battery Status Monitoring": "Gives information about battery status.",
    "Network Control": "Can turn on airplane mode and manage Wi-Fi settings.",
    "Exit Command": "Exits the application.",
    "Turbo Mode Activation": "Activates a turbo mode for enhanced query handling.",
    "Knowledge Base Query Handling": "Searches a knowledge base for information related to user queries.",
    "Error Handling": "Manages exceptions and errors that may arise during operations."
}

# all key values.
trigger_keywords_dict = {
    "wikipedia": "Wikipedia Search",
    "time now": "Current Time",
    "date now": "Current Date",
    "current date and time": "Current Date and Time",
    "who is": "Person Information",
    "open youtube": "Open YouTube",
    "open google": "Open Google",
    "search google": "Google Search",
    "open notepad": "Open Notepad",
    "play": "Play Music",
    "create folder": "Folder Creation",
    "what weather current": "Weather Information",
    "how weather current": "Weather Information",
    "turn on scroll": "Scroll Command Handling",
    "wish me":"Greets the User as per the time",
    "create file": "File Creation",
    "set reminder": "Reminder Management",
    "can you learn":"Learn new things and respond accordingly.",
    "search knowledge":"Search specific knowledge base as stored",
    "check reminders": "Reminder Management",
    "show reminders": "Reminder Management",
    "delete reminder": "Reminder Management",
    "remove reminder": "Reminder Management",
    "increase volume": "Volume Control",
    "decrease volume": "Volume Control",
    "open gesture control": "to control tab with hand recognition gesture.",
    "increase brightness": "Brightness Control",
    "activate turbo mode":"To get Response from Groq AI API",
    "turn on turbo mode":"To get Response from Groq AI API",
    "activate turbo mode":"To get Response from Groq AI API",
    "decrease brightness": "Brightness Control",
    "cpu usage": "CPU Usage Monitoring",
    "battery status": "Battery Status Monitoring",
    "turn on airplane mode": "Network Control",
    "turn off wifi": "Network Control",
    "quit": "Exit Command",
    "exit": "Exit Command",
    "goodbye": "Exit Command"
}

# Initialize volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

keying = ["wikipedia","time now","date now","current date and time","who is","open youtube","open google","search","open notepad","play","create folder","what weather current","how weather current","scroll","create file","set reminder","check reminders","show reminders","delete reminder","remove reminder","increase volume","decrease volume","increase brightness","decrease brightness","cpu usage","battery status","turn on airplane mode","turn off wifi","quit","exit","goodbye"]
fix_key=f"Fix if spelling mistake in the query given \" {query} \" as with the trigering keys in this list [ {keying} ] . For ex wikipedia as wikiped or time as t ime or play as plays or create this as make this. Likewise phrases as per keying if sounds similiar but incomplete or broken in the query fix it. Give the response without any extra data , the response must be same as the query just with corrections if any there , if not return the same output as the query given. Also words with similiar meaning must be replaced with the exact word in the keying list. all the updates must be from the given list only , with no extra data in response.return the same query back if no keyword is there or no changes needed if return the same query back"

def GenerateGroq(prompt):
    # Modify the prompt to include an introduction
    introduction = "This is you 'You are a highly advanced AI assistant named Jarvis. " \
                    "You can perform various tasks, automation, gesture control, and more. " \
                    "Respond to the following prompt as if you are Jarvis: '"

    full_prompt = introduction + prompt

    completion = client.chat.completions.create(
        model=models[0],
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        temperature=1,
        max_tokens=1960,
        top_p=1,
        stream=False,
        stop=None,
    )
    # Collect the response
    answer = (completion.choices[0].message.content)
    return answer  # Return the full response instead of printing it

# comment the current speakPTX if want to use another one , uncomment that function 
def speakPTX(text, pitch=15, rate=1, volume=100):
    engine = CreateObject("SAPI.SpVoice")
    stream = CreateObject("SAPI.SpFileStream")
    engine.Voice = engine.GetVoices().Item(0)  # Male voice
    engine.Rate = rate  # -10 to 10
    engine.Volume = volume  # 0 to 100
    
    params = engine.GetAudioOutputs()
    engine.AudioOutput = params.Item(0)
    
    # Create a custom XML string to control pitch
    xml = f"""
    <pitch absmiddle="{pitch}">
    {text}
    </pitch>
    """
    engine.Speak(xml, 8)  # 8 is SVSFIsXML flag

# def speakPTX(text):
#     engine.say(text)
#     engine.runAndWait()

def speakPTXinput(text):
    engine.say(text)
    engine.runAndWait()
    queue=takeCommand()
    queue=queue.lower()
    return queue
    
def get_drive_names():
    try:
        # Run the command and capture the output
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], capture_output=True, text=True, check=True)
        
        # Split the output into lines and filter out empty lines
        drive_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # Remove the header if present
        if drive_names and drive_names[0] == "Name":
            drive_names.pop(0)

        return drive_names

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []
    
def get_weather(city_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']

        return {
            'description': weather_description,
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': humidity
        }
    else:
        print("Error:", response.status_code)
        return None  # Return None if there's an error

def continuous_scroll(amount):
    global scrolling
    while scrolling:  # Run while scrolling is True
        pyautogui.scroll(amount)
        time.sleep(0.5)  # Adjust the sleep duration as needed

def listen_for_stop_command():
    global scrolling
    while True:
        command = takeCommand()
        if "stop" in command:
            print("Stopping scrolling.")
            scrolling = False  # Set scrolling to False to stop scrolling
            speakPTX("Sure")
            return  # Exit the loop to stop scrolling

def handle_scroll_command():
    global scrolling
    speakPTX("Would you like to scroll upward or downward?")
    direction = takeCommand()
    
    if "upward" in direction:
        amount = 100  # Positive value for up
    elif "downward" in direction:
        amount = -100  # Negative value for down
    else:
        speakPTX("I didn't understand that. Please say upward or downward.")
        return

    speakPTX("You have 3 seconds to open the app. Say stop to to stop. Starting in...")
    for i in range(3, 0, -1):
        speakPTX(str(i))  # Countdown
        time.sleep(1)

    scrolling = True  # Start scrolling
    listener_thread = threading.Thread(target=listen_for_stop_command)
    listener_thread.start()
    
    # Start continuous scrolling
    continuous_scroll(amount)
    listener_thread.join()  # Wait for the listener thread to finish


'''
# also add in import lines <from gtts import gTTS>
def speakTTS(text):
    tts = gTTS(text=text, lang='en', slow=False)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    mixer.music.load(mp3_fp)
    mixer.music.play()
    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)
'''
        
def takeCommand(): 
    with sr.Microphone() as source: 
        print("Listening...") 
        recognizer.pause_threshold = 1 
        audio = recognizer.listen(source) 
    try: 
        print("Recognizing...") 
        query = recognizer.recognize_google(audio, language='en-in') 
        print(f"User  said: {query}\n") 
        if "quit" in query or "exit" in query or ("good" in query and "bye" in query): 
            print("Exiting...") 
            speakPTX("Nice with you buddy, Stay Connected.") 
            sys.exit() 
        else: 
            return query.lower() 
    except sr.UnknownValueError: 
        print("Could not understand audio") 
        speakPTX("Sorry, I didn't catch that. Please repeat.") 
        return "None" 
    except sr.RequestError as e: 
        print(f"Could not request results from Google Speech Recognition service; {e}") 
        speakPTX("I'm having trouble connecting to the speech recognition service. Please check your internet connection.") 
        return "None" 
    except Exception as e: 
        print(f"An unexpected error occurred: {e}") 
        speakPTX("An unexpected error occurred. Please try again.") 
        return "None"

def takeCommandNotes():
    query = ""  # Initialize an empty string to hold the commands
    with sr.Microphone() as source:
        print("Listening... (Say 'stop' to end)")
        recognizer.pause_threshold = 1
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)  # Set a timeout to avoid indefinite blocking
                print("Recognizing...")
                command = recognizer.recognize_google(audio, language='en-in')
                print(f"User  said: {command}\n")
                
                if "stop" in command.lower():  # Check if the user said "stop"
                    break  # Exit the loop if "stop" is detected
                
                query += command + " "  # Append the recognized command to the query
                
            except sr.WaitTimeoutError:
                # This exception is thrown if no audio is detected within the timeout period
                continue  # Continue listening
            except Exception as e:
                print("Say that again please...")
                continue  # Continue listening on errors

    return query.strip()  # Return the accumulated commands, removing any extra whitespace

def load_phi3_model():
    """Check if phi3 model is installed and load it if not"""
    try:
        # Check if phi3 is already installed
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get('models', [])
        if any(model.get('name') == 'phi3' for model in models):
            print("Phi3 model is already installed.")
            return True

        # If not installed, install it
        print("\nInstalling phi3 model... This might take a few minutes...")
        response = requests.post("http://localhost:11434/api/pull", 
                                 json={"name": "phi3"}, 
                                 stream=True)
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'status' in data:
                    print(f"\rStatus: {data['status']}", end='', flush=True)
                if 'completed' in data and data['completed']:
                    print("\nPhi3 model installation completed!")
                    return True
        return True
    except Exception as e:
        print(f"\nError loading phi3 model: {e}")
        return False

def chat_with_ollama(query, history=[]):
    """Send a query to the phi3 model and return the response"""
    url = "http://localhost:11434/api/chat"
    
    messages = history + [{"role": "user", "content": query}]
    data = {
        "model": "phi3",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'message' in result and 'content' in result['message']:
            response_content = result['message']['content']
            return response_content
        else:
            return "Error: Unexpected response format"
    except Exception as e:
        return f"Error: {str(e)}"

def open_notepad():
    os.system("notepad.exe")
    time.sleep(1)

def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder created or already exists at: {folder_path}")

def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"File created successfully at: {file_path}")

def Notepad():

    speakPTX("Tell Me The Query .")
    speakPTX("I Am Ready To Write .")

    writes = takeCommandNotes()

    time = datetime.now().strftime("%H:%M")

    filename = str(time).replace(":","-") + "-note.txt"

    with open(filename,"w") as file:

        file.write(writes)

    path_1 = ".\\" + str(filename)

    path_2 = ".\\" + str(filename)

    os.rename(path_1,path_2)

    os.startfile(path_2)

def set_reminder():
    speakPTX("Sure, I can help you set a reminder. What should I call this reminder?")
    reminder_key = takeCommand()
    speakPTX("What would you like me to remind you about?")
    reminder_text = takeCommand()
    
    try:
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reminders = {}
    reminders[reminder_key] = reminder_text
    try:
        with open('reminders.json', 'w') as f:
            json.dump(reminders, f, indent=4)
        speakPTX(f"Reminder '{reminder_key}' has been set.")
    except Exception as e:
        speakPTX(f"I'm sorry, I encountered an error while saving the reminder. The error was: {str(e)}")

def check_reminders():
    try:
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        speakPTX("No reminders found.")
        return

    if reminders:
        speakPTX("Here are your current reminders:")
        for key, reminder in reminders.items():
            speakPTX(f"{key}: {reminder}")
    else:
        speakPTX("You have no reminders set.")

def delete_reminder(reminder_key):
    try:
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
        if reminder_key in reminders:
            del reminders[reminder_key]
            with open('reminders.json', 'w') as f:
                json.dump(reminders, f, indent=4)
            speakPTX(f"Reminder '{reminder_key}' has been deleted.")
        else:
            speakPTX(f"No reminder found with the key '{reminder_key}'.")
    except FileNotFoundError:
        speakPTX("No reminders file found.")
    except json.JSONDecodeError:
        speakPTX("The reminders file is empty or corrupted.")

def CreationFolder(query):
    if ("create" in query or "make" in query or "generate" in query) and "folder" in query:
        speakPTX(f"Sure, I have permissions for {len(drives)} drives and your desktop to create a folder.")

        if len(drives) > 0:
            speakPTX("The available drives are:")
            for drive in drives:
                speakPTX(drive + " drive")
                print(drive, "drive")
        else:
            speakPTX("No drives available.")

        speakPTX("Where would you like to create the folder? You can say the drive name or 'desktop'.")
        InQuery = takeCommand().lower()
        print(f"User  said: {InQuery}")

        # Check if the user wants to create the folder on the desktop
        if "desktop" in InQuery:
            # InQuery=InQuery.replace("drive","")
            speakPTX("What would you like to name the folder?")
            FolderName=takeCommand()
            folderPath = os.path.join(InQuery + "\\\\", FolderName)  # Construct the path
            try:
                os.makedirs(folderPath, exist_ok=True)  # Create the folder
                speakPTX(f"Folder created on the desktop at {folderPath}.")
            except Exception as e:
                speakPTX(f"Failed to create folder on the desktop. Error: {str(e)}")

        # Check if the user wants to create the folder in one of the drives
        elif InQuery in drives:
            InQuery=InQuery.replace("drive","")
            speakPTX("What would you like to name the folder?")
            FolderName=takeCommand()
            folderPath = os.path.join(InQuery + "\\\\", FolderName)  # Construct the path
            try:
                os.makedirs(folderPath, exist_ok=True)  # Create the folder
                speakPTX(f"Folder created in {InQuery.upper()} drive at {folderPath}.")
            except Exception as e:
                speakPTX(f"Failed to create folder in {InQuery.upper()} drive. Error: {str(e)}")

        else:
            speakPTX("I didn't understand where you want to create the folder. Please specify a valid drive or 'desktop'.")

def wishMe():
    hour = datetime.now().hour
    if hour < 12:
        speakPTX("Good morning!")
    elif hour < 18:
        speakPTX("Good afternoon!")
    else:
        speakPTX("Good evening!")
    speakPTX("I am your personal assistant, Aistie. How may I assist you today?")

def take_screenshot():
    # Get the current date and time
    current_time = datetime.now()

    # Format the filename
    # This format is similar to "Screenshot 2023-11-22 at 15.30.45.png"
    filename = current_time.strftime("Screenshot %Y-%m-%d at %H.%M.%S.png")

    # Take the screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filepath = os.path.join(desktop_path, filename)
    screenshot.save(filepath)

    print(f"Screenshot saved as: {filepath}")
    
class HandTracking:
    def __init__(self, max_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=self.max_hands,
                                         min_detection_confidence=self.detection_confidence,
                                         min_tracking_confidence=self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        return frame

    def find_finger_tips(self, frame):
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            
            # Get coordinates for thumb tip, index base, and finger tips
            thumb_tip = hand_landmarks.landmark[4]
            index_base = hand_landmarks.landmark[5]
            finger_tips = [hand_landmarks.landmark[i] for i in [8, 12, 16, 20]]

            thumb_tip_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_base_coords = (int(index_base.x * w), int(index_base.y * h))
            finger_tip_coords = [(int(tip.x * w), int(tip.y * h)) for tip in finger_tips]

            # Calculate distance between thumb tip and index base
            thumb_index_distance = math.sqrt((thumb_tip_coords[0] - index_base_coords[0]) ** 2 + 
                                             (thumb_tip_coords[1] - index_base_coords[1]) ** 2)

            # Check if the tab-switching feature should be active
            if thumb_index_distance <= 18:
                index_middle_distance = math.sqrt((finger_tip_coords[0][0] - finger_tip_coords[1][0]) ** 2 + 
                                                  (finger_tip_coords[0][1] - finger_tip_coords[1][1]) ** 2)

                middle_ring_distance = math.sqrt((finger_tip_coords[1][0] - finger_tip_coords[2][0]) ** 2 + 
                                                 (finger_tip_coords[1][1] - finger_tip_coords[2][1]) ** 2)

                threshold = sensitivity_thresholds[sensitivity]

                if index_middle_distance < threshold:
                    time.sleep(0.99)
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    time.sleep(0.50)
                elif middle_ring_distance < threshold:
                    time.sleep(0.99)
                    pyautogui.hotkey('ctrl', 'tab')
                    time.sleep(0.50)
                
            # Draw circles and coordinates for visual feedback
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            for i, (x, y) in enumerate(finger_tip_coords):
                cv2.circle(frame, (x, y), 10, colors[i], cv2.FILLED)
                cv2.putText(frame, f'({x}, {y})', (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1)

            # Draw circle for thumb tip
            cv2.circle(frame, thumb_tip_coords, 10, (255, 0, 255), cv2.FILLED)
            cv2.putText(frame, f'Thumb: ({thumb_tip_coords[0]}, {thumb_tip_coords[1]})', 
                        (thumb_tip_coords[0] + 10, thumb_tip_coords[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

            # Draw circle for index base
            cv2.circle(frame, index_base_coords, 10, (0, 255, 255), cv2.FILLED)
            cv2.putText(frame, f'Index Base: ({index_base_coords[0]}, {index_base_coords[1]})', 
                        (index_base_coords[0] + 10, index_base_coords[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            # Display thumb-index distance
            cv2.putText(frame, f'Thumb-Index Distance: {int(thumb_index_distance)}', 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

# def recognize_speech(recognizer, microphone):
#     with microphone as source:
#         print("Listening...")
#         audio = recognizer.listen(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             print("You said:", text)
#             return text
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#             return None
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#             return None

# def speech_recognition_thread(recognizer, microphone):
#     # global run_program
#     while run_program:
#         recognize_speech(recognizer, microphone)

def Vision():
    global run_program
    cap = cv2.VideoCapture(0)
    detector = HandTracking()
    p_time = 0

    # Initialize speech recognition
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # # Start speech recognition in a separate thread
    # speech_thread = threading.Thread(target=speech_recognition_thread, args=(recognizer, microphone))
    # speech_thread.daemon = True
    # speech_thread.start()

    while run_program:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        frame = detector.find_hands(frame)
        frame = detector.find_finger_tips(frame)

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            run_program = False
            break

    cap.release()
    cv2.destroyAllWindows()

class KnowledgeBase:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def learn(self, original_info, ai_modified):
        entry = {
            'original': original_info,
            'ai_modified': ai_modified,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data.append(entry)
        self.save_data()
        return f"I've learned and stored this information.\nOriginal: {original_info}\nAI Modified: {ai_modified}"

    def recall(self, query):
        relevant_info = []
        for entry in self.data:
            if query.lower() in entry['original'].lower() or query.lower() in entry['ai_modified'].lower():
                relevant_info.append(f"Original: {entry['original']}\nAI Modified: {entry['ai_modified']}\nTimestamp: {entry['timestamp']}\n")
        
        if relevant_info:
            return "\n".join(relevant_info)
        else:
            return "I don't have any relevant information about that."

    def search_by_date(self, month, date=None):
        month = month.lower()
        month_code = MONTHS_DICT.get(month)
        if not month_code:
            return "Invalid month name"

        relevant_entries = []
        date_str = f"-{date}" if date else ""
        search_pattern = f"{month_code}{date_str}"

        for entry in self.data:
            entry_date = entry['timestamp'].split()[0]  # Get date part only
            entry_month = entry_date.split('-')[1]  # Get month part
            entry_day = entry_date.split('-')[2]  # Get day part
            
            if date:  # If specific date is provided
                if entry_month == month_code and entry_day == str(date).zfill(2):
                    return f"Original: {entry['original']}"
            else:  # If only month is provided
                if entry_month == month_code:
                    relevant_entries.append(entry['original'])

        if relevant_entries:
            if len(relevant_entries) > 1:
                return f"Found multiple entries for {month}. Here's the first one:\n{relevant_entries[0]}"
            return f"Original: {relevant_entries[0]}"
        
        return f"No entries found for the specified {'date' if date else 'month'}"

    def clear_all_data(self):
        self.data = []
        self.save_data()
        return "All stored data has been cleared."
    
    def delete_data_file(self):
        """Deletes the data file if it exists."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            return f"The data files has been deleted."
        else:
            return f"The data file does not exist."

def get_news():
    news_feeds = {
        'Technology': [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.wired.com/feed/rss",
            "https://feeds.feedburner.com/TheNextWeb"
        ],
        'Business': [
            "https://feeds.feedburner.com/entrepreneur/latest",
            "http://feeds.bbci.co.uk/news/business/rss.xml",
            "https://www.forbes.com/business/feed/"
        ]
    }

    news_items = []

    for category, feeds in news_feeds.items():
        random.shuffle(feeds)
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                entry = random.choice(feed.entries)
                news_items.append(f"{category}: {entry.title}")
                break
            except:
                continue

    return news_items
# Initialize the KnowledgeBase
kb = KnowledgeBase('jarvis_knowledge.pkl')
drives = get_drive_names()

def main():
    global TURBO
    global run_program
    while True:
        query = takeCommand()
        query = query.lower()
        if query == "None":
            continue
        else:
            try:
                if "wikipedia" in query:
                    speakPTX("Searching Wikipedia...")
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    print("According to Wikipedia, " + results)
                    speakPTX("According to Wikipedia, " + results)

                elif "time" in query or ("time" in query and "now" in query) or  ("time" in query and "current" in query):
                    current_time = datetime.now().strftime("%H:%M")
                    speakPTX(f"The current time is {current_time}")

                elif "date" in query and "today"in query or "today's" in query :
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    speakPTX(f"The current date is {current_date}")
                elif "wish"in query and "me" in query:
                    wishMe()
                elif "current date and time" in query or ("date and time" in query and "today" in query or "today's" in query):
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
                    speakPTX(f"The current date and time is {current_datetime}")

                elif "who is" in query:
                    person = query.replace("who is", "").strip()
                    try:
                        info = wikipedia.summary(person, sentences=2)
                        print(f"According to Wikipedia, {info}")
                        speakPTX(f"According to Wikipedia, {info}")
                    except wikipedia.exceptions.DisambiguationError:
                        print(f"There are multiple results for {person}. Please be more specific.")
                        speakPTX(f"There are multiple results for {person}. Please be more specific.")
                    except wikipedia.exceptions.PageError:
                        print(f"I couldn't find any information about {person}")
                        speakPTX(f"I couldn't find any information about {person}")
                
                # searching for files
                elif "find" in query:
                    query = query.replace("find", "")
                    namesearch=speakPTXinput("Sir. say only the file name please",)
                    searchquery = speakPTXinput("Sir , for text file say keyword the text , and image as png jpg or it's extension name only , same for videos. ")
                    if "the" in searchquery and "text" in searchquery:
                        speakPTX("Searching for text files...")
                        global typeExten
                        typeExten=f"{namesearch}.txt"
                    # Press the Windows key
                    pyautogui.press('win')
                    # Give the Start menu a moment to open
                    time.sleep(1.5)
                    # Type the search query
                    pyautogui.typewrite(f'Documents: {typeExten}', interval=0.1)
                    time.sleep(1.5+.5)
                    NewQuery=speakPTXinput("Sir i founnd these results. i can open the first one, or tell the number count to open, if many files")
                    checkResponse=GenerateGroq(f" \" {NewQuery} \" just return the number this query if no number is there return false , if numbers are there just return the numbers in integer only. No extra data should be included in the response either False or any number if there.")
                    if checkResponse is not False:
                        for i in range(15):
                            if str(i) == str(checkResponse):
                                for _ in range(int(i)):
                                    pyautogui.press('down')
                                    time.sleep(.9)  
                        pyautogui.press('enter')  
                    else:
                        speakPTX("Okay sir")
                    
                elif "open youtube" in query:
                    webbrowser.open_new("https://youtube.com")
                    speakPTX("Opening YouTube")

                elif "write" in query and "notepad" in query:
                    Notepad()
                
                elif "copied" in query or "copy" in query:
                    speakPTX("Sir please you want to copy something or paste something ? Or should i save your copied text to dot txt file.")
                    # Get the text from the clipboard
                    clipboard_text = pyperclip.paste()
                    print(clipboard_text)
                
                elif "turbo" in query and  "mode" in query and "is" in query and "active" in query:
                    if TURBO:
                        speakPTX("the Turbo mode is ACTIVE.")
                        print("TURBO Mode Status Active : ")
                    else:
                        speakPTX("the Turbo mode is TURNED Off")
                        print("TURBO Mode Status Inactive : ")
                
                elif "key" in query and ("values" in query or "value" in query):
                    speakPTX("Sure , i have printed all the triggering keys in the terminal followed.")
                    print("\t The left side is Trigering Keys to be in query and Right side followed with Feature name")
                    # Assuming trigger_keywords_dict is already defined
                    count = len(trigger_keywords_dict)  # Get the count of entries

                    print(f"Total number of trigger keywords: {count}\n")
                    for keyword, feature in trigger_keywords_dict.items():
                        print(f"Trigger Keyword: '{keyword}' -> Feature: '{feature}'")
                elif "open google" in query:
                    webbrowser.open_new("https://google.com")
                    speakPTX("Opening Google")

                elif "search" in query and "google" in query:
                    search_query = query.replace("search", "")
                    search_query = search_query.replace("google", "")
                    webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
                    speakPTX(f"Here are the search results for {search_query}")

                elif "open notepad" in query:
                    open_notepad()
                    speakPTX("Opening Notepad")
                    
                elif "text" in query and "to" in query and "speech"in query:
                    speakPTX("Sure sir enter your text in terminal.")
                    speech2text=input("The text : \n")
                    speakPTX("The text is.")
                    speakPTX(speech2text)
                elif "play" in query:
                    song = query.replace("play", "").strip()
                    speakPTX(f"Playing {song} on YouTube")
                    pywhatkit.playonyt(song)
                
                elif "learn" in query:
                    speakPTX("Sure sir just continue with the learning material with no extra data.")
                    save_brain = takeCommand()
                    ai_info = chat_with_ollama(f"This is the information to learn, remove the extra things, words which are not related, like 'learn this', etc. Respond with just the exact data to store for learning, without changing the meaning just the same text without any extra info and meaning change at all: \"{save_brain}\"")
                    responsekb = kb.learn(save_brain, ai_info)
                    speakPTX(responsekb)

                elif "clear knowledge" in query:
                    responsekb = kb.delete_data_file()
                    speakPTX(responsekb)

                elif "search knowledge" in query:
                    speakPTX("Please tell me the month name")
                    month = takeCommand().lower()

                    speakPTX("Please tell the date name. say No if none")
                    date_response = takeCommand()

                    if date_response==int:
                        # speakPTX("Please tell me the date")
                        try:
                            if 1 <= date_response <= 31:
                                response = kb.search_by_date(month, date_response)
                                speakPTX(response)
                            else:
                                speakPTX("Invalid date. Please provide a date between 1 and 31")
                        except ValueError:
                            speakPTX("Invalid date format")
                    else:
                        response = kb.search_by_date(month)
                        speakPTX(response)
                
                elif "news" in query and "latest" in query:
                    if __name__ == "__main__":
                        news = get_news()
                        news=GenerateGroq(f"You are talking to a friend , the friend asked for the latest news \" {news} \" update this para in conversational manner as per the scene you are into. No meaning chagen. and no extra data in response")
                        # for item in news:
                        #     print(item)
                        #     speakPTX(item)
                        print(news)
                        speakPTX(news)
                        
                elif "take" in query and ("screenshot" in query or "ss" in query):
                    take_screenshot()
                    speakPTX("Saved on desktop. Location on result.")
                    print("screenshot taken")

                elif ("create" in query or "make" in query or "generate" in query) and "folder" in query:
                    CreationFolder(query)

                elif ("weather" in query) and ("what" in query or "how" in query):
                    weather_data = get_weather(city_name, API_K)
                    if weather_data:
                        weather_info = f"Sir, the weather is {weather_data['description']} with temperature {weather_data['temperature']}°C, and humidity of {weather_data['humidity']}%, feels like nearly {weather_data['feels_like']}°C."
                        print(weather_info)
                        speakPTX(weather_info)

                elif "scroll" in query:
                    handle_scroll_command()
                    # continue
                
                elif "gesture" and "control" in query:
                    run_program = True  # Set to True only when gesture control is requested
                    speakPTX("Sure sir. For previous tab your index finger and middle finger should be close, for next tab middle finger and ring finger should be close. Control the sensitivity with variable in source. Starting in")
                    for i in range(1,4):
                        speakPTX(str(i))
                    Vision()  # Start gesture control
                    print("Gesture Control for tab switching")
                    print("\t Index Finger tip and Middle Finger tip close for previous tab")
                    print("\t Middle Finger tip and Ring Finger tip close for next tab")
                    run_program = False  # Reset to False when done

                elif "create file" in query:
                    folder_path = os.path.join(os.getcwd(), "new_folder")
                    file_path = os.path.join(folder_path, file_name)
                    create_file(file_path, file_content)
                    speakPTX(f"File created at {file_path}")

                elif "set reminder" in query or "set a reminder" in query:
                    set_reminder()

                elif "check reminders" in query or "show reminders" in query:
                    check_reminders()

                elif "delete reminder" in query or "remove reminder" in query:
                    speakPTX("Which reminder would you like to delete?")
                    reminder_key = takeCommand()
                    delete_reminder(reminder_key)

                elif "increase volume" in query:
                    current_volume = volume.GetMasterVolumeLevelScalar()
                    new_volume = min(1.0, current_volume + 0.1)
                    volume.SetMasterVolumeLevelScalar(new_volume, None)
                    speakPTX(f"Increased volume to {int(new_volume * 100)}%")

                elif "decrease volume" in query:
                    current_volume = volume.GetMasterVolumeLevelScalar()
                    new_volume = max(0.0, current_volume - 0.1)
                    volume.SetMasterVolumeLevelScalar(new_volume, None)
                    speakPTX(f"Decreased volume to {int(new_volume * 100)}%")

                elif "increase brightness" in query:
                    current_brightness = sbc.get_brightness()[0]
                    new_brightness = min(100, current_brightness + 10)
                    sbc.set_brightness(new_brightness)
                    speakPTX(f"Increased brightness to {new_brightness}%")

                elif "decrease brightness" in query:
                    current_brightness = sbc.get_brightness()[0]
                    new_brightness = max(0, current_brightness - 10)
                    sbc.set_brightness(new_brightness)
                    speakPTX(f"Decreased brightness to {new_brightness}%")

                elif "cpu usage" in query:
                    cpu_usage = psutil.cpu_percent(interval=1)
                    speakPTX(f"The current CPU usage is {cpu_usage}%")

                elif "battery status" in query:
                    battery = psutil.sensors_battery()
                    if battery:
                        percent = battery.percent
                        is_plugged = battery.power_plugged
                        status = "plugged in" if is_plugged else "not plugged in"
                        speakPTX(f"The battery is at {percent}% and is {status}.")
                    else:
                        speakPTX("Unable to retrieve battery status.")

                elif "turn on airplane mode" in query:
                    os.system("start ms-settings:network-airplanemode")
                    speakPTX("Opening Airplane mode settings.")

                elif "turn off" in query and ("wi"in query and "fi" in query):
                    os.system("netsh wlan set hostednetwork mode=disallow")
                    speakPTX("Wi-Fi has been turned off.")

                elif "quit" in query or "exit" in query or "goodbye" in query:
                    print("Exiting...")
                    speakPTX("NIce with you buddy,Stay Connected.")
                    sys.exit()
                    
                elif "turbo" in query and ("turn" in query or "activate" in query) and ("on" in query or "enable" in query) and "mode" in query:
                    global TURBO
                    TURBO = True
                    speakPTX("Turbo Mode Activated now")
                    print("TURBO Mode Status Online :")
                # If none of the above conditions are met, check the knowledge base
                else:
                    # First, get all original info from the database with count
                    print("DEBUG: Entering else block - searching knowledge base")
                    # Search the knowledge base
                    all_originals = [entry['original'] for entry in kb.data]
                    database_info = f"Total entries: {len(all_originals)}\nEntries: {' | '.join(all_originals)}"
                    if len(all_originals) != 0:
                        print(f"DEBUG: Database info: {database_info}")
                        
                        prompt = f"""
                        Query: "{query}"
                        Database: "{database_info}"
                        
                        Instructions:
                        1. Answer the query using only the information from the database.
                        2. If there's no related information, respond with "false".
                        3. Provide a concise, friendly answer without any extra information or data.
                        4. Do not include phrases like "Answer:" or "True" in your response.
                        5. Remove any asterisks (*) from your response.
                        Mandatory Intstruction = If there's no fit answer for the query from database just result false with no extra data included just false as response.
                        Again repeating no text , no extra data , no words except false in response if the query cant be answered.
                        """
                        
                        print("DEBUG: Generating Groq response")
                        response = GenerateGroq(prompt)
                        print(f"DEBUG: Raw Groq response: {response}")
                        
                        # Clean up the response
                        response = response.replace("Answer:", "").replace("True", "").replace("*", "").strip()
                        print(f"DEBUG: Cleaned response: {response}")
                        
                        if "false" in response.lower() :
                            print("DEBUG: No information found in knowledge base, considering Turbo mode")
                            if TURBO:
                                try:
                                    # turbo_query=speakPTXinput("The TURBO mode is not active should i activate it?")
                                    # print("The TURBO mode is not active should i activate it?")
                                    # if "no" not in turbo_query:
                                    # print("DEBUG: Turbo mode active, generating response")
                                    # turbo_response = GenerateGroq(query)
                                    # print(f"DEBUG: Turbo response: {turbo_response}")
                                    # speakPTX(turbo_response)
                                    # speakPTX("Ok Sir.")
                                    print("No data found in database.")
                                    speakPTX("Activate the TURBO Mode for more reponses please.")
                                    print("TURBO Status OFFLINE")
                                    continue
                                except Exception as e:
                                    # print(f"DEBUG: Error in Turbo mode: {e}")
                                    speakPTX("Sir, please check your API or internet connection for Turbo Mode features.")
                            else:
                                    # turbo_query=speakPTXinput("The TURBO mode is not active should i activate it?")
                                    # print("The TURBO mode is not active should i activate it?")
                                    # if "no" not in turbo_query:
                                        print("DEBUG: Turbo mode active, generating response")
                                        turbo_response = GenerateGroq(query)
                                        print(f"DEBUG: Turbo response: {turbo_response}")
                                        speakPTX(turbo_response)
                                        speakPTX(turbo_response)
                        else:
                            print(f"DEBUG: Valid response from knowledge base: {response}")
                            speakPTX(response)
                    else:
                        print("DEBUG: Turbo mode inactive, asking for activation")
                        activate_turbo = speakPTXinput("Turbo mode is required for this query. Should i active the TURBO Mode").lower()
                        if activate_turbo in ["yes", "y"]:
                            TURBO = True
                            try:
                                print("DEBUG: Activating Turbo mode and generating response")
                                turbo_response = GenerateGroq(query)
                                print(f"DEBUG: Turbo response: {turbo_response}")
                                speakPTX(turbo_response)
                            except Exception as e:
                                print(f"DEBUG: Error in Turbo mode: {e}")
                                speakPTX("Failed to generate response in Turbo mode.")
                        else:
                            speakPTX("Okay no issues")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    # print(get_drive_names())
    print("Want to use developer's API or use your own GROQ api. \n Type Y for your API and D for developer's api use.")
    api_resp=input("Response = ")
    if api_resp.lower() == 'y':
        print("Please enter your API key")
        api_user=input("Enter your API Key = ")
        GROQ_API=api_user
        client = Groq(
        api_key=(GROQ_API),)
    else:
        GROQ_API="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"
        client = Groq(
        api_key=(GROQ_API),)
        print("Using Developer's default API")
    main()