import logging
import tkinter
import customtkinter
import asyncio
from async_tkinter_loop import async_handler, async_mainloop


# ==============================================================================
#   Virtual Assistant App GUI Functions
# ==============================================================================

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def change_scaling_event(self, new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)


@async_handler
async def counter():
    i = 0
    while True:
        insert_assistant_message("10", "Ziemniak")
        # notification.notify(title="Ziemniak has announced something.", message="Drink water!")
        await asyncio.sleep(10.0)

# ==============================================================================
#   Virtual Assistant App GUI
# ==============================================================================

root = tkinter.Tk()

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("dark")
root.configure(background="#191919")

root.title("BEng Thesis - Intelligent Virtual Personal Assistant")
root.geometry(f"{1800}x{900}")

icon = tkinter.PhotoImage(file="./data/icon.png")
root.iconphoto(False, icon)

# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

# create sidebar frame with widgets
root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
root.sidebar_frame.grid_rowconfigure(4, weight=1)

root.logo_label = customtkinter.CTkLabel(root.sidebar_frame, text="L.U.L.A.",
                                         font=customtkinter.CTkFont(size=20, weight="bold"))
root.logo_label.grid(row=0, column=0, padx=20, pady=(10, 0))

root.logo_label_dsc = customtkinter.CTkLabel(root.sidebar_frame, text="Linux User Lovely Assistant",
                                             font=customtkinter.CTkFont(size=10))
root.logo_label_dsc.grid(row=1, column=0, padx=0, pady=(0, 0))

root.little_side_frame = customtkinter.CTkFrame(root.sidebar_frame, width=130, corner_radius=0)
root.little_side_frame.grid(row=2, column=0)

root.logo_label_dsc = customtkinter.CTkLabel(root.little_side_frame, text="Thinking about: little cats\nMood: curious",
                                             font=customtkinter.CTkFont(size=10))
root.logo_label_dsc.grid(row=0, column=0, padx=0, pady=(0, 0))

# root.sidebar_button_2 = customtkinter.CTkButton(root.sidebar_frame, command="")
# root.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
# root.sidebar_button_3 = customtkinter.CTkButton(root.sidebar_frame, command="")
# root.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

# change colours of GUI
root.appearance_mode_label = customtkinter.CTkLabel(root.sidebar_frame, text="Appearance Mode:", anchor="w")
root.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(0, 0))
root.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(root.sidebar_frame, values=["Dark", "Light"],
                                                               command=lambda x=None: change_appearance_mode_event(root.appearance_mode_optionemenu.get()))
root.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

# configure
root.sidebar_button_conf = customtkinter.CTkButton(root.sidebar_frame,  text_color=("gray10", "#DCE4EE"),
                                                   command="", state="disabled", text="Configure Assistant")
root.sidebar_button_conf.grid(row=7, column=0, padx=20, pady=(0, 20))

# create entry field for user
root.user_entry = customtkinter.CTkEntry(root, placeholder_text="Write something...")
root.user_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

# create textbox with chat history
root.textbox = customtkinter.CTkTextbox(root, width=250, state="disabled")
root.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew", columnspan=3, rowspan=3)


# ==============================================================================
#   Button behaviour
# ==============================================================================

def send_button_event(kernel, assistant):
    user_message = root.user_entry.get()
    insert_user_message(user_message, kernel, assistant)


def insert_user_message(msg, kernel, assistant):
    if not msg:
        return

    root.user_entry.delete(0, tkinter.END)
    print_msg = f"VIKTORIA: {msg}\n"
    root.textbox.configure(state="normal")
    root.textbox.insert(tkinter.END, print_msg)
    root.textbox.configure(state="disabled")

    user_intent = assistant.get_user_intent(msg)
    insert_assistant_message(assistant.decide_action(msg, user_intent, kernel), assistant.name)


def insert_assistant_message(msg, name):

    if msg == '':
        msg = "Well..."

    print_msg = f"{name.upper()}: {msg}\n"
    root.textbox.configure(state="normal")
    root.textbox.insert(tkinter.END, print_msg)
    root.textbox.configure(state="disabled")
    root.textbox.see(tkinter.END)
