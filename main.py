"""
Auother CSR(@TechyCSR)

Run_Main file for AI-Assistant V-1.0
"""




import tkinter as tk
from tkinter import messagebox, Scrollbar, filedialog
from ttkthemes import ThemedStyle
import speech_recognition as sr
import pyttsx3
import asyncio
import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import re
import logging
import urllib.parse
import emoji
from required.bing_image_downloader import downloader
from PIL import Image, ImageTk
import os
import threading


# Rename the imported 'config' module to 'config_file' to avoid conflict
import my_config as config_file


def check_config():
    if not isinstance(config_file.bot_name, str):
        print("Bot name should be a string. Correct it in config.py file.")
        return False

    if not isinstance(config_file.adult_filter_off, bool):
        print("adult_filter_off should be a Boolean value. Correct it in config.py file.")
        return False

    if not isinstance(config_file.auto_delete, bool):
        print("auto_delete should be a Boolean value. Correct it in config.py file.")
        return False

    if config_file.img_typ not in ["gif", "photo", "clipart", "transparent"]:
        print("img_typ should be one of 'gif', 'photo', 'clipart', or 'transparent'. Correct it in config.py file.")
        return False
    
    if config_file.VoiceType not in ["M","F"]:
        print("voice_typ should be one of 'M','F'. Correct it in config.py file.")
        return False
    
    return True

if __name__ == "__main__":
    if not check_config():
        # Stop execution if there are configuration errors
        exit()



#checking up configuartion 

name=config_file.bot_name
master=config_file.master
ad=config_file.auto_delete
ac=config_file.adult_filter_off
imgnum=config_file.num_images
imgtyp=config_file.img_typ
diretory=config_file.output_dir
logm=config_file.verbose

global vid
vid=0
if config_file.VoiceType =="M":
    vid=0
else :
    vid=1



# Function to create a new chatbot instance
def create_chatbot():
    cookies = json.loads(open("cookie.json", encoding="utf-8").read())  # might omit cookies option
    return asyncio.run(Chatbot.create(cookies=cookies))

# Create the initial chatbot instance
bot = create_chatbot()

def remove_asterisks(text):
    # Remove asterisks using regex
    return re.sub(r'\*', '', text)

def response(text):
    text_to_speech("Have Patience, I am Typing my Response.")
    try:
        response = asyncio.run(bot.ask(prompt=text, conversation_style=ConversationStyle.creative, simplify_response=True))
        rs = response["text"]
        rs = rs.replace("Bing", f"{name}")
        rs = rs.replace("bing", f"{name}")
        rs = rs.replace("Microsoft", f"{master}'s")
        rs = remove_asterisks(rs)
        text_to_speech("Here's, My response on Your Screen .")
    except Exception as e:
        text_to_speech("Some Error has raised, Please fix me to use further.")
        messagebox.showinfo("Error Warning", "You need to restart or need to update the cookie file to continue :) ")
        rs = str(e) + f"\nYou Need to Click Restart Button To Reset {name}."
        rs = rs.replace("Bing", f"{name}")
        rs = rs.replace("bing", f"{name}")
        rs = rs.replace("Microsoft", f"{master}'s")
        rs = remove_asterisks(rs)
    return rs

def on_send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        send_button.config(state=tk.NORMAL)
        send_button.config(text="Typing..")
        root.update_idletasks()
        response_text = response(user_input)
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"\n\n👤 {master}: {user_input}\n", "user_text")
        chat_log.insert(tk.END, f"🤖 {name}: {response_text}\n\n", "ai_text")
        chat_log.config(state=tk.DISABLED)
        send_button.config(state=tk.NORMAL)
        send_button.config(text="Send")
        input_text.delete("1.0", tk.END)




def text_to_speech(text):
    engine = pyttsx3.init()
    # Set properties (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[vid].id)  
    engine.setProperty('rate', 123)  # Speed of speech
    engine.say(text)
    engine.runAndWait()


def on_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        voice_input_button.config(state=tk.NORMAL)
        voice_input_button.config(text="Speak..")
        root.update_idletasks()
        audio = r.listen(source)
    try:
        extracted_text = r.recognize_google(audio, language='en-US')
        input_text.insert(tk.END, extracted_text)
        voice_input_button.config(state=tk.NORMAL)
        voice_input_button.config(text="🎤")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        voice_input_button.config(state=tk.NORMAL)
        voice_input_button.config(text="🎤")

def on_restart():
    global bot
    chat_log.config(state=tk.NORMAL)
    chat_log.delete("1.0", tk.END)
    chat_log.config(state=tk.DISABLED)
    input_text.delete("1.0", tk.END)
    bot.close()
    bot = create_chatbot()

def on_image_generate():
    prompt = input_text.get("1.0", tk.END).strip()
    num_images = image_count.get()
    if not num_images:
        num_images = str(imgnum)
    num_images = int(num_images)
    if prompt and num_images:
        text_to_speech("Downloading Images ")
        image_button.config(text="Downloading...")
        image_button.config(state=tk.NORMAL)
        threading.Thread(target=download_images, args=(prompt, num_images), daemon=True).start()

