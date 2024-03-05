#!/bin/env python3
import os
import aiml
import asyncio
import tkinter
import logging
import logging.config
import customtkinter

from plyer import notification
from async_tkinter_loop import async_handler, async_mainloop

from source.assistant_logic import Assistant, greet_user
from source.gui import root, insert_assistant_message, send_button_event


# ==============================================================================
#   Logger
# ==============================================================================

def create_logger(config_file_path: str):

    logging.config.fileConfig(config_file_path)
    return logging.getLogger()


def log_service_start():
    logging.info(" ==== BEng Thesis - Intelligent Virtual Personal Assistant STARTED ==== ")


def log_service_stop():
    logging.info(" ==== BEng Thesis - Intelligent Virtual Personal Assistant STOPPED ==== ")


@async_handler
async def counter():
    while True:
        insert_assistant_message("10", "Ziemniak")
        notification.notify(title="Ziemniak has announced something.", message="Drink water!")
        await asyncio.sleep(10.0)


@async_handler
async def water_counter(kernel, assistant):
    while True:
        notification.notify(title="LULA wrote (1) message...", message="Drink water!")
        insert_assistant_message("Did you drink water?", "LULA")

        root.send_water_msg_button = customtkinter.CTkButton(master=root, fg_color="transparent", border_width=2,
                                                             text_color=("gray10", "#DCE4EE"),
                                                             command=lambda: send_water_button_event(kernel, assistant,
                                                                                                     root.send_water_msg_button),
                                                             text="DRINK WATER")
        root.send_water_msg_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        await asyncio.sleep(45)


@async_handler
async def send_water_button_event(kernel, assistant, button):
    print("click water")
    user_message = root.user_entry.get()

    if not user_message:
        return

    root.user_entry.delete(0, tkinter.END)

    print_msg = f"VIKTORIA: {user_message}\n"
    root.textbox.configure(state="normal")
    root.textbox.insert(tkinter.END, print_msg)
    root.textbox.configure(state="disabled")

    user_intent = assistant.get_user_intent(user_message)
    print(user_intent)

    if user_message == "Yes!":
        insert_assistant_message("I am so happy to hear that!", "LULA")
        insert_assistant_message("Good hydration of the body is very important for mental work.", "LULA")
        insert_assistant_message("I'll remind you about it in a while.", "LULA")
        insert_assistant_message("I am here to help you, right?", "LULA")
        button.destroy()
    else:
        insert_assistant_message("Noooo! Please, drink something!", "LULA")

    await asyncio.sleep(0)


def main():

    create_logger("config/virtual-assistant.conf")
    log_service_start()
    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        logging.info("BRAIN - exists.")
        logging.info(kernel.bootstrap(brainFile="bot_brain.brn"))
    else:
        logging.info("KERNEL - creating a new brain file...")
        logging.info(kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b"))
        logging.info(kernel.saveBrain("bot_brain.brn"))

    assistant = Assistant("Lula")
    insert_assistant_message(greet_user(), assistant.name)

    root.send_msg_button = customtkinter.CTkButton(master=root, border_width=2,
                                                   text_color=("gray10", "#DCE4EE"),
                                                   command=lambda: send_button_event(kernel, assistant),
                                                   text="Send!")
    root.send_msg_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    #water_counter(kernel, assistant)

    async_mainloop(root)


if __name__ == "__main__":
    main()
