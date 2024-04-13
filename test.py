import customtkinter

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
        
        self.entry1 = customtkinter.CTkEntry(self.frame,placeholder_text="Please type you name")
        self.entry1.pack(pady=12, padx=10)
        
        self.entry2 = customtkinter.CTkEntry(self.frame, placeholder_text="How many characters should be included?")
        self.entry2.pack(pady=12, padx=10)
        
        self.drop1 = customtkinter.CTkOptionMenu(self.frame, values=["lowercase", "UPPERCASE", "Numbers", "All"])
        self.drop1.pack( pady=12, padx=10)
        
        self.button1 = customtkinter.CTkButton(self.frame2, text="Confirm", command=self.save)
        self.button1.pack(padx=12, pady=10)
        
        self.button2 = customtkinter.CTkButton(self.frame2, text="Exit", command=self.exit)
        self.button2.pack(padx=12, pady=10)
        
    def save(self):
        self.user = self.entry1.get()
        self.pwd_length = self.entry2.get()
        self.chars = self.drop1.get()
        print(self.user,self.pwd_length,self.chars)
        
        #--Save to ini file
        
        self.exit()
        
    def exit(self):
        self.state("withdrawn")
        
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("900x700")
        self.title("Password Generator 2.0")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=12, padx=10)
        
        self.label1 = customtkinter.CTkLabel(self.frame,text="Welcome to my Password Generator", font=("Roboto",24))
        self.label1.pack(pady=12, padx=10)
        
        self.button_1 = customtkinter.CTkButton(self.frame, text="Generate Password", command=self.generate)
        self.button_1.pack(side="top", padx=20, pady=20)
        
        self.button_2 = customtkinter.CTkButton(self.frame, text="Settings", command=self.open_toplevel)
        self.button_2.pack(side="top", padx=20, pady=20)
        
        

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SettingsWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.state("normal")
            
    def generate(self):
        pass


app = App()
app.mainloop()