def download_images(prompt, num_images):
    try:
        downloader.download(prompt, limit=num_images, output_dir=diretory, adult_filter_off=ac, force_replace=True, timeout=60, verbose=logm, filter=imgtyp)
        messagebox.showinfo("Image Generation", f"{num_images} Images downloaded successfully!")
        display_images(prompt, num_images)
    except Exception as e:
        #print(e)
        text_to_speech("Some Error has raised, Please fix me to use further.")
        messagebox.showerror("Image Generation Error", f"An error occurred while downloading images: {str(e)}")
    finally:
        image_button.config(text="Image")
        image_button.config(state=tk.NORMAL)
        input_text.delete("1.0", tk.END)
        folder_path = f"dataset/{prompt}"
        if ad is False:
            return
        if os.path.exists(folder_path):
            try:
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)
                os.rmdir(folder_path)
            except Exception as e:
                print(f"Error cleaning up folder {folder_path}: {str(e)}")

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

from PIL import Image, ImageSequence

def resize_gif(image_path, output_path, size=(320, 240)):
    im = Image.open(image_path)
    frames = ImageSequence.Iterator(im)
    frames = thumbnails(frames, size)
    om = next(frames)
    om.info = im.info
    om.save(output_path, save_all=True, append_images=list(frames))

def thumbnails(frames, size):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail(size, Image.LANCZOS )
        yield thumbnail

def display_images(prompt, num):
    chat_log.config(state=tk.NORMAL)
    text_to_speech("Downloading Done,Showing Your Required images .")
    # Insert the prompt before displaying the images
    chat_log.insert(tk.END, f"\n{name}:{num} Images downloaded using the prompt '{prompt}'.\n", "user_text")
    chat_log.tag_configure("user_text", foreground="#3174f0", font=("Arial", 12, "bold"))

    image_frame = tk.Frame(chat_log, bg="#f9f9f9")
    chat_log.window_create(tk.END, window=image_frame)

    image_paths = []
    image_extensions = []
    for i in range(1, num + 1):
        try:
            if imgtyp == "gif":
                ext = "gif"
            else:
                ext = "jpg"

            image_path = f"dataset/{prompt}/Image_{i}.{ext}"
            image_paths.append(image_path)
            image_extensions.append(ext)
        except Exception as e:
            print(f"Error finding image {i}: {str(e)}")

    max_images_per_row = 4
    for i, image_path in enumerate(image_paths):
        try:
            row_index = i // max_images_per_row
            col_index = i % max_images_per_row

            _, file_extension = os.path.splitext(image_path)

            if file_extension.lower() == ".gif":
                resized_gif_path = f"dataset/{prompt}/Resized_Image_{i}.gif"
                resize_gif(image_path, resized_gif_path)  # Resize GIF image
                image_label = ImageLabel(image_frame)
                image_label.load(resized_gif_path)
            else:
                image = Image.open(image_path)
                image = image.resize((250, 200), Image.LANCZOS )
                photo = ImageTk.PhotoImage(image)

                image_label = tk.Label(image_frame, image=photo, bd=2, relief=tk.SOLID)
                image_label.image = photo

            image_label.grid(row=row_index, column=col_index, padx=5, pady=5)
        except Exception as e:
            print(f"Error displaying image {i}: {str(e)}")

    chat_log.config(state=tk.DISABLED)




def on_clear():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete("1.0", tk.END)
    chat_log.config(state=tk.DISABLED)
    input_text.delete("1.0", tk.END)
    image_count.delete(0, tk.END)

def on_save():
    text_to_save = chat_log.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_to_save)
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving the file: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title(f"{name} BY {master}")
root.geometry("800x600")
root.configure(bg="#f9f9f9")

# Apply a themed style for a modern look
style = ThemedStyle(root)
style.set_theme("arc")

# Create a header
header_label = tk.Label(root, text=f"{name} Your Personal AI Assistant !", font=("Arial", 20, "bold"), bg="#0078d4", fg="white", padx=10, pady=5)
header_label.pack(fill=tk.X)

# Create a frame to hold the chat log
chat_frame = tk.Frame(root, bg="#f9f9f9", bd=5, relief=tk.RIDGE)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Create the chat log display
chat_log = tk.Text(chat_frame, wrap="word", height=15, width=70, font=("Arial", 12), bg="white", bd=0)
chat_log.tag_configure("user_text", foreground="#3174f0", font=("Arial", 12, "bold"))
chat_log.tag_configure("ai_text", foreground="#00a650", font=("Arial", 12, "bold"))
chat_log.config(state=tk.DISABLED)

# Create a vertical scroll bar for the chat log
scrollbar = Scrollbar(chat_frame, command=chat_log.yview)
chat_log.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_log.pack(pady=(10, 0), padx=10, fill=tk.BOTH, expand=True)

# Create a footer
footer_frame = tk.Frame(root, bg="#f0f0f0")
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

# Create a frame to hold the input text box and buttons
input_frame = tk.Frame(root, bg="#f9f9f9")
input_frame.pack(pady=5, padx=10, fill=tk.X)

