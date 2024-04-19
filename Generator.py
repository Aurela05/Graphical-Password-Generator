import customtkinter
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image
from pathlib import Path
from pickle import APPEND
import string
import secrets
import PySimpleGUI as sg

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Settings")
        
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=12, padx=10)
        
        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.pack(pady=12, padx=10)
        
        self.label = customtkinter.CTkLabel(self.frame, text="Settings Window", font=("Roboto",24))
        self.label.pack(padx=20, pady=20)
        
        self.entry1 = customtkinter.CTkEntry(self.frame,placeholder_text="Please type your name")
        self.entry1.pack(pady=12, padx=10)
        
        self.entry2 = customtkinter.CTkEntry(self.frame, placeholder_text="How many characters should be included?")
        self.entry2.pack(pady=12, padx=10)
        
        self.drop1 = customtkinter.CTkOptionMenu(self.frame, values=["Lowercase", "Lower and Upper", "Numbers", "All"])
        self.drop1.pack( pady=12, padx=10)
        
        self.button1 = customtkinter.CTkButton(self.frame2, text="Confirm", command=self.save)
        self.button1.pack(padx=12, pady=10)
        
        self.button2 = customtkinter.CTkButton(self.frame2, text="Exit", command=self.exit)
        self.button2.pack(padx=12, pady=10)
        
    def save(self):
        self.user = self.entry1.get()
        self.pwd_length = self.entry2.get()
        self.chars = self.drop1.get()
        if self.chars == "Lowercase":
            self.charsss = string.ascii_lowercase
        if self.chars == "Lower and Upper":
            self.charsss = string.ascii_letters
        if self.chars == "Numbers":
            self.charsss = string.digits
        if self.chars == "All":
            self.charsss = string.ascii_letters + string.digits
        
        #--Save to ini file
        settings["USER"]["person_1"] = self.user
        settings["PASS"]["length"] = self.pwd_length
        settings["PASS"]["chars"] = self.charsss
        self.exit()
        
    def exit(self):
        self.destroy()
        
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x500")
        self.title("Password Generator 2.0")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=12, padx=10)
        
        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.pack(pady=12, padx=10)
        
        self.label1 = customtkinter.CTkLabel(self.frame,text="Welcome to my Password Generator", font=("Roboto",24))
        self.label1.pack(pady=12, padx=10)
        
        self.button_1 = customtkinter.CTkButton(self.frame, text="Generate Password", command=self.generate)
        self.button_1.pack(side="top", padx=20, pady=20)
        
        self.label2 = customtkinter.CTkLabel(self.frame2, text="Current Settings", font=("Roboto",24))
        self.label2.pack(pady=12, padx=10)
        
        # self.label3 = customtkinter.CTkLabel(self.frame2, text="User: "+USERNAME, font=("Roboto",18))
        # self.label3.pack(pady=12, padx=10)
        
        # self.label4 = customtkinter.CTkLabel(self.frame2, text="Length: "+settings["PASS"]["length"], font=("Roboto",18))
        # self.label4.pack(pady=12, padx=10)
        
        self.button_2 = customtkinter.CTkButton(self.frame2, text="Settings", command=self.open_toplevel)
        self.button_2.pack(side="top", padx=20, pady=20)
        
        self.button_3 = customtkinter.CTkButton(self.frame2, text="Open file", command=self.open_file)
        self.button_3.pack(side="top", padx=20, pady=20)
        
        self.textbox = customtkinter.CTkTextbox(master=self, width=400)
        
        
        

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SettingsWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.state("normal")
            
    def generate(self):
        password = ""
        password_char = settings["PASS"]["chars"]
        password_len=int(settings["PASS"]["length"])
        
        for i in range(password_len):
            password += "".join(secrets.choice(password_char))
            
        USERNAME = settings["USER"]["person_1"]
        settings["PASS"]["password"] = password
        text_file = open(USERNAME, "a")
        text_file.write('()--'+password)
        text_file.write(' ')
        text_file.close()

        settings["PASS"]["password"] = password
        print(password)
    
    def open_file(self):
        self.filename = filedialog.askopenfilename(initialdir=".../PythonPWG",title="e",filetypes=(("txt file","*.txt"),("all files","*.*")))
        if self.filename:
            print("e")
            with open(self.filename, 'r') as file:
                content = file.read()
                self.textbox.pack(pady=12, padx=10)
                self.textbox.insert("0.0",content)

                
                
class Appdef(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x500")
        self.title("Password Generator 2.0")

if __name__ == "__main__": 
    SETTINGS_PATH = str(Path.cwd())
    
#--Locate ini file
    settings = sg.UserSettings(
    path=SETTINGS_PATH, filename="settings.ini", use_config_file=True, convert_bools_and_none=True
    )
    
#--Default settings
    if settings["PASS"]["length"] == '':
        settings["PASS"]["length"] = 0
    if settings["USER"]["person_1"] == '':
        settings["USER"]["person_1"] = 'User'
#--Assign variables from ini file
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    USERNAME = settings["USER"]["person_1"]
    password_length = int(settings["PASS"]["length"])
    password_len_disp=str(password_length)
    password_char = str(settings["PASS"]["chars"])
    password = ""
    password = settings["PASS"]["password"]
    
app = App()
app.mainloop()