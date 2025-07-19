#-------------------------------------------------------LAUNCH_PAGE------------------------------------------------------#
#packages
import time
import threading  
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar,Style
#class packages
import get_set_Data as app
import checkInfo as check
import choose_page as next
#next page
def next_page():
    next.field_page()
# Launch frame
def launch_page():
    try:   
        #show logo
        logo=app.get_logo()
        if logo[0] :
           print(logo[1])
           
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        launch = Tk()
        # Variables
        percent = StringVar()
        task = StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        img = PhotoImage(file=app.get_path_to_logo(1))
        # Label image
        label = Label(launch, image=img, bg=app.get_hex_white_color())
        label.pack(pady=20)
        # Progress bar
        style=Style()
        style.theme_use('default')
        style.configure("L.Horizontal.TProgressbar", 
                         thickness=30, 
                         troughcolor=app.get_hex_white_color(),      
                         background=app.get_hex_green_color())       
        bar = Progressbar(launch, orient="horizontal", length=650,mode='determinate',
                          style="L.Horizontal.TProgressbar")
        bar.pack(pady=30)
        #percent label
        percent.set("0%")
        percentLabel = Label(launch, textvariable=percent, font=app.get_loading_font(), 
                             fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        percentLabel.pack(pady=10)
        #task label
        task.set(f"Checking information......... {app.get_wait_unicode()}")#what we start with 
        taskLabel = Label(launch, textvariable=task, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        taskLabel.pack(pady=5)
        # Function that updates progress bar
        def progress():
            time.sleep(3)
            tasks = [check.is_packages_installed, 
                     check.is_version_adapted, 
                     check.is_files_exists, 
                     check.is_objests_Expression_functional] #All task we have to do 
            checked=True #if no problem
            #checking each task
            for x in range(len(tasks)):
                #time to wait
                time.sleep(2)
                #checking task
                taskLoad=tasks[x]()
                if not taskLoad[0]:
                   task.set(f"{taskLoad[1]} {app.get_cross_mark_unicode()}")
                   checked=False
                   taskLabel.config(fg="red")
                   break
                #making move the bar progress
                bar["value"] = (x + 1) * 25
                percent.set(f"{(x + 1) * 25}%")
                task.set(f"{taskLoad[1]} {app.get_check_unicode()}")   
                #update
                launch.update_idletasks()
            #if not problem we can start the program
            if checked:
               time.sleep(3)
               task.set(f"The program is ready to start  {app.get_smile_unicode()}")
               button.config(state=NORMAL)    
        # Avoid blocking the app
        def start_progress():
            threading.Thread(target=progress).start()
        #start_app
        def start_app():
            try:
                #close frame
                launch.destroy()
                #next page
                next_page()
            except Exception as e:#info problem
                messagebox.showerror(title="Error",message=f"Error : {e}")  
        # Button
        button = Button(launch, text=f"{app.get_start_unicode()} Start", command=start_app,
                        font=app.get_button_font(),
                        width=12, height=2,state=DISABLED,
                        bg=app.get_hex_green_color(),
                        fg=app.get_hex_white_color())
        button.pack(pady=60)
        # Window settings
        launch.iconphoto(True, icon)
        launch.title(app.get_title())
        launch.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        launch.resizable(False, False)
        launch.config(background=app.get_hex_white_color())
        #start
        start_progress()
        #show 
        launch.mainloop()
    except Exception as e:
           messagebox.showerror(title="Error",message=f"Error : {e}")  