# Create the restart button
restart_button = tk.Button(input_frame, text="Restart", font=("Arial", 12, "bold"), bg="#ff7f50", fg="white", bd=0,
                           activebackground="#ffa070", activeforeground="white", command=on_restart)
restart_button.grid(row=0, column=0, padx=(0, 10))

# Create the image generation button
image_button = tk.Button(input_frame, text="Image", font=("Arial", 12), bg="#0078d4", fg="white", bd=0,
                         activebackground="#005a9e", activeforeground="white", command=on_image_generate)
image_button.grid(row=0, column=1, padx=(10, 0))

# Create an input box for the number of images to download
image_count_label = tk.Label(input_frame, text="Num of Images:", font=("Arial", 12), bg="#f9f9f9")
image_count_label.grid(row=0, column=2, padx=(0, 10))

image_count = tk.Entry(input_frame, font=("Arial", 12), bd=2, relief=tk.SOLID, width=5)
image_count.grid(row=0, column=3, padx=(0, 10))

# Create the main input text box
input_text = tk.Text(input_frame, wrap="word", height=4, width=50, font=("Arial", 12), bd=2, relief=tk.SOLID)
input_text.grid(row=0, column=4, padx=(25, 0))

# Create the send button
send_button = tk.Button(input_frame, text="Send", font=("Arial", 12, "bold"), bg="#00a650", fg="white", bd=0,
                        activebackground="#009743", activeforeground="white", command=on_send)
send_button.grid(row=0, column=5, padx=(20, 40))

# Create the voice input button
voice_input_button = tk.Button(input_frame, text="Audio🎤", font=("Arial", 12), bg="#00a680", fg="white", bd=0,
                               activebackground="#009743", activeforeground="white", command=on_voice_input)
voice_input_button.grid(row=0, column=6, padx=(5, 30))

# Create the clear button
clear_button = tk.Button(input_frame, text="Clear", font=("Arial", 12, "bold"), bg="#ff4757", fg="white", bd=0,
                         activebackground="#ff6b81", activeforeground="white", command=on_clear)
clear_button.grid(row=0, column=7, padx=(10, 15))
text_to_speech("Welcome to Your Personal AI Assistant ")

def toggle_auto_delete():
    global ad
    ad = auto_delete_var.get()
    
# Function to display a message when the toggles are updated
def toggle_updated_message():
    message_label.config(text="Setting Updated!", fg="green")
    message_label.after(2000, clear_message)

def clear_message():
    message_label.config(text="")

# Create the save button
save_button = tk.Button(input_frame, text="Save", font=("Arial", 12), bg="#1e90ff", fg="white", bd=0,
                        activebackground="#4b9bff", activeforeground="white", command=on_save)
save_button.grid(row=0, column=8,padx=(10, 15))
auto_delete_var = tk.BooleanVar(value=ad)

# Create the auto-delete check mark
auto_delete_check = tk.Checkbutton(input_frame, text="Auto Delete", variable=auto_delete_var, bg="#f9f9f9", command=toggle_auto_delete,font=("Arial", 12, "bold"))
auto_delete_check.grid(row=0, column=9, padx=(0, 0), sticky=tk.W)

# Function to toggle the 'Photo' option when the Photo toggle is clicked
def toggle_photo():
    global imgtyp
    if imgtyp == "gif":
        imgtyp = "photo"
        photo_toggle_var.set(True)
        gif_toggle_var.set(False)
        toggle_updated_message()

# Function to toggle the 'Gif' option when the Gif toggle is clicked
def toggle_gif():
    global imgtyp
    if imgtyp == "photo":
        imgtyp = "gif"
        gif_toggle_var.set(True)
        photo_toggle_var.set(False)
        toggle_updated_message()

# Create a BooleanVar to track the state of the Photo toggle
photo_toggle_var = tk.BooleanVar(value=(imgtyp == "photo"))

# Create a BooleanVar to track the state of the Gif toggle
gif_toggle_var = tk.BooleanVar(value=(imgtyp == "gif"))

# Create the Photo toggle button
photo_toggle = tk.Checkbutton(input_frame, text="Photo", variable=photo_toggle_var, bg="#f9f9f9", command=toggle_photo, font=("Arial", 12, "bold"))
photo_toggle.grid(row=1, column=9, padx=(0, 0), sticky=tk.W)

# Create the Gif toggle button
gif_toggle = tk.Checkbutton(input_frame, text="Gif", variable=gif_toggle_var, bg="#f9f9f9", command=toggle_gif, font=("Arial", 12, "bold"))
gif_toggle.grid(row=2, column=9, padx=(0, 0), sticky=tk.W)

# Create a message label to display update messages
message_label = tk.Label(input_frame, text="", font=("Arial", 12, "italic"), fg="green", bg="#f9f9f9")
message_label.grid(row=3, column=8, columnspan=2, pady=(0, 5))



# Create a frame to hold the footer
footer_frame = tk.Frame(root, bg="white", height=5)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

# Create the footer label
footer_label = tk.Label(footer_frame, text="© 2023 - All rights reserved by CSR.", font=("Arial", 10), fg="blue", bg="white")
footer_label.pack(pady=2)


# Run the main loop
root.mainloop()
