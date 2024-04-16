import tkinter
from tkinter import *
import tkinter.messagebox
import customtkinter
import os
import subprocess
from PIL import Image, ImageTk
import ast
import re
import pandas as pd
import numpy as np

# main file
main_file = 'C:/Users/singhab3/OneDrive - STMicroelectronics/Desktop/Workplace/GUI/Scripts_Gui.txt'
df = pd.read_csv(main_file)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

def inputs(mand_inp, opt_inp, script_type, script_path):
    script_name = os.path.basename(script_path)
    # 0 X 3
    input_frame = customtkinter.CTkTabview(app, fg_color='transparent', border_width=1)
    input_frame.add(script_name)
    input_frame.grid(row=0, column=3, rowspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew")
    input_frame.tab(script_name).grid_columnconfigure(0, weight=1)
    input_frame.tab(script_name).grid_rowconfigure((1,2), weight=1)
    # 1 X 1
    textbox = customtkinter.CTkTextbox(app, state='disabled', border_width=1)#, height=210)
    textbox.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
    
    # Script help data ( only for python now )
    if (script_name.endswith(".py")):    
        help_data = subprocess.check_output("python \"{}\" -h".format(script_path), shell=True)
        textbox.configure(state='normal')
        textbox.insert("0.0", help_data)
        textbox.configure(state='disabled')
    
    # mandatory frame
    mandatory_frame = customtkinter.CTkScrollableFrame(input_frame.tab(script_name), label_text="Mandatory Inputs")#, label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"), height=290)
    mandatory_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
    mandatory_frame.grid_columnconfigure(1, weight=1)
    # optional frame
    optional_frame = customtkinter.CTkScrollableFrame(input_frame.tab(script_name), label_text="Optional Inputs")
    optional_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
    optional_frame.grid_columnconfigure(1, weight=1)
    
    if script_type == 1:
        type_var = tkinter.IntVar(value=script_type)
        type_button_1 = customtkinter.CTkRadioButton(input_frame.tab(script_name), variable=type_var, value=1, text='Type I')#, command=type_selection)
        type_button_1.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="w")
        type_button_2 = customtkinter.CTkRadioButton(input_frame.tab(script_name), variable=type_var, value=2, text='Type II', state=tkinter.DISABLED)#, command=type_selection)
        type_button_2.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="e")
        
        label_entry_pair = []
        for i, arg in enumerate(mand_inp.split()):
            label = customtkinter.CTkLabel(mandatory_frame, text=arg)
            label.grid(row=i, column=0, padx=(20, 0), pady=(0, 15), sticky="w")
            entry = customtkinter.CTkEntry(mandatory_frame, placeholder_text=f"Input {i+1}")
            entry.grid(row=i, column=1, padx=(20, 20), pady=(0, 15), sticky="nsew")
            label_entry_pair.append([label, entry])
        
        optional_entry_pair = []
        if not pd.isna(opt_inp):
            for i, arg in enumerate(opt_inp.split()):
                label = customtkinter.CTkLabel(optional_frame, text=arg)
                label.grid(row=i, column=0, padx=(20, 0), pady=(0, 15), sticky="w")
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Input {i+1}")
                entry.grid(row=i, column=1, padx=(20, 20), pady=(0, 15), sticky="nsew")
                optional_entry_pair.append([label, entry])
            
            def add_entry_type1():
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split()) - 1}")
                entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
                optional_entry_pair.append([f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split()) - 1}", entry])
            
            plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, command=add_entry_type1, border_width=1)
            plus_button.grid(row=len(opt_inp.split()), column=1, padx=20, pady=(0, 15), sticky="e")
        
        else:
            # for no optional inputs
            def add_entry_type1():
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children())}")
                entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
                optional_entry_pair.append([f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split()) - 1}", entry])
            
            plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, command=add_entry_type1, border_width=1)
            plus_button.grid(row=0, column=1, padx=20, pady=(0,15), sticky="e")

        # run button
        def run_command():
            command = [script_path]
            for mlabel, mentry in label_entry_pair:
                command.append(mlabel.cget('text'))
                command.append(mentry.get())
            
            for olabel, oentry in optional_entry_pair:
                try:    
                    command.append(olabel.cget('text'))
                    command.append(oentry.get())
                except Exception as e:
                    command.append(oentry.get())
            
            print(command)

        run_button = customtkinter.CTkButton(input_frame.tab(script_name), text='Run', border_width=2, command=run_command, fg_color="green", hover_color="darkgreen", font=customtkinter.CTkFont(size=16, weight="bold"), height=50)
        run_button.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew",)
        
    elif script_type == 2:
        type_var = tkinter.IntVar(value=script_type)
        type_button_1 = customtkinter.CTkRadioButton(input_frame.tab(script_name), variable=type_var, value=1, text='Type I', state=tkinter.DISABLED)#, command=type_selection)
        type_button_1.grid(row=0, column=0, padx=(20, 0), pady=(0, 0), sticky="w")
        type_button_2 = customtkinter.CTkRadioButton(input_frame.tab(script_name), variable=type_var, value=2, text='Type II')#, command=type_selection)
        type_button_2.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="e")
        
        label_entry_pair = {}
        for i, arg in enumerate(mand_inp.split()):
            entry = customtkinter.CTkEntry(mandatory_frame, placeholder_text=f"{arg}")
            entry.grid(row=i, column=0, columnspan=2, padx=(20, 20), pady=(0, 15), sticky="nsew")
            label_entry_pair[arg] = entry
        
        optional_entry_pair = {}
        if not pd.isna(opt_inp):
            for i, arg in enumerate(opt_inp.split()):
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"{arg}")
                entry.grid(row=i, column=1, padx=(20, 20), pady=(0, 15), sticky="nsew")
                optional_entry_pair[arg] = entry
            
            def add_entry_type2():
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split())}")
                entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
                optional_entry_pair[f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split()) - 1}"] = entry
            
            plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, border_width=1, command=add_entry_type2)
            plus_button.grid(row=len(opt_inp.split()), column=1, padx=20, pady=(0, 15), sticky="e")

        else:
            # for no optional inputs
            def add_entry_type2():
                entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children())}")
                entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
                optional_entry_pair[f"Optional Input {len(optional_frame.winfo_children()) - 1}"] = entry
            
            plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, command=add_entry_type2, border_width=1)
            plus_button.grid(row=0, column=1, padx=20, pady=(0, 15), sticky="e")
        
        # run button
        def run_command():
            command = [script_path]
            for mlabel, mentry in label_entry_pair.items():
                command.append(mentry.get())
            
            for olabel, oentry in optional_entry_pair.items():
                command.append(oentry.get())
            
            print(command) 

        run_button = customtkinter.CTkButton(input_frame.tab(script_name), text='Run', border_width=2, command=run_command, fg_color="green", hover_color="darkgreen", font=customtkinter.CTkFont(size=16, weight="bold"), height=50)
        run_button.grid(row=3, column=0, padx=(20, 20), pady=(20,20), sticky="nsew",)

