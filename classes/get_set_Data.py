#------------------------------------------------------GET-SET-DATA---------------------------------------------------#
import os
import glob
import shutil
import pickle as pick
from tkinter import Tk, filedialog,messagebox

#------------------------------------------------------------------------------------------->Global variable
#path to files
path_to_file=os.path.dirname(__file__).replace("classes","files")
#path to images
path_to_images=os.path.dirname(__file__).replace("classes","images")
#path to compareImages
path_to_compare_images=os.path.join(path_to_images,"CompareImages")
#path to faces images folder
path_to_faces_images=os.path.join(path_to_compare_images,"faces_images")
#path to faces videos folder
path_to_faces_videos=os.path.join(path_to_compare_images,"faces_videos")
#path to faces videos folder
path_to_faces_webcam=os.path.join(path_to_compare_images,"faces_webcam")
#path to yoloFace
path_yolo_face=[os.path.join(path_to_file,"yolov3-wider_16000.weights"),
                os.path.join(path_to_file,"yolov3-face.cfg")]
#path to yoloObjects
path_yolo_objects=[os.path.join(path_to_file,"yolov3.weights"),
                   os.path.join(path_to_file,"yolov3.cfg")]
#path to kera(AI)
path_to_kera=os.path.join(path_to_file,"FER_model.keras")

#------------------------------------------------------------------------------------------->function
#to get Logo
def get_logo():
    try:
        with open(os.path.join(path_to_file,"logo.L"),"rb") as file:
            logo=pick.load(file)
        return [True,logo]    
    except Exception as e:
        return  [False,f"Error during getting : {e}"] 
#to get the necessary packages
def get_packages():
    try:
        with open(os.path.join(path_to_file,"packages.L"),"rb") as file:
            packages=pick.load(file)
        return [True,packages]    
    except Exception as e:
        return  [False,f"Error during getting : {e}"]   
    
#to get we need to check
def get_version_adapted():
    try:
         with open(os.path.join(path_to_file,"versions.L"),"rb") as file:
            versions=pick.load(file)
         return [True,versions]    
    except Exception as e:    
        return  [False,f"Error during getting: {e}"]

#to get files we need in the program
def get_Files():
     try:
         with open(os.path.join(path_to_file,"Files.L"),"rb") as file:
            files=pick.load(file)
         return [True,files]    
     except Exception as e:    
        return  [False,f"Error during getting : {e}"]

#to set Objets 
def get_Objets():
    #to modifie global value
    global objets_class
    try:
        with open(os.path.join(path_to_file,"Objets.L"),"rb") as file:
             objets=pick.load(file) 
        return [True,objets]            
    except Exception as e:    
             return [False,f"Error during setting: {e}"]         

#set expressions
def get_Expressions():
    #to modifie global value
    global expressions
    try:
        with open(os.path.join(path_to_file,"expressions.L"),"rb") as file:
             exps=pick.load(file) 
        return [True,exps]                 
    except Exception as e:    
        return [False,f"Error during setting: {e}"] 

#to get index for a specific expression
def getIndexFor(name,TypeC):
    index_dict={name: i for i, name in enumerate(TypeC[1])}
    if name in index_dict:
        return index_dict[name]#if we find
    else:
        return -1 #if we not find the index    

#to get formats for images 
def get_images_formats():
    try:
        with open(os.path.join(path_to_file,"formats.L"),"rb") as file:
             formats_images=pick.load(file) 
        return [True,(formats_images[0]["type"],formats_images[0]["formats"]),formats_images[0]["extensions"]]                 
    except Exception as e:    
        return [False,f"Error : {e}"] 
    
#to get videos formats    
def get_videos_formats():
    try:
        with open(os.path.join(path_to_file,"formats.L"),"rb") as file:
             formats_videos=pick.load(file) 
        return [True,(formats_videos[1]["type"],formats_videos[1]["formats"]),formats_videos[1]["extensions"]]                 
    except Exception as e:    
        return [False,f"Error : {e}"] 

