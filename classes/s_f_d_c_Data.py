#--------------------------------------------SEARCH-FIND-DISPLAY-COMPARE-DATA---------------------------------------------------#
#packages
import os
import threading
import numpy as np
import cv2 as device
from deepface import DeepFace
from PIL import Image, ImageTk
from tkinter import Tk, Toplevel, Label,PhotoImage,messagebox
#classes
import get_set_Data as app
#-------------------------------------------------------------------------->display images 
#display images
def display_images(images, is_matrix):
    root = Tk()
    root.withdraw()
    def show_image(image):
        #image
        win = Toplevel()
        img = Image.open(image["path"])
        img_tk = ImageTk.PhotoImage(img)
        #icon
        icon = PhotoImage(file=app.get_path_to_logo(0))
        #position
        if image["position"] == 0:
             bounds = [img_tk.width(), img_tk.height(), 0, 0]
        elif image["position"] == 1:   
             bounds = app.get_bounds()[1]
        else:
             bounds = [img_tk.width(), img_tk.height(), app.get_bounds()[0] - img_tk.width(), 0]
        #Label
        label = Label(win, image=img_tk)
        label.image = img_tk
        label.pack()
        #window
        win.iconphoto(True, icon)
        win.title(image["title"])
        win.geometry(f"{bounds[0]}x{bounds[1]}+{bounds[2]}+{bounds[3]}")
        win.config(background=app.get_hex_white_color())
    #if not matrix
    if not is_matrix:
        for image in images:
                show_image(image)
    else:           
        for index in images:
                for image in index:
                    show_image(image)
    root.mainloop()                
    

#--------------------------------------------------------------------------->compare faces
#compare 2 faces return true il there are equal
def compare_faces(img1,img2):
    #we check if two face are same
    check=DeepFace.verify(img1,
                          img2,
                          detector_backend="mtcnn",
                          enforce_detection=False
                          )
    #if same we stop 
    if check["verified"] and check["distance"] < 0.6:
        return True
    #if  no match 
    return False  
#to compare 2 folder
def compare_folder(path_folder1,path_folder2,main_folder):
    #results
    results=[]
    #get faces from folder 
    dbs_folder1=app.get_images_from_folder(os.path.join(path_folder1,"faces"))
    dbs_folder2=app.get_images_from_folder(os.path.join(path_folder2,"faces"))
    #we stocke the name of the image we are working on 
    name_image=os.path.basename(app.get_images_from_folder(os.path.join(path_folder2,"data"))[0])
    #check each image
    for img2 in dbs_folder2 :
        for img1 in dbs_folder1:
            #result
            result=compare_faces(img1,img2)
            #if same face
            if result:
               #copy
               real_path=app.get_copy(img1,os.path.basename(img1),os.path.join(app.path_to_compare_images,"copy"))
               #path in copy for img1(face)
               results.append({"path":real_path,"title":f"Face {os.path.basename(img1)}","position":0})
               #path in main_folder if we have one
               results.append({"path":os.path.join(main_folder,name_image),"title":f"Face {os.path.basename(img1)} found here {name_image}","position":2})
    return results
#to compare face in a folder
def compare_face_folder(main_face,faces):
    #results
    results=[]
    #check the image
    for face in faces:
        if compare_faces(main_face,face):#if we found a match
             results.append({"path":main_face,"title":f"Face {os.path.basename(face)} found here","position":2})
             results.append({"path":face,"title":f"Face {os.path.basename(face)}","position":0})
             return results
    return results #if no match     

