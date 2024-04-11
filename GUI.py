import PySimpleGUI as sg
from pathlib import Path
from pickle import APPEND
import string
import secrets
    
bugs="{Known bugs: If 'please select an option' is selected it will use those characters for the password which causes spaces to appear in the password}"

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num = "123456789"
l_and_n = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
justify1="                                                           "
justify2="                                                                        "

#--Settings window so the user can change the specifications of their password
def settings_window(settings):
    layout = [
        [sg.Text("SETTINGS")],
        [sg.Text("How many characters should your password include? "), sg.Input(settings["PASS"]["length"], key="-length-", s=8)],
        [sg.Text("Please type your name:"), sg.Input(settings["USER"]["person_1"], key="-user-", s=10)],
        [sg.DropDown(values=["Lowercase", "Lower and uppercase", "Numbers", "Letters and numbers"], default_value="Please select an option", key="-charac-", s=18)],
        [sg.Button("Save current settings")],
        ]
    
    window = sg.Window("Current settings", layout, modal=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "Save current settings":
            settings["PASS"]["chars"] = values["-charac-"]
            settings["PASS"]["length"] = values["-length-"]
            settings["PASS"]["length"] == int
            settings["USER"]["person_1"] = values["-user-"]
            if settings["PASS"]["chars"] == "Lowercase":
                settings["PASS"]["chars"] = lower
            elif settings["PASS"]["chars"] == "Uppercase":
                settings["PASS"]["chars"] = upper
            elif settings["PASS"]["chars"] == "Numbers":
                settings["PASS"]["chars"] = num
            elif settings["PASS"]["chars"] == "Letters and numbers":
                settings["PASS"]["chars"] = l_and_n   
            sg.popup_no_titlebar("Settings saved!")
            break
    window.close()
    
def generate_password():
    password = ""
    password_char = settings["PASS"]["chars"]
    password_len=int(settings["PASS"]["length"])
    
    for i in range(password_len):
        password += "".join(secrets.choice(password_char))
        
    settings["PASS"]["password"] = password
    text_file = open(USERNAME, "a")
    text_file.write(password)
    text_file.close()

    #while True:
        #for i in range(password_length):
            #password += "".join(secrets.choice(password_char))
        #break
    settings["PASS"]["password"] = password
    print(password)
    print(password_char)

def main_window():
    #--Create the menu at the top of the app
    menu_def = [
        ["Toolbar", ["Command 1", "Command 2"]],
                ["Help", ["Settings", "About"]]
    ]
    
    #--Create the two main layouts
    layoutUpdate = [
        [sg.Text("User: " + USERNAME, key="xxx"), sg.Text(size=(15,1))],
        [sg.Text("----------------------------------------------------------------------------------------------------------------------------")], 
        [sg.Text(justify1+"Welcome to my password generator!")],
        [sg.Text(justify2+"Your current settings: ", text_color="Black", justification="center")],
        [sg.Text("----------------------------------------------------------------------------------------------------------------------------")],
        [sg.Text("Length of password: " + password_len_disp, key="len")],
        [sg.Text("Characters included: " + password_char, key="char")],
        [sg.Sizer(v_pixels=336)],
        [sg.Button("Generate Password"), sg.Button("Settings")],
        ]
    layout_final = [
        [sg.Text("Here is your password, " + USERNAME, key="yyy")],
        [sg.Text(password, key="pass")],
        [sg.Text("", key="iff")],
        [sg.Sizer(v_pixels=464)],
        [sg.Button("Reload App")],
    ]
    #--Make it possible to switch between the two main layouts
    layout = [
        [sg.MenubarCustom(menu_def, tearoff=False)],
        [sg.Column(layoutUpdate, key="-COL1-"),
         sg.Column(layout_final, key="-COL2-", visible=False)],
        [sg.Button("Exit")],
    ]
    #--Get window title from ini file and create the main window
    window_title = settings["GUI"]["title"]
    window = sg.Window(window_title, layout, location=(0,0), size=(900,700), keep_on_top=True, finalize=True)
    
#--Main while loop
    layout = 1
    while True:
        event, values = window.read()
        print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        
        if event == "About":
            window.disappear()
            sg.popup(window_title, "Version 1.0", "Generate and store random, secure passwords", bugs, grab_anywhere=True)
            window.reappear()
            
        if event in ("Command 1","Command 2"):
            sg.popup_error("Those features have not been implemented yet!", keep_on_top=True)
            
        #--Generate a password based on the specifications of the user
        #--Also switches the layout fluidly
        if event == "Generate Password":
            generate_password()
            window[f"-COL{layout}-"].update(visible=False)
            if layout < 2:
                layout += 1
                if len(settings["PASS"]["password"]) > 76:
                    window["iff"].update("Your password is too long to display in the app; check the auto-generated text file")
                    pass
                NAME="Here is your password, "+settings["USER"]["person_1"]+":"
                pw=settings["PASS"]["password"]
                window["yyy"].update(NAME)
                window["pass"].update(pw)
                window[f"-COL{layout}-"].update(visible=True)
                
        if event == "Reload App":
            window[f"-COL{layout}-"].update(visible=False)
            window["-COL1-"].update(visible=True)
            layout = 1
            
        elif event in (sg.WINDOW_CLOSED, "Exit"):
            break
        
        #--Open settings window and updates UI in the main window
        if event == "Settings":
            window.disappear()
            settings_window(settings)
            number="Length of password: "+str(settings["PASS"]["length"])
            NAME=settings["USER"]["person_1"]
            char="Characters included: "+settings["PASS"]["chars"]
            window["len"].update(number)
            window["xxx"].update(NAME)
            window["char"].update(char)
            window.reappear()
            
    window.close()

if __name__ == "__main__": 
    SETTINGS_PATH = str(Path.cwd())
    
#--Locate ini file
    settings = sg.UserSettings(
    path=SETTINGS_PATH, filename="settings.ini", use_config_file=True, convert_bools_and_none=True
    )
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
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    main_window()