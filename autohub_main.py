#!/sw/freetools/python/3.10.4/rh80_64/modules/bin/python
import customtkinter
import os
from PIL import Image, ImageTk
import pandas as pd
import shutil

# main file
main_file = "/work/LIPAT/USER_AREAS/ABHISHEK/AUTOMATION_HUB/scripts_file_new.csv"
df = pd.read_csv(main_file)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

def inputs(mand_inp, opt_inp, script_type, script_path, tools_inp, selected_script_button, info):
    global current_script_button
    # Reset color of the previously selected button
    if current_script_button:
        try:
            current_script_button.configure(fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"])  # customtkinter default color
        except Exception:
            current_script_button = None
    # Change color of the currently selected button
    selected_script_button.configure(fg_color="green", hover_color="darkgreen")
    current_script_button = selected_script_button
    
    script_name = os.path.basename(script_path)
    # 0 X 3
    input_frame = customtkinter.CTkTabview(app, fg_color='transparent', border_width=1, width=420)
    input_frame.add(script_name)
    input_frame.grid(row=0, column=3, rowspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew")
    input_frame.tab(script_name).grid_columnconfigure(0, weight=1)
    input_frame.tab(script_name).grid_rowconfigure((4,5), weight=1)
    
    # 1 X 2
    tools_frame = customtkinter.CTkScrollableFrame(app, label_text="TOOLS", label_font=customtkinter.CTkFont(size=14, weight="bold"))#, label_fg_color='transparent')
    tools_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    tools_frame.grid_columnconfigure(1, weight=1)
    tools_frame.grid_columnconfigure(2, weight=1)
    
    def toggle_checkbox_entries():
        state1 = customtkinter.NORMAL if checkbox_var.get() else customtkinter.DISABLED
        for _, entry in tool_entry_pair1:
            entry.delete(0, "end")
            entry._activate_placeholder()
            entry.master.focus()
            entry.configure(state=state1)
        for entry1, entry2 in tool_entry_pair2:
            for entry in (entry1, entry2):
                entry.delete(0, "end")
                entry._activate_placeholder()
                entry.master.focus()
                entry.configure(state=state1)
        state2 = customtkinter.DISABLED if checkbox_var.get() else customtkinter.NORMAL
        ucdprod_entry.configure(state=state2)
        
    checkbox_var = customtkinter.IntVar()
    checkbox = customtkinter.CTkCheckBox(tools_frame, text="Create .ucdprod", variable=checkbox_var, command=toggle_checkbox_entries, checkbox_height=28, checkbox_width=28, font=customtkinter.CTkFont(size=14))
    checkbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(0, 20), sticky='nsew')
    
    # # tools data
    tool_entry_pair1 = []
    tool_entry_pair2 = []
    if not pd.isna(tools_inp):
        for i, j in enumerate(tools_inp.split('::')):
            if '@' not in j:
                tool_label = customtkinter.CTkLabel(tools_frame, text=j)
                tool_label.grid(row=i+1, column=0, padx=20, pady=(0, 20), sticky='nsw')
                tool_entry = customtkinter.CTkEntry(tools_frame, placeholder_text="version")
                tool_entry.grid(row=i+1, column=1, columnspan=2, padx=(0, 20), pady=(0, 20), sticky='nsew')
                tool_entry.configure(state=customtkinter.DISABLED)
                tool_entry_pair1.append([tool_label, tool_entry])
            else:
                tool_label = customtkinter.CTkLabel(tools_frame, text=j.strip('@'))
                tool_label.grid(row=i+1, column=0, padx=20, pady=(0, 20), sticky='nsw')
                tool_entry1 = customtkinter.CTkEntry(tools_frame, placeholder_text="tool")
                tool_entry1.grid(row=i+1, column=1, padx=(0, 20), pady=(0, 20), sticky='nsew')
                tool_entry2 = customtkinter.CTkEntry(tools_frame, placeholder_text="version")
                tool_entry2.grid(row=i+1, column=2, padx=(0, 20), pady=(0, 20), sticky='nsew')
                tool_entry1.configure(state=customtkinter.DISABLED)
                tool_entry2.configure(state=customtkinter.DISABLED)
                tool_entry_pair2.append([tool_entry1, tool_entry2])
    
    # 0 X 0
    info_frame = customtkinter.CTkTextbox(input_frame.tab(script_name), state='disabled', border_width=1, height=60)
    info_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
    info_frame.configure(state='normal')
    info_frame.insert("end", 'INFO: ')
    info_frame.insert("end", info)
    info_frame.configure(state='disabled')
    
    # reset button
    def reset():
        # reset checkbox
        checkbox_var.set(0)
        state1 = customtkinter.NORMAL if checkbox_var.get() else customtkinter.DISABLED
        state2 = customtkinter.DISABLED if checkbox_var.get() else customtkinter.NORMAL
        # reset tool entries
        for _, entry in tool_entry_pair1:
            entry.delete(0, "end")
            entry._activate_placeholder()
            entry.master.focus()
            entry.configure(state=state1)
        for entry1, entry2 in tool_entry_pair2:
            for entry in (entry1, entry2):
                entry.delete(0, "end")
                entry._activate_placeholder()
                entry.master.focus()
                entry.configure(state=state1)
        ucdprod_entry.configure(state=state2)
        # reset inputs section
        for entry in (chng_entry, ucdprod_entry):
            entry.delete(0, "end")
            entry._activate_placeholder()
            entry.master.focus()
        for entry_pairs in (mandatory_entry_pair, optional_entry_pair):
            for _, entry in entry_pairs:
                entry.delete(0, "end")
                entry._activate_placeholder()
                entry.master.focus()
    # 0 X 1
    reset_button = customtkinter.CTkButton(input_frame.tab(script_name), text="RESET", command=reset, fg_color="red", border_width=1, width=40, corner_radius=20, hover_color='darkred', font=customtkinter.CTkFont(size=14, weight="bold"))
    reset_button.grid(row=0, column=1, padx=(0, 20), pady=(10, 0), sticky="nse")
    
    
    
    # 0 X 3 - 1 x 0
    chng_entry = customtkinter.CTkEntry(input_frame.tab(script_name), placeholder_text="Working directory path")
    chng_entry.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    
    # 2 X 0
    ucdprod_entry = customtkinter.CTkEntry(input_frame.tab(script_name), placeholder_text="Existing .ucdprod path")
    ucdprod_entry.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    
    # mandatory frame
    # 0 X 3 - 2 X 0
    mandatory_frame = customtkinter.CTkScrollableFrame(input_frame.tab(script_name), label_text="Mandatory Inputs")#, label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"), height=290)
    mandatory_frame.grid(row=4, column=0, columnspan = 2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    mandatory_frame.grid_columnconfigure(1, weight=1)
    # optional frame
    # 0 X 3 - 3 X 0
    optional_frame = customtkinter.CTkScrollableFrame(input_frame.tab(script_name), label_text="Optional Inputs")
    optional_frame.grid(row=5, column=0, columnspan = 2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    optional_frame.grid_columnconfigure(1, weight=1)
    
    mandatory_entry_pair = []
    for i, arg in enumerate(mand_inp.split()):
        label = customtkinter.CTkLabel(mandatory_frame, text=arg)
        label.grid(row=i, column=0, padx=(20, 0), pady=(0, 15), sticky="w")
        entry = customtkinter.CTkEntry(mandatory_frame, placeholder_text=f"Input {i+1}")
        entry.grid(row=i, column=1, padx=(20, 20), pady=(0, 15), sticky="nsew")
        mandatory_entry_pair.append([label, entry])
    
    optional_entry_pair = []
    if not pd.isna(opt_inp):
        for i, arg in enumerate(opt_inp.split()):
            label = customtkinter.CTkLabel(optional_frame, text=arg)
            label.grid(row=i, column=0, padx=(20, 0), pady=(0, 15), sticky="w")
            entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Input {i+1}")
            entry.grid(row=i, column=1, padx=(20, 20), pady=(0, 15), sticky="nsew")
            optional_entry_pair.append([label, entry])
        # for some optional inputs
        def add_entry_type1():
            entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children()) - 2*len(opt_inp.split())}")
            entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
            optional_entry_pair.append([f"Optional Input {len(optional_frame.winfo_children()) - len(opt_inp.split()) - 1}", entry])
        
        plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, command=add_entry_type1, border_width=1, corner_radius=28)
        plus_button.grid(row=len(opt_inp.split()), column=1, padx=20, pady=(0, 15), sticky="e")
    
    if pd.isna(opt_inp):
        # for no optional inputs
        def add_entry_type1():
            entry = customtkinter.CTkEntry(optional_frame, placeholder_text=f"Optional Input {len(optional_frame.winfo_children())}")
            entry.grid(row=len(optional_frame.winfo_children()), column=1, padx=20, pady=(0, 15), sticky="nsew")
            optional_entry_pair.append([f"Optional Input {len(optional_frame.winfo_children()) - 1}", entry])
        
        plus_button = customtkinter.CTkButton(optional_frame, text="+", width=40, command=add_entry_type1, border_width=1, corner_radius=28)
        plus_button.grid(row=0, column=1, padx=20, pady=(0,15), sticky="e")
    
    def check_mandatory():
        filled = all(mentry.get() for mlabel, mentry in mandatory_entry_pair)
        if filled:
            run_button.configure(state=customtkinter.NORMAL)
        else:
            run_button.configure(state=customtkinter.DISABLED)
    # button only available if mandatory fields are all filled 
    for mlabel, mentry in mandatory_entry_pair:
        mentry.bind("<Key>", lambda event, arg=mlabel: check_mandatory())

    # 2 X 1
    textbox1 = customtkinter.CTkTextbox(app, state='disabled', border_width=1, height=360)
    textbox1.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
    # Script help data    
    #help_data = subprocess.check_output("{} -h".format(script_path), shell=True)
    help_data = os.popen("{} -h".format(script_path)).read()
    textbox1.configure(state='normal')
    textbox1.insert("0.0", help_data)
    textbox1.configure(state='disabled')
    
    # run and print button commands 
    def construct_command():
        command = [script_path]
        # mandatory inputs
        if script_type == 1:
            for mlabel, mentry in mandatory_entry_pair:
                command.append(mlabel.cget('text'))
                command.append(mentry.get())
        elif script_type == 2:
            for mlabel, mentry in mandatory_entry_pair:
                command.append(mentry.get())
        # optional inputs 
        for olabel, oentry in optional_entry_pair:
            if oentry.get():
                if script_type == 1:
                    try:    
                        command.append(olabel.cget('text'))
                        command.append(oentry.get())
                    except Exception as e:
                        command.append(oentry.get())  
                if script_type == 2:
                    command.append(oentry.get())
        return command

    def run_command():
        current_directory = os.getcwd()
        # change directory
        working_dir = script_name
        if chng_entry.get():
            try:
                os.makedirs(os.path.join(chng_entry.get(), working_dir), exist_ok=True)
                os.chdir(os.path.join(chng_entry.get(), working_dir))
            except FileNotFoundError:
                print('The specified directory does not exist.')
        else:
            os.makedirs(working_dir, exist_ok=True)
            os.chdir(os.path.join(os.getcwd(), working_dir))
        
        # make .ucdprod
        if not checkbox_var.get():
            try:
                if '.ucdprod' in ucdprod_entry.get():
                    shutil.copy2(ucdprod_entry.get(), os.path.join(os.getcwd(), '.ucdprod'))
                    #with open(os.path.join(os.getcwd(), '.ucdprod'), 'a') as f:
                    #    f.write('python 3.10.4\n')
                    #f.close()
            except FileNotFoundError:
                print('The specified directory does not exist.')
        else:
            with open('.ucdprod', 'w') as f:
                for tlabel, tentry in tool_entry_pair1:
                    f.writelines([tlabel.cget('text'), " ", tentry.get(), '\n'])
                for tentry1, tentry2 in tool_entry_pair2:
                    f.writelines([tentry1.get(), " ", tentry2.get(), '\n'])
        
        with open('script.csh', 'w') as f:
            f.writelines(["#!/bin/csh", "\n"])
            f.writelines(['echo EXECUTING : ', " ".join(construct_command()), '\n'])
            f.write('echo ============================================================================================================================================\n')
            f.write("setenv UCDPRJDIR $PWD\n")
            f.write("eval `ukerEnv`\n")
            f.writelines([" ".join(construct_command()), '\n'])
            f.write('echo ============================================================================================================================================\n')
            f.write('echo FINISHED\n')
        
        os.system('chmod 755 script.csh')
        os.system('script.csh')
        #os.system("xfce4-terminal --hold --command='script.csh'")
        os.chdir(current_directory)

    def print_command():
        print(" ".join(construct_command()))
    # run button
    # 0 X 3 - 4 X 0
    run_button = customtkinter.CTkButton(input_frame.tab(script_name), text='Run', border_width=2, command=run_command, fg_color="green", hover_color="darkgreen", font=customtkinter.CTkFont(size=16, weight="bold"), height=50)
    run_button.grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsw")
    run_button.configure(state=customtkinter.DISABLED)
    # print button
    # 0 X 0 - 4 X 0
    print_button = customtkinter.CTkButton(input_frame.tab(script_name), text='Print\nCommand', border_width=2, command=print_command, fg_color="green", hover_color="darkgreen", font=customtkinter.CTkFont(size=14, weight="bold"), height=50)
    print_button.grid(row=6, column=1, padx=(0, 20), pady=(20, 20), sticky="nse")