#------------------------------------------------------------------------------------->Search face        
#to search faces in a images
def search_faces_for_image(path_to_Image,name_Image,path_folder):
    try:
        if os.path.exists(path_folder):
           #we clean the folder where we are going to work 
           app.set_folder_to_empty(path_folder)  
        else:
            app.set_folder(path_folder) 
        #folder for faces and images detect
        faces_folder=os.path.join(path_folder,"faces")
        data_folder=os.path.join(path_folder,"data")     
        #create folder we stocke faces and the name of image we are working in 
        app.set_folder(faces_folder)
        app.set_folder(data_folder)
        #path to image changed
        path_I=None
        #counter (to counter number of faces detect)
        counter=0
        #load AI
        net_seek=device.dnn.readNet(app.path_yolo_face[0],app.path_yolo_face[1])
        #load image
        image=device.imread(path_to_Image)
        height,width=image.shape[:2] #height and width for the image
        #getting the image ready for AI 
        blob_image=device.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        #send the image to the AI
        net_seek.setInput(blob_image)
        #get All layers names
        layers_names=net_seek.getLayerNames()
        #getting index for layers responding
        output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
        #getting results
        results=net_seek.forward(output_layers)
        #frame for faces detected(x,y,w,h)
        boxes=[]
        #confidences in %
        confidences=[]
        #getting coordinate for faces found
        for result in results:
            for detection in result :
                confidence=detection[4]
                if confidence > 0.6:
                    w=int(detection[2] * width)
                    h=int(detection[3] * height)
                    x=int(int(detection[0] * width) - (w/2))
                    y=int(int(detection[1] * height) - (h/2))
                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
        #deleting duplicates
        faces=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
        #if we found faces
        if len(faces) > 0:
            for coordinates in np.array(faces).flatten():
                #coordonates without duplicates 
                x,y,w,h=boxes[coordinates]
                #face coordinate
                face=image[y:y+h,x:x+w]
                #resize 
                face_resized = device.resize(face, (300, 300))
                #save face
                device.imwrite(os.path.join(faces_folder,f"{counter}.png"),face_resized)
                #drawing a rectangle above
                device.rectangle(image,(x,y),(x+w,y+h),app.get_green_bgr_color(),2)
                #increment counter
                counter+=1
            #path_I    
            path_I= os.path.join(data_folder,name_Image)
            #save image
            device.imwrite(path_I,image)    
            #response
            return [True,f"The program detected {counter} faces  {app.get_face_unicode()} for the image {name_Image}",path_I]
        else :#if no faces detected
            raise Exception(f"The program detected no faces for the image {name_Image}")   
    except Exception as e:
            return [False,e,path_I]