def get_script(name):
    for widget in script_frame.winfo_children():
        widget.destroy()
    # selected category dataframe
    category_df = df.loc[df["Category"] == name]
    for i in category_df.itertuples():
        script_button = customtkinter.CTkButton(script_frame, text=os.path.basename(i[2]), command=lambda mand_inp=i[3], opt_inp=i[4], script_type=i[5], script_path=i[2]: inputs(mand_inp, opt_inp, script_type, script_path))
        script_button.grid(row=i[0], column=0, padx=20, pady=(0, 20), sticky='nsew')
    print(category_df)


app = customtkinter.CTk()
app.title("\U0001F6FAmation Hub")
app.geometry(f"{1024}x{480}")

iconpath = ImageTk.PhotoImage(file="automation_light.png")
app.wm_iconbitmap()
app.iconphoto(False, iconpath)

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)

# sidebar 0 X 0
logo_image = customtkinter.CTkImage(dark_image=Image.open('automation_light.png'), light_image=Image.open('automation_dark.png'), size=((80, 80)))

sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)

logo_label = customtkinter.CTkLabel(sidebar_frame, text="Automation\nHub", font=customtkinter.CTkFont(size=24, weight="bold"), image=logo_image, compound=customtkinter.TOP)
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 10))

scaling_label = customtkinter.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
scaling_label.grid(row=7, column=0, padx=20, pady=(0, 0))
scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event)
scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(0, 20))

# 0 X 1
category_frame = customtkinter.CTkScrollableFrame(app, label_text="Category", label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"), height=290)
category_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
category_frame.grid_columnconfigure(0, weight=1)

for i, category in enumerate(df['Category'].unique()):
    category_button = customtkinter.CTkButton(category_frame, text=category, command=lambda name=category: get_script(name))
    category_button.grid(row=i, column=0, padx=20, pady=(0, 20), sticky='nsew')

# 0 X 2
script_frame = customtkinter.CTkScrollableFrame(app, label_text="Scripts", label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"))
script_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
script_frame.grid_columnconfigure(0, weight=1)

# 0 X 3
input_frame = customtkinter.CTkTabview(app, fg_color='transparent', border_width=1)
input_frame.grid(row=0, column=3, rowspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew")
input_frame.grid_columnconfigure(0, weight=1)

# 1 X 1
textbox = customtkinter.CTkTextbox(app, state='disabled', border_width=1)
textbox.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

# defaults
appearance_mode_optionemenu.set("Dark")
scaling_optionemenu.set("100%")
input_frame.add('Inputs')

app.mainloop()