def get_script(name, selected_category_button):
    global current_category_button
    # Reset color of the previously selected button
    if current_category_button:
        current_category_button.configure(fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"])  # customtkinter default color
    # Change color of the currently selected button
    selected_category_button.configure(fg_color="green", hover_color="darkgreen")
    current_category_button = selected_category_button

    for widget in script_frame.winfo_children():
        widget.destroy()

    # selected category dataframe
    category_df = df.loc[df["Category"] == name]
    for i in category_df.itertuples():
        script_button = customtkinter.CTkButton(script_frame, text=os.path.basename(i[2]))
        script_button.configure(command=lambda mand_inp=i[3], opt_inp=i[4], script_type=i[5], script_path=i[2], tools_inp=i[7], button=script_button, info=i[8]: inputs(mand_inp, opt_inp, script_type, script_path, tools_inp, button, info))
        script_button.grid(row=i[0], column=0, padx=20, pady=(0, 20), sticky='nsew')
    #print(category_df)


###################### main ######################
app = customtkinter.CTk()
app.title("\U0001F6FAmation Hub")
app.geometry(f"{1200}x{700}")

iconpath = ImageTk.PhotoImage(file="/work/LIPAS/USER_AREAS/BHUPENDRA/CMOSE40ULP/CMOSE40ULP_CONV_ADC_SA_12b_5Msps_S_H_OD25_7m4x2zAP@1.0-INTERM-00/TEMP/automation_light.png")
app.wm_iconbitmap()
app.iconphoto(False, iconpath)

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

# sidebar 0 X 0
sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)

