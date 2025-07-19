#-------------------------------------------------------HOMA_PAGE------------------------------------------------------#
#frame packages
from tkinter import *
from tkinter import messagebox
#class packages
import get_set_Data as app
import detect_page as detect
#command
command_selected=[]
#next page
def next_page():
     print(command_selected)
     if    command_selected[0] == "faces" and command_selected[1] == "images" :
           detect.faces_images()
     elif  command_selected[0] == "faces" and command_selected[1] == "videos" :
           detect.faces_videos()
     elif  command_selected[0] == "faces" and command_selected[1] == "webcam" :
           detect.faces_webcam()
     elif  command_selected[0] == "objects" and command_selected[1] == "images" :
           detect.objects_images()
     elif  command_selected[0] == "objects" and command_selected[1] == "videos" :
           detect.objects_videos()
     elif  command_selected[0] == "objects" and command_selected[1] == "webcam" :
           detect.objects_webcam()
     elif  command_selected[0] == "micro-expressions" and command_selected[1] == "images" :
           detect.micro_images()
     elif  command_selected[0] == "micro-expressions" and command_selected[1] == "videos" :
           detect.micro_videos() 
     else: 
           detect.micro_webcam()           
#tool_page
def tool_page():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        tool_frame = Tk()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        # Label
        label = Label(tool_frame, text=f"What you want to detect {command_selected[0]} on",
                      fg=app.get_hex_green_color(),bg=app.get_hex_white_color(),
                      font=app.get_title_font())
        label.pack(pady=20)
        #def next_step
        def next_step(choice):
            #global
            global command_selected
            try:
                #close frame
                tool_frame.destroy()
                #if back
                if choice=="back":
                    command_selected=[]
                    field_page()
                else:#next page
                    command_selected.append(choice)
                    next_page()
            except Exception as e:#info problem
                messagebox.showerror(title="Error",message=f"Error : {e}")
        # Button (images)
        images_button = Button(tool_frame, text=f"{app.get_images_unicode()}  Images", command=lambda: next_step("images"),
                              font=app.get_button_font(),
                              width=20, height=3,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        images_button.pack(pady=20)
        # Button (videos)
        videos_button = Button(tool_frame, text=f"{app.get_videos_unicode()}  Videos", command=lambda: next_step("videos"),
                                font=app.get_button_font(),
                                width=20, height=3,
                                bg=app.get_hex_green_color(),
                                fg=app.get_hex_white_color())
        videos_button.pack(pady=20)
        # Button (webcam)
        webcam_button = Button(tool_frame, text=f"{app.get_webcam_unicode()}  Webcam", command=lambda: next_step("webcam"),
                              font=app.get_button_font(),
                              width=20, height=3,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        webcam_button.pack(pady=20)
        # Button (webcam)
        back_button = Button(tool_frame, text=f"{app.get_back_unicode()}  Back", command=lambda: next_step("back"),
                              font=app.get_button_font(),
                              width=20, height=3,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        back_button.pack(pady=20)
        # Window settings
        tool_frame.iconphoto(True, icon)
        tool_frame.title(app.get_title())
        tool_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        tool_frame.resizable(False, False)
        tool_frame.config(background=app.get_hex_white_color())
        #show 
        tool_frame.mainloop()
    except Exception as e:
        messagebox.showerror(title="Error",message=f"Error : {e}")
#field frame
def field_page():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        field_frame = Tk()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        # Label
        label = Label(field_frame, text="Please choose what you want to detect",
                      fg=app.get_hex_green_color(),bg=app.get_hex_white_color(),
                      font=app.get_title_font())
        label.pack(pady=20)
        #next_step
        def next_step(choice):
            global command_selected
            try:
                #reset to empty
                command_selected=[]
                #add command
                command_selected.append(choice)
                #close frame
                field_frame.destroy()
                #next page
                tool_page()
            except Exception as e:#info problem
                messagebox.showerror(title="Error",message=f"Error : {e}")
        # Button (faces)
        faces_button = Button(field_frame, text=f"{app.get_face_unicode()}  Faces", command=lambda: next_step("faces"),
                              font=app.get_button_font(),
                              width=20, height=3,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        faces_button.pack(pady=30)
        # Button (Objects)
        objects_button = Button(field_frame, text=f"{app.get_objects_unicode()}  Objects", command=lambda: next_step("objects"),
                                font=app.get_button_font(),
                                width=20, height=3,
                                bg=app.get_hex_green_color(),
                                fg=app.get_hex_white_color())
        objects_button.pack(pady=30)
        # Button (micro expressions)
        micro_button = Button(field_frame, text=f"{app.get_micro_unicode()}  Micro-expressions", command=lambda: next_step("micro-expressions"),
                              font=app.get_button_font(),
                              width=20, height=3,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        micro_button.pack(pady=30)
        # Window settings
        field_frame.iconphoto(True, icon)
        field_frame.title(app.get_title())
        field_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        field_frame.resizable(False, False)
        field_frame.config(background=app.get_hex_white_color())
        #show 
        field_frame.mainloop()
    except Exception as e:
        messagebox.showerror(title="Error",message=f"Error : {e}")    
       
  