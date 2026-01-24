#-------------------------------------------------------DETECT_PAGE------------------------------------------------------#
#frame packages
import os
import time
import threading
from tkinter import *
from tkinter import messagebox
#class packages
import get_set_Data as app
import choose_page as choose
import s_f_d_c_Data as search
#------------------------------------------------------------------------------->Global
#were we stoke all images
dbs=None
#the location of the folder
main_folder=None
#the location of videos
videos_path=None
#index for element we are looking for 
index_value=None
#------------------------------------------------------------------------------->faces
#frame for faces/images
def faces_images():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        FI_frame = Tk()
        # Variables
        look_for_faces= StringVar()
        gathering_images=StringVar()
        result=StringVar()
        timeP=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def check_faces():
            try:
                #clean compare folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #get path to face images
                file=app.get_path_to_faces_image()
                #if we select an image
                if len(file[0]) > 0:
                   #button faces
                   faces_button.config(state=DISABLED)
                   #color for facesLabel
                   facesLabel.config(fg=app.get_hex_green_color())
                   #look_for_faces
                   look_for_faces.set(f"The program is searching faces in  {file[1]}.........{app.get_wait_unicode()}")#what we start with 
                   #update in frame
                   FI_frame.update_idletasks()
                   #wait to start searching
                   time.sleep(3)
                   #search
                   response=search.search_faces_for_image(file[0],file[1],app.path_to_faces_images)
                   if response[0]:#if we found image
                      look_for_faces.set(response[1]) 
                      folder_button.config(state=NORMAL)
                   else:
                       raise Exception(response[1])  
                   #show image
                   threading.Thread(target=search.display_images,args=([{"path":response[2],"title":f"Face(s) detected for {file[1]}","position":0}],False)).start()    
                else:   
                   raise Exception ("Nothing selected")   
            except Exception as e:
                look_for_faces.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                facesLabel.config(fg="red")
                faces_button.config(state=NORMAL)
        #close 
        def quit_all():
            FI_frame.destroy() #close the frame
            os._exit(0) #close the process           
        # Button(for faces)
        faces_button = Button(FI_frame, text=f"{app.get_images_unicode()}  Please select an image with faces to detect", command=check_faces,
                        font=app.get_button_font(),
                        width=52, height=2,
                        bg=app.get_hex_green_color(),
                        fg=app.get_hex_white_color())
        faces_button.pack(pady=20)
        #faces label
        facesLabel = Label(FI_frame, textvariable=look_for_faces, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        facesLabel.pack(pady=3)
        #get dbs
        def get_dbs():
            global dbs
            global main_folder
            try:
                path_dbs=app.get_path_to_folder()
                if len(path_dbs[0]) > 0:
                   #color
                   gatherLabel.config(fg=app.get_hex_green_color())
                   #button faces
                   folder_button.config(state=DISABLED)
                   #gathering label
                   gathering_images.set(f"Gathering images from {path_dbs[1]}.... {app.get_wait_unicode()}")  
                   #update in frame
                   FI_frame.update_idletasks()
                   #time to wait
                   time.sleep(3)
                   #gathering images
                   dbs=app.get_images_from_folder(path_dbs[0])
                   if len(dbs) > 0 :
                      gathering_images.set(f"The program found  {len(dbs)} usable images {app.get_images_unicode()} from {path_dbs[1]}")
                      main_folder=path_dbs[0]
                      detect_button.config(state=NORMAL)
                   else:
                      raise Exception (f"The program found 0 image for folder {path_dbs[1]}")     
                else:
                    raise Exception ("Nothing selected") 
            except Exception as e:
                gathering_images.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                gatherLabel.config(fg="red")
                folder_button.config(state=NORMAL)
        # Button(for folder)        
        folder_button = Button(FI_frame, text=f"{app.get_folder_unicode()}  Please select the database (folder)",
                               command=get_dbs,state=DISABLED,       
                               font=app.get_button_font(),
                               width=52, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        folder_button.pack(pady=30)
        #gather label
        gatherLabel = Label(FI_frame, textvariable=gathering_images, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        gatherLabel.pack(pady=3)
         #detect 
        def detect():
            try:
                #disable bouton
                detect_button.config(state=DISABLED)
                #set result
                result.set(f"We are checking each image from {os.path.basename(main_folder)}.....{app.get_wait_unicode()}")
                #timeP
                timeP.set("It may take some time depending on the number of images")
                #update frame
                FI_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(1)
                #start
                start_time=time.time()
                #we get results from searching
                results=search.find_faces_in_dbs(dbs,main_folder,app.path_to_faces_images)
                #end
                end_time=time.time()
                if len(results) > 0:
                    result.set(f"We found {len(results)} possible matches")
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    #show result
                    threading.Thread(target=search.display_images,args=(results,True)).start()
                    #another try
                    faces_button.config(state=NORMAL)
                else:
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    folder_button.config(state=NORMAL)
                    detect_button.config(state=DISABLED)
                    raise Exception("No match found .Please try another folder") 
            except Exception as e:
                result.set(f"{e}")
                resultLabel.config(fg="red")
        # start Detecting         
        detect_button = Button(FI_frame, text=f"{app.get_start_unicode()}  Detect faces ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=20)
        
        #result label
        resultLabel = Label(FI_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        #time label
        timeLabel = Label(FI_frame, textvariable=timeP, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        timeLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                FI_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")  
        back_button = Button(FI_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=20)
        # Window settings
        FI_frame.iconphoto(True, icon)
        FI_frame.title(app.get_title())
        FI_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        FI_frame.resizable(False, False)
        FI_frame.config(background=app.get_hex_white_color())
        FI_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        FI_frame.mainloop()
    except Exception as e:
        messagebox.showerror(title="Error",message=f"Error : {e}")  
#frame for faces/videos
def faces_videos():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        FV_frame = Tk()
        # Variables
        look_for_faces= StringVar()
        videos_str=StringVar()
        result_str=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def check_faces():
            try:
                #clean compare folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #get path to face images
                file=app.get_path_to_faces_image()
                #if we select an image
                if len(file[0]) > 0:
                   #button faces
                   faces_button.config(state=DISABLED)
                   #color for facesLabel
                   facesLabel.config(fg=app.get_hex_green_color())
                   #look_for_faces
                   look_for_faces.set(f"The program is searching faces in  {file[1]}.........{app.get_wait_unicode()}")#what we start with 
                   #update in frame
                   FV_frame.update_idletasks()
                   #wait to start searching
                   time.sleep(3)
                   #search
                   response=search.search_faces_for_image(file[0],file[1],app.path_to_faces_videos)
                   if response[0]:#if we found image
                      look_for_faces.set(response[1]) 
                      video_button.config(state=NORMAL)
                   else:
                       raise Exception(response[1])  
                    #show image
                   threading.Thread(target=search.display_images,args=([{"path":response[2],"title":f"Face(s) detected for {file[1]}","position":0}],False)).start()    
                else:   
                   raise Exception ("Nothing selected")   
            except Exception as e:
                look_for_faces.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                facesLabel.config(fg="red")
                faces_button.config(state=NORMAL)
        #close
        def quit_all():
            FV_frame.destroy() #close the frame
            os._exit(0) #close the process            
        # Button(for faces)
        faces_button = Button(FV_frame, text=f"{app.get_images_unicode()}  Please select an image with faces to detect", 
                              command=check_faces,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        faces_button.pack(pady=20)
        #faces label
        facesLabel = Label(FV_frame, textvariable=look_for_faces, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        facesLabel.pack(pady=3)
        #get dbs
        def get_videos():
            global videos_path
            try:
                videos_path=app.get_path_videos()
                if len(videos_path[0]) > 0:
                   #color
                   videoLabel.config(fg=app.get_hex_green_color())
                   #button video
                   video_button.config(state=DISABLED)
                   #change label
                   videos_str.set(f"The program is ready to detect faces in {videos_path[1]}")  
                   #detect
                   detect_button.config(state=NORMAL)
                   #update in frame
                   FV_frame.update_idletasks()
                else:
                    raise Exception ("Nothing selected") 
            except Exception as e:
                videos_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                videoLabel.config(fg="red")
                video_button.config(state=NORMAL)
        # Button(video)        
        video_button = Button(FV_frame, text=f"{app.get_folder_unicode()}  Please select a video ",
                              command=get_videos,state=DISABLED,       
                              font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        video_button.pack(pady=30)
        #video label
        videoLabel = Label(FV_frame, textvariable=videos_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        videoLabel.pack(pady=3)
        #detect 
        def detect():
            try:
                #disable bouton
                detect_button.config(state=DISABLED)
                #set result
                result_str.set(f"We are checking each face in {videos_path[1]}.....{app.get_wait_unicode()}")
                #update frame
                FV_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(1)
                #start
                threading.Thread(target=search.find_faces_in_VW,args=(app.path_to_faces_videos,os.path.join(app.path_to_compare_images,"work_video"),
                                        f"Reading video.... Tape 'q' to quit",videos_path[0],result_str)).start()
            except Exception as e:
                result_str.set(f"{e}")
                resultLabel.config(fg="red")

        # start Detecting         
        detect_button = Button(FV_frame, text=f"{app.get_start_unicode()}  Detect faces ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=20)
        #result label
        resultLabel = Label(FV_frame, textvariable=result_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                FV_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")          
        back_button = Button(FV_frame, text=f"{app.get_back_unicode()}  Back",
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=20)
        # Window settings
        FV_frame.iconphoto(True, icon)
        FV_frame.title(app.get_title())
        FV_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        FV_frame.resizable(False, False)
        FV_frame.config(background=app.get_hex_white_color())
        FV_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        FV_frame.mainloop()
    except Exception as e:
        messagebox.showerror(title="Error",message=f"Error : {e}")  
#frame for faces/webcam
def faces_webcam():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        FW_frame = Tk()
        # Variables
        look_for_faces= StringVar()
        result_str=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def check_faces():
            try:
                #clean compare folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #get path to face images
                file=app.get_path_to_faces_image()
                #if we select an image
                if len(file[0]) > 0:
                   #button faces
                   faces_button.config(state=DISABLED)
                   #color for facesLabel
                   facesLabel.config(fg=app.get_hex_green_color())
                   #look_for_faces
                   look_for_faces.set(f"The program is searching faces in  {file[1]}.........{app.get_wait_unicode()}")#what we start with 
                   #update in frame
                   FW_frame.update_idletasks()
                   #wait to start searching
                   time.sleep(3)
                   #search
                   response=search.search_faces_for_image(file[0],file[1],app.path_to_faces_webcam)
                   if response[0]:#if we found image
                      look_for_faces.set(response[1]) 
                      detect_button.config(state=NORMAL)
                   else:
                       raise Exception(response[1])  
                   #show image
                   threading.Thread(target=search.display_images,args=([{"path":response[2],"title":f"Face(s) detected for {file[1]}","position":0}],False)).start()
                else:   
                   raise Exception ("Nothing selected")   
            except Exception as e:
                look_for_faces.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                facesLabel.config(fg="red")
                faces_button.config(state=NORMAL)
        #close 
        def quit_all():
            FW_frame.destroy() #close the frame
            os._exit(0) #close the process        
        # Button(for faces)
        faces_button = Button(FW_frame, text=f"{app.get_images_unicode()}  Please select an image with faces to detect", 
                              command=check_faces,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        faces_button.pack(pady=50)
        
        #faces label
        facesLabel = Label(FW_frame, textvariable=look_for_faces, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        facesLabel.pack(pady=5)
        #detect 
        def detect():
            try:
                #disable bouton
                detect_button.config(state=DISABLED)
                #set result
                result_str.set(f"We checking each face from the webcam ...{app.get_wait_unicode()}")
                #update frame
                FW_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(1)
                #start
                threading.Thread(target=search.find_faces_in_VW,args=(app.path_to_faces_webcam,os.path.join(app.path_to_compare_images,"work_webcam"),
                                        f"Reading webcam.... Tape 'q' to quit","",result_str)).start()
            except Exception as e:
                result_str.set(f"{e}")
                resultLabel.config(fg="red")
                detect_button.config(state=NORMAL)

        # start Detecting         
        detect_button = Button(FW_frame, text=f"{app.get_start_unicode()}  Detect faces ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=50)
        #result label
        resultLabel = Label(FW_frame, textvariable=result_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=5)
        # back  
        def back():   
            try:
                #close
                FW_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")         
        back_button = Button(FW_frame, text=f"{app.get_back_unicode()}  Back",
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=40)
        # Window settings
        FW_frame.iconphoto(True, icon)
        FW_frame.title(app.get_title())
        FW_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        FW_frame.resizable(False, False)
        FW_frame.config(background=app.get_hex_white_color())
        FW_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        FW_frame.mainloop()
    except Exception as e:
        messagebox.showerror(title="Error",message=f"Error : {e}")  

#-------------------------------------------------------------------------------------->Objects (IVW)
#frame for Objects/images
def objects_images():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        OI_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        result=StringVar()
        timeP=StringVar()
        gathering_images=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the file in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    OI_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Objets()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            OI_frame.destroy() #close the frame
            os._exit(0) #close the process         
        # Button(for save)
        save_button = Button(OI_frame, text=f"{app.get_objects_unicode()}  Download the list of objects we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=5)
        #save label
        saveLabel = Label(OI_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=3)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #loof for the entry index
                 index=app.getIndexFor(entry.get(),app.get_Objets())
                 if  index != -1 : 
                     index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     folder_button.config(state=NORMAL)
                     index_value=index
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(OI_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name of object")
        # Button(for Get Index)
        get_button = Button(OI_frame, text=f"{app.get_objects_unicode()} Get index for the object", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        #index label
        indexLabel = Label(OI_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=3)
        #get dbs
        def get_dbs():
            global dbs
            global main_folder
            try:
                path_dbs=app.get_path_to_folder()
                if len(path_dbs[0]) > 0:
                   #color
                   gatherLabel.config(fg=app.get_hex_green_color())
                   #button faces
                   folder_button.config(state=DISABLED)
                   #gathering label
                   gathering_images.set(f"Gathering images from {path_dbs[1]}.... {app.get_wait_unicode()}")  
                   #update in frame
                   OI_frame.update_idletasks()
                   #time to wait
                   time.sleep(3)
                   #gathering images
                   dbs=app.get_images_from_folder(path_dbs[0])
                   if len(dbs) > 0 :
                      gathering_images.set(f"The program found  {len(dbs)} usable images {app.get_images_unicode()} from {path_dbs[1]}")
                      main_folder=path_dbs[0]
                      detect_button.config(state=NORMAL)
                   else:
                      raise Exception (f"The program found 0 images for folder {path_dbs[1]}")     
                else:
                    raise Exception ("Nothing selected") 
            except Exception as e:
                gathering_images.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                gatherLabel.config(fg="red")
                folder_button.config(state=NORMAL)
        # Button(for folder)        
        folder_button = Button(OI_frame, text=f"{app.get_folder_unicode()}  Please select the database (folder)",
                               command=get_dbs,state=DISABLED,       
                               font=app.get_button_font(),
                               width=52, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        folder_button.pack(pady=5)
        #gather label
        gatherLabel = Label(OI_frame, textvariable=gathering_images, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        gatherLabel.pack(pady=3)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #disable bouton
                detect_button.config(state=DISABLED)
                #set result
                result.set(f"We are looking for index {index_value} in each image from {os.path.basename(main_folder)}.....{app.get_wait_unicode()}")
                #timeP
                timeP.set("It may take some time depending on the number of images")
                #update frame
                OI_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(3)
                #start
                start_time=time.time()
                #we get results from searching
                results=search.find_object_in_dbs(dbs,index_value,os.path.join(app.path_to_compare_images,"OI_DBS"))
                #end
                end_time=time.time()
                if len(results) > 0:
                    result.set(f"We found {len(results)} possible matches")
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    #show result
                    threading.Thread(target=search.display_images,args=(results,False)).start()
                    #another try
                    entry.config(state=NORMAL)
                    get_button.config(state=NORMAL)
                else:
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    detect_button.config(state=DISABLED)
                    raise Exception("No match found .Please try another folder") 
            except Exception as e:
                result.set(f"{e}")
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                folder_button.config(state=DISABLED)
                detect_button.config(state=DISABLED)
        # start Detecting         
        detect_button = Button(OI_frame, text=f"{app.get_start_unicode()}  Detect Object ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=5)
        
        #result label
        resultLabel = Label(OI_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        #time label
        timeLabel = Label(OI_frame, textvariable=timeP, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        timeLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                OI_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")     
        back_button = Button(OI_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        OI_frame.iconphoto(True, icon)
        OI_frame.title(app.get_title())
        OI_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        OI_frame.resizable(False, False)
        OI_frame.config(background=app.get_hex_white_color())
        OI_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        OI_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")

#frame for Objects/videos
def objects_videos():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        OV_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        videos_str=StringVar()
        result=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the program in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    OV_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Objets()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
                
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            OV_frame.destroy() #close the frame
            os._exit(0) #close the process                    
        # Button(for save)
        save_button = Button(OV_frame, text=f"{app.get_objects_unicode()}  Download the list of objects we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=5)
        #save label
        saveLabel = Label(OV_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=3)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #update
                 OV_frame.update_idletasks()
                 #value
                 value=entry.get()
                 if  value != "all" : 
                     #loof for the entry index
                     index=app.getIndexFor(entry.get(),app.get_Objets())  
                     if index != -1:
                        index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                        indexLabel.config(fg=app.get_hex_green_color())   
                        index_value=index
                        video_button.config(state=NORMAL)
                     else:
                        raise Exception("No index found ")     
                 elif value == "all":
                     index_str.set(f"We are going to detect all objects {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     index_value=value
                     video_button.config(state=NORMAL)
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(OV_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name or all")
        # Button(for Get Index)
        get_button = Button(OV_frame, text=f"{app.get_objects_unicode()} Get index for the object", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        
        #index label
        indexLabel = Label(OV_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=3)
        #get dbs
        def get_videos():
            global videos_path
            try:
                videos_path=app.get_path_videos()
                if len(videos_path[0]) > 0:
                   #color
                   videoLabel.config(fg=app.get_hex_green_color())
                   #button video
                   video_button.config(state=DISABLED)
                   #change label
                   videos_str.set(f"The program is ready to detect objects in {videos_path[1]}")  
                   #detect
                   detect_button.config(state=NORMAL)
                   #update in frame
                   OV_frame.update_idletasks()
                else:
                    raise Exception ("Nothing selected") 
                   
            except Exception as e:
                videos_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                videoLabel.config(fg="red")
                video_button.config(state=NORMAL)
        # Button(video)        
        video_button = Button(OV_frame, text=f"{app.get_folder_unicode()}  Please select a video ",
                              command=get_videos,state=DISABLED,       
                              font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        video_button.pack(pady=5)
        #video label
        videoLabel = Label(OV_frame, textvariable=videos_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        videoLabel.pack(pady=3)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #disable bouton
                detect_button.config(state=DISABLED)
                #result
                if index_value == "all":
                   result.set(f"We are looking for each objects in {videos_path[1]}.....{app.get_wait_unicode()}")
                   threading.Thread(target=search.find_objects_VWA,args=(videos_path[0], f"Reading video.... Tape 'q' to quit",result)).start()
                else:
                   result.set(f"We are looking for object {index_value} in {videos_path[1]}.....{app.get_wait_unicode()}")    
                   #show
                   threading.Thread(target=search.find_objects_VWI,args=(index_value,videos_path[0], f"Reading video.... Tape 'q' to quit",result)).start()
                #update
                OV_frame.update_idletasks()
               
            except Exception as e:
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                video_button.config(state=DISABLED)
                detect_button.config(state=DISABLED)
        # start Detecting         
        detect_button = Button(OV_frame, text=f"{app.get_start_unicode()}  Detect Object ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=5)
        
        #result label
        resultLabel = Label(OV_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                OV_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")    
        back_button = Button(OV_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        OV_frame.iconphoto(True, icon)
        OV_frame.title(app.get_title())
        OV_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        OV_frame.resizable(False, False)
        OV_frame.config(background=app.get_hex_white_color())
        OV_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        OV_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")
#frame for Objects/Webcam
def objects_webcam():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        OW_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        result=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the program in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    OW_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Objets()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            OW_frame.destroy() #close the frame
            os._exit(0) #close the process                     
        # Button(for save)
        save_button = Button(OW_frame, text=f"{app.get_objects_unicode()}  Download the list of objects we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=30)
        #save label
        saveLabel = Label(OW_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=5)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #update
                 OW_frame.update_idletasks()
                 #value
                 value=entry.get()
                 if  value != "all" : 
                     #loof for the entry index
                     index=app.getIndexFor(entry.get(),app.get_Objets())  
                     if index != -1:
                        index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                        indexLabel.config(fg=app.get_hex_green_color())   
                        index_value=index
                        detect_button.config(state=NORMAL)
                     else:
                        raise Exception("No index found ")     
                 elif value == "all":
                     index_str.set(f"We are going to detect all objects {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     index_value=value
                     detect_button.config(state=NORMAL)
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(OW_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name or all")
        # Button(for Get Index)
        get_button = Button(OW_frame, text=f"{app.get_objects_unicode()} Get index for the object", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        #faces label
        indexLabel = Label(OW_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=5)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #disable bouton
                detect_button.config(state=DISABLED)
                #result
                if index_value == "all":
                   result.set(f"We are looking for each objects in webcam.....{app.get_wait_unicode()}")
                   threading.Thread(target=search.find_objects_VWA,args=("", f"Reading video.... Tape 'q' to quit",result)).start()
                else:
                   result.set(f"We are looking for object {index_value} in webcam.....{app.get_wait_unicode()}")    
                   #show
                   threading.Thread(target=search.find_objects_VWI,args=(index_value,"", f"Reading video.... Tape 'q' to quit",result)).start()
                #update
                OW_frame.update_idletasks()
               
            except Exception as e:
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                detect_button.config(state=DISABLED)
        # start Detecting         
        detect_button = Button(OW_frame, text=f"{app.get_start_unicode()}  Detect Object ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=30)
        #result label
        resultLabel = Label(OW_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=5)
        # back  
        def back():   
            try:
                #close
                OW_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")      
        back_button = Button(OW_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        OW_frame.iconphoto(True, icon)
        OW_frame.title(app.get_title())
        OW_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        OW_frame.resizable(False, False)
        OW_frame.config(background=app.get_hex_white_color())
        OW_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        OW_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")
  
#-------------------------------------------------------------------------------------->Micro expressions (IVW)
#frame for Micro/images
def micro_images():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        MI_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        result=StringVar()
        timeP=StringVar()
        gathering_images=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the file in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    MI_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Expressions()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close        
        def quit_all():
            MI_frame.destroy() #close the frame
            os._exit(0) #close the process  
        # Button(for save)
        save_button = Button(MI_frame, text=f"{app.get_objects_unicode()}  Download the list of expressions we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=5)
        #save label
        saveLabel = Label(MI_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=3)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #loof for the entry index
                 index=app.getIndexFor(entry.get(),app.get_Expressions())
                 if  index != -1 : 
                     index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     folder_button.config(state=NORMAL)
                     index_value=index
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(MI_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name of expression")
        # Button(for Get Index)
        get_button = Button(MI_frame, text=f"{app.get_objects_unicode()} Get index for the expression", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        
        #index label
        indexLabel = Label(MI_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=3)
        #get dbs
        def get_dbs():
            global dbs
            global main_folder
            try:
                path_dbs=app.get_path_to_folder()
                if len(path_dbs[0]) > 0:
                   #color
                   gatherLabel.config(fg=app.get_hex_green_color())
                   #button faces
                   folder_button.config(state=DISABLED)
                   #gathering label
                   gathering_images.set(f"Gathering images from {path_dbs[1]}.... {app.get_wait_unicode()}")  
                   #update in frame
                   MI_frame.update_idletasks()
                   #time to wait
                   time.sleep(3)
                   #gathering images
                   dbs=app.get_images_from_folder(path_dbs[0])
                   if len(dbs) > 0 :
                      gathering_images.set(f"The program found  {len(dbs)} usable images {app.get_images_unicode()} from {path_dbs[1]}")
                      main_folder=path_dbs[0]
                      detect_button.config(state=NORMAL)
                   else:
                      raise Exception (f"The program found 0 images for folder {path_dbs[1]}")     
                else:
                    raise Exception ("Nothing selected") 
            except Exception as e:
                gathering_images.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                gatherLabel.config(fg="red")
                folder_button.config(state=NORMAL)
        # Button(for folder)        
        folder_button = Button(MI_frame, text=f"{app.get_folder_unicode()}  Please select the database (folder)",
                               command=get_dbs,state=DISABLED,       
                               font=app.get_button_font(),
                               width=52, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        folder_button.pack(pady=5)
        #gather label
        gatherLabel = Label(MI_frame, textvariable=gathering_images, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        gatherLabel.pack(pady=3)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #disable bouton
                detect_button.config(state=DISABLED)
                #color
                resultLabel.config(fg=app.get_hex_green_color())
                #set result
                result.set(f"We are looking for index {index_value} in each image from {os.path.basename(main_folder)}.....{app.get_wait_unicode()}")
                #timeP
                timeP.set("It may take some time depending on the number of images")
                #update frame
                MI_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(3)
                #start
                start_time=time.time()
                #we get results from searching
                results=search.find_micro_in_dbs(dbs,index_value,os.path.join(app.path_to_compare_images,"MI_DBS"))
                #end
                end_time=time.time()
                if len(results) > 0:
                    result.set(f"We found {len(results)} possible matches")
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    #show result
                    threading.Thread(target=search.display_images,args=(results,False)).start()
                    #another try
                    entry.config(state=NORMAL)
                    get_button.config(state=NORMAL)
                else:
                    timeP.set(f"Search time : {int((end_time-start_time)//60)} minutes")
                    detect_button.config(state=DISABLED)
                    raise Exception("No match found .Please try again")    
            except Exception as e:
                result.set(f"{e}")
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                folder_button.config(state=DISABLED)
                detect_button.config(state=DISABLED)
        # start Detecting         
        detect_button = Button(MI_frame, text=f"{app.get_start_unicode()}  Detect expression ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=5)
        
        #result label
        resultLabel = Label(MI_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        #time label
        timeLabel = Label(MI_frame, textvariable=timeP, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        timeLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                MI_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")      
        back_button = Button(MI_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        MI_frame.iconphoto(True, icon)
        MI_frame.title(app.get_title())
        MI_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        MI_frame.resizable(False, False)
        MI_frame.config(background=app.get_hex_white_color())
        MI_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        MI_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")

#frame for micro/videos
def micro_videos():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        MV_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        videos_str=StringVar()
        result=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()

                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the file in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    MV_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Expressions()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            MV_frame.destroy() #close the frame
            os._exit(0) #close the process          
                
        # Button(for save)
        save_button = Button(MV_frame, text=f"{app.get_objects_unicode()}  Download the list of expressions we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=5)
        
        #save label
        saveLabel = Label(MV_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=3)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #update
                 MV_frame.update_idletasks()
                 #value
                 value=entry.get()
                 if  value != "all" : 
                     #loof for the entry index
                     index=app.getIndexFor(entry.get(),app.get_Expressions())  
                     if index != -1:
                        index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                        indexLabel.config(fg=app.get_hex_green_color())   
                        index_value=index
                        video_button.config(state=NORMAL)
                     else:
                        raise Exception("No index found ")     
                 elif value == "all":
                     index_str.set(f"We are going to detect all expressions {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     index_value=value
                     video_button.config(state=NORMAL)
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
                 
        #Entry box
        entry=Entry(MV_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name or all")
        # Button(for Get Index)
        get_button = Button(MV_frame, text=f"{app.get_objects_unicode()} Get index for the expression", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        
        #index label
        indexLabel = Label(MV_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=3)
        #get dbs
        def get_videos():
            global videos_path
            try:
                videos_path=app.get_path_videos()

                if len(videos_path[0]) > 0:
                   #color
                   videoLabel.config(fg=app.get_hex_green_color())
                   #button video
                   video_button.config(state=DISABLED)
                   #change label
                   videos_str.set(f"The program is ready to detect expressions in {videos_path[1]}")  
                   #detect
                   detect_button.config(state=NORMAL)
                   #update in frame
                   MV_frame.update_idletasks()
                else:
                    raise Exception ("Nothing selected") 
                   
            except Exception as e:
                videos_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                videoLabel.config(fg="red")
                video_button.config(state=NORMAL)
        # Button(video)        
        video_button = Button(MV_frame, text=f"{app.get_folder_unicode()}  Please select a video ",
                              command=get_videos,state=DISABLED,       
                              font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        video_button.pack(pady=5)
        #video label
        videoLabel = Label(MV_frame, textvariable=videos_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        videoLabel.pack(pady=3)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #color
                resultLabel.config(fg=app.get_hex_green_color())
                #disable bouton
                detect_button.config(state=DISABLED)
                #result
                if index_value == "all":
                   result.set(f"We are looking for each expression in {videos_path[1]}.....{app.get_wait_unicode()}")
                   threading.Thread(target=search.find_expressions_VWA,args=(videos_path[0], f"Reading video.... Tape 'q' to quit",result)).start()
                else:
                   result.set(f"We are looking for expression {index_value} in {videos_path[1]}.....{app.get_wait_unicode()}")    
                   #show
                   threading.Thread(target=search.find_expressions_VWI,args=(index_value,videos_path[0], f"Reading video.... Tape 'q' to quit",result)).start()
                #update
                MV_frame.update_idletasks()
               
            except Exception as e:
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                video_button.config(state=DISABLED)
                detect_button.config(state=DISABLED)
                

        # start Detecting         
        detect_button = Button(MV_frame, text=f"{app.get_start_unicode()}  Detect expression ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=5)
        
        #result label
        resultLabel = Label(MV_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        # back  
        def back():   
            try:
                #close
                MV_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}") 
        back_button = Button(MV_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        MV_frame.iconphoto(True, icon)
        MV_frame.title(app.get_title())
        MV_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        MV_frame.resizable(False, False)
        MV_frame.config(background=app.get_hex_white_color())
        MV_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        MV_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")

#frame for micro/Webcam
def micro_webcam():
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        MW_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        result=StringVar()
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the file in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    MW_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    load=app.set_file(path_file,app.get_String(app.get_Expressions()[1]))
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            MW_frame.destroy() #close the frame
            os._exit(0) #close the process         
        # Button(for save)
        save_button = Button(MW_frame, text=f"{app.get_objects_unicode()}  Download the list of expressions we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=30)
        #save label
        saveLabel = Label(MW_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=5)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #update
                 MW_frame.update_idletasks()
                 #value
                 value=entry.get()
                 if  value != "all" : 
                     #loof for the entry index
                     index=app.getIndexFor(entry.get(),app.get_Expressions())  
                     if index != -1:
                        index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                        indexLabel.config(fg=app.get_hex_green_color())   
                        index_value=index
                        detect_button.config(state=NORMAL)
                     else:
                        raise Exception("No index found ")     
                 elif value == "all":
                     index_str.set(f"We are going to detect all expressions {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     index_value=value
                     detect_button.config(state=NORMAL)
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(MW_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name or all")
        # Button(for Get Index)
        get_button = Button(MW_frame, text=f"{app.get_objects_unicode()} Get index for the expression", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        #index label
        indexLabel = Label(MW_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=5)
         #detect 
        def detect():
            try:
                #reset folder
                app.set_folder_to_empty(app.path_to_compare_images)
                #disable bouton
                detect_button.config(state=DISABLED)
                #result
                if index_value == "all":
                   result.set(f"We are looking for each expressions in webcam.....{app.get_wait_unicode()}")
                   threading.Thread(target=search.find_expressions_VWA,args=("", f"Reading video.... Tape 'q' to quit",result)).start()
                else:
                   result.set(f"We are looking for expression {index_value} in webcam.....{app.get_wait_unicode()}")    
                   #show
                   threading.Thread(target=search.find_expressions_VWI,args=(index_value,"", f"Reading video.... Tape 'q' to quit",result)).start()
                #update
                MW_frame.update_idletasks()
            except Exception as e:
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
                detect_button.config(state=DISABLED)
        # start Detecting         
        detect_button = Button(MW_frame, text=f"{app.get_start_unicode()}  Detect Expression ", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=30)
        #result label
        resultLabel = Label(MW_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=5)
        # back  
        def back():   
            try:
                #close
                MW_frame.destroy()
                #back to choose page
                choose.field_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")       
        back_button = Button(MW_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        MW_frame.iconphoto(True, icon)
        MW_frame.title(app.get_title())
        MW_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        MW_frame.resizable(False, False)
        MW_frame.config(background=app.get_hex_white_color())
        MW_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        MW_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")

#-------------------------------------------------------------------------------------->Objects and Micro expressions (S)
def object_micro_screen(choice):
    try:
        # Get frame bounds
        bounds = app.get_bounds()[1]
        # Create main window
        OMS_frame = Tk()
        # Variables
        save_str= StringVar()
        index_str=StringVar()
        result=StringVar()
        #check  choice
        if choice == "objects":
            elt= "object"
        else:
            elt="micro-expression"    
        # Images
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #check faces
        def save_file():
            try:
                #to get path to file
                path_file=app.get_path_file()
                if len(path_file) > 0:
                    #color
                    saveLabel.config(fg=app.get_hex_green_color())
                    #change save_str
                    save_str.set(f"We are loading the program in {os.path.basename(path_file)} ... {app.get_wait_unicode()}")
                    #update
                    OMS_frame.update_idletasks()
                    #time wait
                    time.sleep(3)
                    #load
                    if choice == "objects":
                        load=app.set_file(path_file,app.get_String(app.get_Objets()[1]))
                    else: 
                        load=app.set_file(path_file,app.get_String(app.get_Expressions()[1]))   
                    #if succeed
                    if load[0]:
                       #change save_str
                       save_str.set(f"Successful loaded  {app.get_congrat_unicode()} ") 
                    else:
                       raise Exception(load[1]) 
                else:
                    raise Exception("Nothing selected")    
                
            except Exception as e:
                save_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                saveLabel.config(fg="red")
        #close
        def quit_all():
            OMS_frame.destroy() #close the frame
            os._exit(0) #close the process                    
        # Button(for save)
        save_button = Button(OMS_frame, text=f"{app.get_objects_unicode()}  Download the list of {elt} we can detect", 
                              command=save_file,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        save_button.pack(pady=5)
        #save label
        saveLabel = Label(OMS_frame, textvariable=save_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        saveLabel.pack(pady=3)
        #get index
        def get_index():
            global index_value
            try:
                 #close entry
                 get_button.config(state=DISABLED)
                 #close entry
                 entry.config(state=DISABLED)
                 #update
                 OMS_frame.update_idletasks()
                 #value
                 value=entry.get()
                 if  value != "all" : 
                     #look for the entry index
                     if choice == "objects":
                        index=app.getIndexFor(entry.get(),app.get_Objets())
                     else: 
                        index=app.getIndexFor(entry.get(),app.get_Expressions())   
                     #check the index
                     if index != -1:
                        index_str.set(f"Index : {index} {app.get_congrat_unicode()}")
                        indexLabel.config(fg=app.get_hex_green_color())   
                        index_value=index
                        detect_button.config(state=NORMAL)
                     else:
                        raise Exception("No index found ")     
                 elif value == "all":
                     index_str.set(f"We are going to detect all {elt} {app.get_congrat_unicode()}")
                     indexLabel.config(fg=app.get_hex_green_color())   
                     index_value=value
                     detect_button.config(state=NORMAL)
                 else:
                     raise Exception("No index found ")   
            except Exception as e:
                 index_str.set(f"Error : {e} {app.get_cross_mark_unicode()}")
                 indexLabel.config(fg="red")
                 entry.config(state=NORMAL)    
                 get_button.config(state=NORMAL)
        #Entry box
        entry=Entry(OMS_frame,bg=app.get_hex_white_color(),
                    fg=app.get_hex_green_color(),font=app.get_entry_font(),
                    width=29)
        entry.pack(pady=5)
        entry.insert(0,"Enter a name or all")
        # Button(for Get Index)
        get_button = Button(OMS_frame, text=f"{app.get_objects_unicode()} Get index for the {elt}", 
                              command=get_index,font=app.get_button_font(),
                              width=52, height=2,
                              bg=app.get_hex_green_color(),
                              fg=app.get_hex_white_color())
        get_button.pack(pady=3)
        
        #index label
        indexLabel = Label(OMS_frame, textvariable=index_str, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        indexLabel.pack(pady=3)
        
         #detect 
        def detect():
            try:
                #color
                resultLabel.config(fg="green")
                #disable bouton
                detect_button.config(state=DISABLED)
                #set result
                result.set("With the upcoming frame you can drag or resize it but you can't go back")
                #update frame
                OMS_frame.update_idletasks()
                #wait 1 seconds before start
                time.sleep(3)
                #close frame 
                OMS_frame.destroy()
                #start
                search.launch_window(choice,index_value)
            except Exception as e:
                result.set(f"{e}")
                resultLabel.config(fg="red")
                entry.config(state=NORMAL)
                get_button.config(state=NORMAL)
               
                detect_button.config(state=DISABLED)
            
        # start Detecting         
        detect_button = Button(OMS_frame, text=f"{app.get_start_unicode()}  Detect {elt}", 
                               command=detect,state=DISABLED,
                               font=app.get_button_font(),
                               width=22, height=2,
                               bg=app.get_hex_green_color(),
                               fg=app.get_hex_white_color())
        detect_button.pack(pady=5)

        #result label
        resultLabel = Label(OMS_frame, textvariable=result, font=app.get_loading_font(), 
                          fg=app.get_hex_green_color(),bg=app.get_hex_white_color())
        resultLabel.pack(pady=3)
        
        # back  
        def back():   
            try:
                #close
                OMS_frame.destroy()
                #back to choose page
                choose.screen_page()
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error : {e}")    
        back_button = Button(OMS_frame, text=f"{app.get_back_unicode()}  Back", 
                             command=back,font=app.get_button_font(),
                             width=22, height=2,
                             bg=app.get_hex_green_color(),
                             fg=app.get_hex_white_color())
        back_button.pack(pady=5)
        # Window settings
        OMS_frame.iconphoto(True, icon)
        OMS_frame.title(app.get_title())
        OMS_frame.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        OMS_frame.resizable(False, False)
        OMS_frame.config(background=app.get_hex_white_color())
        OMS_frame.protocol("WM_DELETE_WINDOW", quit_all)
        #show 
        OMS_frame.mainloop()
    except Exception as e:    
        messagebox.showerror(title="Error",message=f"Error : {e}")
#-----------------------------------------------------------------------------------------------------------> I am L 