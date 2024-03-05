import os
import httpx
import random
import logging
import customtkinter
from datetime import datetime
from async_tkinter_loop import async_handler

from source.intent_classification import IntentClassifier
from source.gui import root, insert_assistant_message, send_button_event


intent_classifier = IntentClassifier()

OPENWEATHER_APP_ID = "1ab13fe5b44890da6d1664caf8ec291b"


class Assistant:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_user_intent(user_message):
        user_intent = intent_classifier.predict(user_message)
        logging.info(f"USER MSG - user's msg: {user_message}")
        logging.info(f"INTENT - user's intent: {user_intent}")
        return user_intent

    @staticmethod
    def decide_action(user_message, user_intent, kernel):
        if user_intent == 'weather':
            get_weather_report()
        elif user_intent == "leaving":
            return kernel.respond(user_message)
        elif user_intent == "findip":
            find_my_ip()
        elif user_intent == "horoscope":
            return fortune_cookie()
        elif user_intent == "discord":
            return open_discord()
        elif user_intent == "gimp":
            return open_gimp()
        elif user_intent == "xed":
            return open_notepad()
        elif user_intent == "music":
            answer_play_music(user_message)
            return "I like that. Maybe one more time?"
        elif user_intent == "movie":
            answer_play_video(user_message)
            return "Is that a movie or series?"
        elif user_intent == "signal":
            open_signal()
            return "BEEP BOP!"
        elif user_intent == "joke":
            return kernel.respond(user_message)
        elif user_intent == "terminal":
            return open_terminal()
        else:
            return kernel.respond(user_message)


def greet_user():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        msg = "Good morning, Viktoria! What's up?"
    elif (hour >= 12) and (hour < 16):
        msg = "Hello there, Viktoria! Still working, huh?"
    elif (hour >= 16) and (hour < 19):
        msg = "Good evening, Viktoria. Nice to see you there!"

    return msg


@async_handler
async def find_my_ip():
    logging.info("ODER - run get request: 'https://api64.ipify.org?format=json'")
    insert_assistant_message("Give me a second, I need to check that...", "LULA")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api64.ipify.org?format=json")
        ip_address_dict = response.json()
        ip_address = ip_address_dict["ip"]
    logging.info(f"ORDER - response: {ip_address}")
    insert_assistant_message(f"Well, your IP Address is: {ip_address}", "LULA")


@async_handler
async def get_weather_report():
    logging.info("ORDER - run get request: 'http://api.openweathermap.org/data/2.5/weather?q=3081368'")
    insert_assistant_message("Hmmm... I need to check that.", "LULA")
    insert_assistant_message("As I remember, your city is Wrocław, right?", "LULA")
    insert_assistant_message("In a few seconds I will have a special forecast just for you... :)", "LULA")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api.openweathermap.org/data/2.5/weather?lat=51&lon=17&appid={OPENWEATHER_APP_ID}&units=metric")
        response_dict = response.json()
        logging.info(f"ORDER - response: {response_dict}")
        weather = response_dict["weather"][0]["description"]
        temperature = response_dict["main"]["temp"]
        max_temp = response_dict["main"]["temp_max"]
        min_temp = response_dict["main"]["temp_min"]
        feels_like = response_dict["main"]["feels_like"]
        insert_assistant_message(f"Here is your weather report - the current temperature is {temperature}C, but it feels like {feels_like}C.", "LULA")
        insert_assistant_message(f"The maximal temperature is {max_temp}C, and the minimal is {min_temp}C.", "LULA")
        insert_assistant_message(f"Also, the weather report talks about {weather}.", "LULA")
        insert_assistant_message("I hope you will not be upset now!", "LULA")
        insert_assistant_message("Every weather is a nice weather, I think.", "LULA")


def open_discord():
    os.system("discord &")
    logging.info("ORDER - open: Discord App")
    return f"No problem, I will open it just for you... but just don't spend your all day chatting!"


def open_gimp():
    os.system("gimp &")
    logging.info("ORDER - open: GIMP")
    return f"What would you like to draw?"


def open_notepad():
    os.system("xed &")
    logging.info("ORDER - open: xed")
    return "Here you are, let's write a wonderful story!"


def answer_play_music(message):
    path = message.split(':', 1)[-1]
    insert_assistant_message(f"So, you would like me to listen to {path}? No problem!", "Lula")
    play_media(path)


def answer_play_video(message):
    path = message.split(':', 1)[-1]
    insert_assistant_message(f"So, you would like me to watch together this: {path}? Okay, let's go~!", "Lula")
    play_media(path)


def play_media(file_path):
    logging.info(f"ORDER - play: {file_path}")
    cmd = f'celluloid "{file_path}" &'
    os.system(cmd)


def fortune_cookie():

    insert_assistant_message("Okay, I have one fortune cookie for you!", "Lula")
    insert_assistant_message("Let's open it...", "Lula")
    insert_assistant_message("It says...", "Lula")

    cookies = ["Love will lead the way.", "The man who waits till tomorrow, misses the opportunities of today.",
               "Grant yourself a wish this year only you can do it.", "The problem with resisting temptation is that it may never come again.",
               "Your fortune is as sweet as a cookie.", "The greatest risk is not taking one.",
               "No distance is too far, if two hearts are tied together.", "Your worst enemy has a crush on you!",
               "You cannot become rich except by enriching others.","The food here taste so good, even a cave man likes it.",
               "I have a dream.... Time to go to bed.", "The race is not always to the swift, but to those who keep on running."]
    fortune = random.randint(0, len(cookies) - 1)

    return cookies[fortune].upper()


def open_signal():
    logging.info(f"ORDER - open: signal")
    os.system("/opt/Signal/signal-desktop --no-sandbox %U &")


def open_terminal():
    logging.info(f"ORDER - open: gnome-terminal")
    os.system("gnome-terminal &")