#to get bounds 
def get_bounds():
   #for windows frames
   root = Tk()
   width= root.winfo_screenwidth() #width for the screen
   height= root.winfo_screenheight() #height for the screen 
   root.destroy() #we close the window
   return [
           width,#with of screen
           [750,550,((width // 2) - (750// 2)),((height // 2) - (550 // 2))],#center
          ] 

#to get path to the logo images
def get_path_to_logo(index):
    return os.path.join(path_to_images,os.path.join("ProjetImages","{}.png".format(index)))

#to get path for faces's images
def get_path_to_faces_image():
    root = Tk()
    root.withdraw()  # to hide the root frame

    images_formats=get_images_formats()
    if images_formats[0]:#if not problem
       file = filedialog.askopenfilename(title="Choose an image for face",
                                      filetypes=[images_formats[1]])
       return [file,os.path.basename(file)]
    else:
       messagebox.showerror(title="Error",message=images_formats[1])    
       return ["",""]

#to get path to a specific video
def get_path_videos():
    root = Tk()
    root.withdraw()  # to hide the root frame
    videos_formats=get_videos_formats()
    if videos_formats[0]:#if not problem
       file = filedialog.askopenfilename(title="Choose a video ",
                                         filetypes=[videos_formats[1]])
       return [file,os.path.basename(file)]
    else:
       messagebox.showerror(title="Error",message=videos_formats[1])    
       return ["",""]

#to get path to folder(dbs)
def get_path_to_folder():
    root= Tk()
    root.withdraw()
    folder_path= filedialog.askdirectory(title="Choose folder")
    return [folder_path,os.path.basename(folder_path)]

#to get all images from a folder
def get_images_from_folder(path_folder):
    images = []
    formats=get_images_formats()[2]
    for ext in formats:
        images.extend(glob.glob(f"{path_folder}/*.{ext}"))
    
    return [image.replace("\\", "/") for image in images]

#to get path where to save file for objets/micro
def get_path_file():
    root = Tk()
    root.withdraw()  
    file_path = filedialog.asksaveasfilename(
                           defaultextension=".txt",   
                           filetypes=[("Text Files", "*.txt")],
                           title="Save your file"
                )
    return file_path
#to get a string from a liste
def get_String(arrayL):
    st=""
    for n in arrayL:
        st=st+n+"\n"
    return st    

#to create a copy 
def get_copy(source,name,path):
    if not os.path.exists(path):
        set_folder(path)    
    shutil.copyfile(source,os.path.join(path,name))
    return os.path.join(path,name)

#to delete a folder container
def set_folder_to_empty(path_folder):
    for file in os.listdir(path_folder):
        path_obj=os.path.join(path_folder,file)
        if os.path.isfile(path_obj):os.remove(path_obj)
        elif os.path.isdir(path_obj):shutil.rmtree(path_obj)


#to create a folder
def set_folder(path):
    os.mkdir(path)


#to save file
def set_file(path_file,typeF):
   try :
        with open(path_file, "w") as f:
             f.write(typeF)
        return [True,path_file]
   except Exception as e:
        return [False,f"Error : {e}"]                


#backgrount button's text color 
def get_hex_white_color():
    return "#faf8f7" 

#button and text frame color 
def get_hex_green_color():
    return "#084d18"

#red hex
def get_red_hex():
    return (0,0,255)
#blue hex
def get_bleu_hex():
    return (255,0,0)

#green color in bgr
def get_green_bgr_color():
    return (24, 77, 8)

#font for frame's text 
def get_button_font():
    return ("Arial", 12, "bold")

#loading font
def get_loading_font():
    return ("Comic Sans MS", 12)

#font for title inside frame
def get_title_font():
    return ("Arial", 19,"bold")

#font for entry
def get_entry_font():
    return  ("Arial",25)
#to get title for the app 
def get_title():
    return "L-detector"


#unicode for face
def get_face_unicode():
    return "\U0001F464"

#unicode for objects
def get_objects_unicode():
    return "\U0001F4E6"

#unicode for micro-expression
def get_micro_unicode():
    return "\U0001F3AD"

#unicode for image
def get_images_unicode():
    return "\U0001F5BC"

#unicode for video
def get_videos_unicode():
    return "\U0001F3A5"

#unicode for webcam
def get_webcam_unicode():
    return "\U0001F3A6"

#unicode for back
def get_back_unicode():
    return "\u2190"

#unicode check mark 
def get_check_unicode():
    return "\U00002705"

#unicode check mark 
def get_cross_mark_unicode():
    return "\U0000274C"

#unicode check mark 
def get_smile_unicode():
    return "\U0001F60A"

#unicode for waiting
def get_wait_unicode():
    return "\U0001F501"

#to get folder unicode
def get_folder_unicode():
    return "\U0001F5C2"

#start unicode
def get_start_unicode():
    return "\U0001F3C1"

#congrat unicode
def get_congrat_unicode():
    return "\U0001F389"