logo_image = customtkinter.CTkImage(dark_image=Image.open('/work/LIPAS/USER_AREAS/BHUPENDRA/CMOSE40ULP/CMOSE40ULP_CONV_ADC_SA_12b_5Msps_S_H_OD25_7m4x2zAP@1.0-INTERM-00/TEMP/automation_light.png'), light_image=Image.open('/work/LIPAS/USER_AREAS/BHUPENDRA/CMOSE40ULP/CMOSE40ULP_CONV_ADC_SA_12b_5Msps_S_H_OD25_7m4x2zAP@1.0-INTERM-00/TEMP/automation_dark.png'), size=((80, 80)))
logo_label = customtkinter.CTkLabel(sidebar_frame, text="CAD\nAutomation\nHub", font=customtkinter.CTkFont(size=24, weight="bold"), image=logo_image, compound=customtkinter.TOP)
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
category_frame = customtkinter.CTkScrollableFrame(app, label_text="CATEGORY", label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"), height=290)
category_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
category_frame.grid_columnconfigure(0, weight=1)

current_category_button = None
current_script_button = None
for i, category in enumerate(df['Category'].unique()):
    category_button = customtkinter.CTkButton(category_frame, text=category)
    category_button.configure(command=lambda name=category, button=category_button: get_script(name, button))
    category_button.grid(row=i, column=0, padx=20, pady=(0, 20), sticky='nsew')

# 0 X 2
script_frame = customtkinter.CTkScrollableFrame(app, label_text="SCRIPT", label_fg_color='transparent', label_font=customtkinter.CTkFont(size=14, weight="bold"))
script_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
script_frame.grid_columnconfigure(0, weight=1)

# 0 X 3
input_frame = customtkinter.CTkTabview(app, border_width=1, width=420)
input_frame.grid(row=0, column=3, rowspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew")
input_frame.grid_columnconfigure(0, weight=1)

# 1 X 2
tools_frame = customtkinter.CTkScrollableFrame(app, label_text="TOOLS", label_font=customtkinter.CTkFont(size=14, weight="bold"))#, label_fg_color='transparent')
tools_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
tools_frame.grid_columnconfigure(0, weight=1)

# 2 X 1
textbox1 = customtkinter.CTkTextbox(app, state='disabled', border_width=1, height=360)
textbox1.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

# defaults
appearance_mode_optionemenu.set("Dark")
scaling_optionemenu.set("100%")
input_frame.add('INPUT')

app.mainloop()