#to search objet in image
def search_object_in_image(indexObject,path_image,path_folder_save):
    try:
        #classes
        classes=app.get_Objets()[1]
        #load AI
        net_seek=device.dnn.readNet(app.path_yolo_objects[0],app.path_yolo_objects[1])
        #load image
        image=device.imread(path_image)
        height,width=image.shape[:2] #height and width for the image
        #getting the image ready for AI 
        blob_image=device.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        #send the image to the AI
        net_seek.setInput(blob_image)
        #get All layers names
        layers_names=net_seek.getLayerNames()
        #getting index for layers responding
        output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
        #getting results
        results=net_seek.forward(output_layers)
        #frame for faces detected(x,y,w,h)
        boxes=[]
        #confidences in %
        confidences=[]
        #id for the class
        class_ids = []
        #getting coordinate for faces found
        for result in results:
            for detection in result:
                scores = detection[5:]
                class_id = np.argmax(scores)#to get what type of class is it
                confidence = scores[class_id]
                if confidence > 0.5:
                    w=int(detection[2] * width)
                    h=int(detection[3] * height)
                    x=int(int(detection[0] * width) - (w/2))
                    y=int(int(detection[1] * height) - (h/2))
                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        #deleting duplicates
        indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
        #if we found faces
        if len(indexes) > 0:
            for index in np.array(indexes).flatten():
                if class_ids[index] == indexObject:
                      x, y, w, h = boxes[index]
                      device.rectangle(image, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                      path_I = os.path.join(path_folder_save, os.path.basename(path_image))
                      device.imwrite(path_I, image)
                      return [True, {"path": path_I, "title": f"Object {classes[indexObject]} found here {os.path.basename(path_image)}", "position": 2}]    
        return [False,None]           
    except Exception as e:
        messagebox.showerror(title="Error",message=f"{e} {app.get_cross_mark_unicode()}")
        return [False,None]    
    
#to search objet in image
def search_expression_in_image(indexExpression,path_image,path_folder_save):
    import keras
    try:
        #classes
        classes=app.get_Expressions()[1]
        #load AI
        net_seek=device.dnn.readNet(app.path_yolo_face[0],app.path_yolo_face[1])
        #AI for expressions
        model = keras.models.load_model(app.path_to_kera)  
        #load image
        image=device.imread(path_image)
        height,width=image.shape[:2] #height and width for the image
        #getting the image ready for AI 
        blob_image=device.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        #send the image to the AI
        net_seek.setInput(blob_image)
        #get All layers names
        layers_names=net_seek.getLayerNames()
        #getting index for layers responding
        output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
        #getting results
        results=net_seek.forward(output_layers)
        #frame for faces detected(x,y,w,h)
        boxes=[]
        #confidences in %
        confidences=[]
        #id for the class
        class_ids = []
        #getting coordinate for faces found
        for result in results:
            for detection in result:
                scores = detection[5:]
                class_id = np.argmax(scores)#to get what type of class is it
                confidence = scores[class_id]
                if confidence > 0.5:
                    w=int(detection[2] * width)
                    h=int(detection[3] * height)
                    x=int(int(detection[0] * width) - (w/2))
                    y=int(int(detection[1] * height) - (h/2))
                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        #deleting duplicates
        indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
        #if we found faces
        if len(indexes) > 0:
            for index in np.array(indexes).flatten():
                 x, y, w, h = boxes[index]
                 face = image[y:y + h, x:x + w]
                 #if face size == 0(face without pixels)
                 if face.size == 0 :
                     continue
                 #put the image in a format that AI understands
                 gray_face = device.cvtColor(face, device.COLOR_BGR2GRAY)
                 roi = device.resize(gray_face, (48, 48)).reshape(1, 48, 48, 1).astype('float32') / 255.0
                 #predict emotions
                 pred = model.predict(roi)[0]
                 if np.argmax(pred) == indexExpression:
                      device.rectangle(image, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                      path_I = os.path.join(path_folder_save, os.path.basename(path_image))
                      device.imwrite(path_I, image)
                      return [True, {"path": path_I, "title": f"Expression {classes[indexExpression]} found here {os.path.basename(path_image)}", "position": 2}]    
        return [False,None]           
    except Exception as e:
        messagebox.showerror(title="Error",message=f"{e} {app.get_cross_mark_unicode()}")
        return [False,None]    


#------------------------------------------------------------------------------------------->find faces,objets
#to find faces in dbs
def find_faces_in_dbs(dbs,main_folder,face_folder):
    #shared-result
    shared_results=[]
    for image in dbs:
        print(f"Checking .... {image} {app.get_wait_unicode()} ")
        resultFace=search_faces_for_image(image,os.path.basename(image),os.path.join(app.path_to_compare_images,"temp"))
        #if we find face we check with there are in the faces selected
        if resultFace[0]:#if we found face
           #compares faces 
           results=compare_folder(face_folder,os.path.join(app.path_to_compare_images,"temp"),main_folder) 
           #if we found faces stock
           if len(results) > 0:
              shared_results.append([result for result in results]) 
              print(f"We got a possible match for {os.path.basename(image)} {app.get_congrat_unicode()}")   
        print(f"Image {image} checked {app.get_check_unicode()}")
    
    print(f"The program is done with {len(shared_results)} results")    
    return shared_results
#to find faces in a video or a webcam
def find_faces_in_VW(faces_folder,work_folder,title,path_videos,resutR):
    try:
        if os.path.exists(work_folder):
           #we clean the folder where we are going to work 
           app.set_folder_to_empty(work_folder)  
        else:
           app.set_folder(work_folder)     
        #choice(if is a webcam or a videos )
        choice=None
        if len(path_videos) > 0:#working in videos 
           choice=path_videos
        else:
           choice=0
        #bounds
        bounds=app.get_bounds()[1]   
        # load AI for face
        net_seek=device.dnn.readNet(app.path_yolo_face[0],app.path_yolo_face[1])
        # load video or webcam
        cap = device.VideoCapture(choice)
        #check each frame
        while True:
             #to get the frame and if the video is still active
             ret, frame = cap.read()
             if not ret:
                break
             #to get the height an width of each frame
             height, width = frame.shape[:2]
             #getting the image ready for AI 
             blob_frame=device.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
             #send the image to the AI
             net_seek.setInput(blob_frame)
             #get All layers names
             layers_names=net_seek.getLayerNames()
             #getting index for layers responding
             output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
             #getting results
             results=net_seek.forward(output_layers)
             #frame for faces detected(x,y,w,h)
             boxes=[]
             #confidences in %
             confidences=[]
             #getting coordinate for faces found
             for result in results:
                 for detection in result :
                     confidence=detection[4]
                     if confidence > 0.6:
                        w=int(detection[2] * width)
                        h=int(detection[3] * height)
                        x=int(int(detection[0] * width) - (w/2))
                        y=int(int(detection[1] * height) - (h/2))
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
             #deleting duplicates
             faces=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
             #if we found faces
             if len(faces) > 0:
                for coordinates in np.array(faces).flatten():
                    #coordonates without duplicates 
                    x,y,w,h=boxes[coordinates]
                    #face coordinate
                    face=frame[y:y+h,x:x+w]
                    #resize face
                    face_resized = device.resize(face, (300, 300))
                    #path to image
                    path_I=os.path.join(work_folder,f"{0}.png")
                    #save face
                    device.imwrite(path_I,face_resized)
                    #drawing a rectangle above
                    device.rectangle(frame,(x,y),(x+w,y+h),app.get_red_hex(),2)
                    #we check face in folder
                    resultCFF=compare_face_folder(path_I,app.get_images_from_folder(os.path.join(faces_folder,"faces")))
                    if len(resultCFF) > 0:
                        #drawing a rectangle above
                        device.rectangle(frame,(x,y),(x+w,y+h),app.get_green_bgr_color(),2)
                        #dispaly result
                        threading.Thread(target=display_images,args=(resultCFF,False)).start()
             #show frame
             device.namedWindow(title,device.WINDOW_NORMAL)
             device.resizeWindow(title,bounds[0],bounds[1])
             device.moveWindow(title,bounds[2],bounds[3])
             device.imshow(title, frame)
             #to quit the frame 
             if device.waitKey(1) & 0xFF == ord("q"):
                resutR.set("The window is closed ")
                break      
        cap.release()
        device.destroyAllWindows()     
    except Exception as e:      
            messagebox.showerror(title="Error",message=f"Error : {e}")   
#to find object in dbs
def find_object_in_dbs(dbs,indexObject,main_path):
    #if the folder exists
    if os.path.exists(main_path):
        app.set_folder_to_empty(main_path)
    else :
        app.set_folder(main_path)   
    #results
    results=[]    
    #check each image
    for image in dbs:
        print(f"Checking .... {image} {app.get_wait_unicode()} ")
        result=search_object_in_image(indexObject,image,main_path)
        if  result[0] :#if the object was found
            results.append(result[1])
            print(f"We got a possible match for {os.path.basename(image)} {app.get_congrat_unicode()}")   
        print(f"Image {image} checked {app.get_check_unicode()}")
    return results  
#to detect object with index 
def find_objects_VWI(indexObject,path_video,title,result_str):
    try:
        #classes
        classes=app.get_Objets()[1]
        #to know if is webcam or a video
        choice=None #
        if len(path_video) > 0:
            choice=path_video    
        else:
            choice=0
         #bounds
        bounds=app.get_bounds()[1]   
        # load AI for face
        net_seek=device.dnn.readNet(app.path_yolo_objects[0],app.path_yolo_objects[1])
        # load video or webcam
        cap = device.VideoCapture(choice)
        #check each frame
        while True:
            #to get the frame and if the video is still active
             ret, frame = cap.read()
             if not ret:
                break
             #to get the height an width of each frame
             height, width = frame.shape[:2]
             #getting the image ready for AI 
             blob_frame=device.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
             #send the image to the AI
             net_seek.setInput(blob_frame)
             #get All layers names
             layers_names=net_seek.getLayerNames()
             #getting index for layers responding
             output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
             #getting results
             results=net_seek.forward(output_layers)
             #frame for faces detected(x,y,w,h)  
             boxes=[]
             #confidences in %
             confidences=[]
             #id for the class
             class_ids = []
             #getting coordinate for faces found
             for result in results:
                 for detection in result:
                     scores = detection[5:]
                     class_id = np.argmax(scores)#to get what type of class is it
                     confidence = scores[class_id]
                     if confidence > 0.5:
                        w=int(detection[2] * width)
                        h=int(detection[3] * height)
                        x=int(int(detection[0] * width) - (w/2))
                        y=int(int(detection[1] * height) - (h/2))
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
             #deleting duplicates
             indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
             #if we found faces
             if len(indexes) > 0:
                for index in np.array(indexes).flatten():
                      if class_ids[index] == indexObject:
                          x, y, w, h = boxes[index]
                          device.rectangle(frame, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                          device.putText(frame,  f"{classes[class_ids[index]]}: {confidences[index]:.2f}", (x, y - 10),
                                         device.FONT_HERSHEY_SIMPLEX, 1, app.get_green_bgr_color(), 5)
             #show frame
             device.namedWindow(title,device.WINDOW_NORMAL)
             device.resizeWindow(title,bounds[0],bounds[1])
             device.moveWindow(title,bounds[2],bounds[3])
             device.imshow(title, frame)
             #to quit the frame 
             if device.waitKey(1) & 0xFF == ord("q"):
                result_str.set("The window is closed ")
                break      
        cap.release()
        device.destroyAllWindows()  
    except Exception as e:
         messagebox.showerror(title="Error",message=f"Error : {e}")             
#to detect all objects
def find_objects_VWA(path_video,title,result_str):
    try:
        #classes
        classes=app.get_Objets()[1]
        #to know if is webcam or a video
        choice=None #
        if len(path_video) > 0:
            choice=path_video    
        else:
            choice=0
         #bounds
        bounds=app.get_bounds()[1]   
        # load AI for face
        net_seek=device.dnn.readNet(app.path_yolo_objects[0],app.path_yolo_objects[1])
        # load video or webcam
        cap = device.VideoCapture(choice)
        #check each frame
        while True:
            #to get the frame and if the video is still active
             ret, frame = cap.read()
             if not ret:
                break
             #to get the height an width of each frame
             height, width = frame.shape[:2]
             #getting the image ready for AI 
             blob_frame=device.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
             #send the image to the AI
             net_seek.setInput(blob_frame)
             #get All layers names
             layers_names=net_seek.getLayerNames()
             #getting index for layers responding
             output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
             #getting results
             results=net_seek.forward(output_layers)
             #frame for faces detected(x,y,w,h)  
             boxes=[]
             #confidences in %
             confidences=[]
             #id for the class
             class_ids = []
             #getting coordinate for faces found
             for result in results:
                 for detection in result:
                     scores = detection[5:]
                     class_id = np.argmax(scores)#to get what type of class is it
                     confidence = scores[class_id]
                     if confidence > 0.5:
                        w=int(detection[2] * width)
                        h=int(detection[3] * height)
                        x=int(int(detection[0] * width) - (w/2))
                        y=int(int(detection[1] * height) - (h/2))
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
             #deleting duplicates
             indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
             #if we found faces
             if len(indexes) > 0:
                for index in np.array(indexes).flatten():
                    x, y, w, h = boxes[index]
                    device.rectangle(frame, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                    device.putText(frame,  f"{classes[class_ids[index]]}: {confidences[index]:.2f}", (x, y - 10),
                                         device.FONT_HERSHEY_SIMPLEX, 1, app.get_green_bgr_color(), 5)
             #show frame
             device.namedWindow(title,device.WINDOW_NORMAL)
             device.resizeWindow(title,bounds[0],bounds[1])
             device.moveWindow(title,bounds[2],bounds[3])
             device.imshow(title, frame)
             #to quit the frame 
             if device.waitKey(1) & 0xFF == ord("q"):
                result_str.set("The window is closed ")
                break      
        cap.release()
        device.destroyAllWindows()  
    except Exception as e:
         messagebox.showerror(title="Error",message=f"Error : {e}")             
#to find micro in dbs
def find_micro_in_dbs(dbs,indexExpression,main_path):
    #if the folder exists
    if os.path.exists(main_path):
        app.set_folder_to_empty(main_path)
    else :
        app.set_folder(main_path)   
    #results
    results=[]    
    #check each image
    for image in dbs:
        print(f"Checking .... {image} {app.get_wait_unicode()} ")
        result=search_expression_in_image(indexExpression,image,main_path)
        if  result[0] :#if the object was found
            results.append(result[1])
            print(f"We got a possible match for {os.path.basename(image)} {app.get_congrat_unicode()}")   
        print(f"Image {image} checked {app.get_check_unicode()}")
    return results  
#to detect expression with index 
def find_expressions_VWI(indexExpression,path_video,title,result_str):
    import keras
    try:
        #classes
        classes=app.get_Expressions()[1]
        #to know if is webcam or a video
        choice=None #
        if len(path_video) > 0:
            choice=path_video    
        else:
            choice=0
         #bounds
        bounds=app.get_bounds()[1]   
        # load AI for face
        net_seek=device.dnn.readNet(app.path_yolo_face[0],app.path_yolo_face[1])
        #AI for expressions
        model = keras.models.load_model(app.path_to_kera) 
        # load video or webcam
        cap = device.VideoCapture(choice)
        #check each frame
        while True:
            #to get the frame and if the video is still active
             ret, frame = cap.read()
             if not ret:
                break
             #to get the height an width of each frame
             height, width = frame.shape[:2]
             #getting the image ready for AI 
             blob_frame=device.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
             #send the image to the AI
             net_seek.setInput(blob_frame)
             #get All layers names
             layers_names=net_seek.getLayerNames()
             #getting index for layers responding
             output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
             #getting results
             results=net_seek.forward(output_layers)
             #frame for faces detected(x,y,w,h)  
             boxes=[]
             #confidences in %
             confidences=[]
             #id for the class
             class_ids = []
             #getting coordinate for faces found
             for result in results:
                 for detection in result:
                     scores = detection[5:]
                     class_id = np.argmax(scores)#to get what type of class is it
                     confidence = scores[class_id]
                     if confidence > 0.5:
                        w=int(detection[2] * width)
                        h=int(detection[3] * height)
                        x=int(int(detection[0] * width) - (w/2))
                        y=int(int(detection[1] * height) - (h/2))
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
             #deleting duplicates
             indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
             #if we found faces
             if len(indexes) > 0:
                for index in np.array(indexes).flatten():
                    x, y, w, h = boxes[index]
                    face = frame[y:y + h, x:x + w]
                    #put the image in a format that AI understands
                    gray_face = device.cvtColor(face, device.COLOR_BGR2GRAY)
                    roi = device.resize(gray_face, (48, 48)).reshape(1, 48, 48, 1).astype('float32') / 255.0
                    #predict emotions
                    pred = model.predict(roi)[0]
                    if np.argmax(pred) == indexExpression:
                        device.rectangle(frame, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                        device.putText(frame,  f"{classes[indexExpression]}: {confidences[index]:.2f}", (x, y - 10),
                                         device.FONT_HERSHEY_SIMPLEX, 1, app.get_green_bgr_color(), 5)
             #show frame
             device.namedWindow(title,device.WINDOW_NORMAL)
             device.resizeWindow(title,bounds[0],bounds[1])
             device.moveWindow(title,bounds[2],bounds[3])
             device.imshow(title, frame)
             #to quit the frame 
             if device.waitKey(1) & 0xFF == ord("q"):
                result_str.set("The window is closed ")
                break      
        cap.release()
        device.destroyAllWindows()  
    except Exception as e:
         messagebox.showerror(title="Error",message=f"Error : {e}")
#to detect all expression  
def find_expressions_VWA(path_video,title,result_str):
    import keras
    try:
        #classes
        classes=app.get_Expressions()[1]
        #to know if is webcam or a video
        choice=None #
        if len(path_video) > 0:
            choice=path_video    
        else:
            choice=0
         #bounds
        bounds=app.get_bounds()[1]   
        # load AI for face
        net_seek=device.dnn.readNet(app.path_yolo_face[0],app.path_yolo_face[1])
        #AI for expressions
        model = keras.models.load_model(app.path_to_kera) 
        # load video or webcam
        cap = device.VideoCapture(choice)
        #check each frame
        while True:
            #to get the frame and if the video is still active
             ret, frame = cap.read()
             if not ret:
                break
             #to get the height an width of each frame
             height, width = frame.shape[:2]
             #getting the image ready for AI 
             blob_frame=device.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
             #send the image to the AI
             net_seek.setInput(blob_frame)
             #get All layers names
             layers_names=net_seek.getLayerNames()
             #getting index for layers responding
             output_layers=[layers_names[int(i)-1] for i in net_seek.getUnconnectedOutLayers()]
             #getting results
             results=net_seek.forward(output_layers)
             #frame for faces detected(x,y,w,h)  
             boxes=[]
             #confidences in %
             confidences=[]
             #id for the class
             class_ids = []
             #getting coordinate for faces found
             for result in results:
                 for detection in result:
                     scores = detection[5:]
                     class_id = np.argmax(scores)#to get what type of class is it
                     confidence = scores[class_id]
                     if confidence > 0.5:
                        w=int(detection[2] * width)
                        h=int(detection[3] * height)
                        x=int(int(detection[0] * width) - (w/2))
                        y=int(int(detection[1] * height) - (h/2))
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
             #deleting duplicates
             indexes=device.dnn.NMSBoxes(boxes,confidences,0.6,0.4)
             #if we found faces
             if len(indexes) > 0:
                for index in np.array(indexes).flatten():
                    x, y, w, h = boxes[index]
                    face = frame[y:y + h, x:x + w]
                    #put the image in a format that AI understands
                    gray_face = device.cvtColor(face, device.COLOR_BGR2GRAY)
                    roi = device.resize(gray_face, (48, 48)).reshape(1, 48, 48, 1).astype('float32') / 255.0
                    #predict emotions
                    pred = model.predict(roi)[0]
                    #draw and write
                    device.rectangle(frame, (x, y), (x + w, y + h), app.get_green_bgr_color(), 2)
                    device.putText(frame,  f"{classes[np.argmax(pred)]}: {confidences[index]:.2f}", (x, y - 10),
                                         device.FONT_HERSHEY_SIMPLEX, 1, app.get_green_bgr_color(), 5)
             #show frame
             device.namedWindow(title,device.WINDOW_NORMAL)
             device.resizeWindow(title,bounds[0],bounds[1])
             device.moveWindow(title,bounds[2],bounds[3])
             device.imshow(title, frame)
             #to quit the frame 
             if device.waitKey(1) & 0xFF == ord("q"):
                result_str.set("The window is closed ")
                break      
        cap.release()
        device.destroyAllWindows()  
    except Exception as e:
         messagebox.showerror(title="Error",message=f"Error : {e}")         