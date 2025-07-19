# L-Detector
This program allows you to find specific faces, objects, micro-expressions using images, videos, webcam

# How does it work ? 
In this program you will have to choose what you want to do, i.e. you will have 3 possible choices per area. For faces, objects, and microexpressions, we'll each have images (image folders), videos, and webcams. It's up to the user to choose what they want to do.
For:
1) Faces ---> Images (here we want to have images containing the faces we want; it's like facial recognition in a database; it's like providing an image with one or more faces, and the program displays the images in the folder containing that face.)
2) Faces ---> Videos (here it's the same as Faces/Images, but here the user provides a video from which we want to detect the images.)
3) Faces ---> Webcam (this is also the same as Faces/Images, but here we use the camera.)
4) Objects ---> Images (here we search for objects in images; the program provides a list of objects it can detect, and in an image folder we search for images with the objects we want to find.)
5) Objects ---> Videos (It's like objects/images but with a user-supplied video, with "all" meaning we want to detect all objects.)
6) Objects ---> webcam (It's like objects/images but using the computer's camera.)
7) Micro-expressions ---> images (Here we search for images with a given expression; the expressions are provided by the program.)
8) Micro-expressions ---> videos (Here we search for expressions (all) or an expression on a video.)
9) Micro-expressions ---> webcam (Here it's like Micro-expressions/videos but on the integrated camera.)

# What we need to run the app 
1) The user must ensure that their Python version is between (or equal to) 3.8 and 3.12
2) The user must run this command on a terminal:
a) pip install opencv-python
b) pip install numpy
c) pip install tensorflow
d) pip install deepface
e) pip install keras
f) pip install pillow
g) pip install mtcnn
h) pip install retina-face
3) The user must ensure that their Tensorflow version is between (or equal to) 2.11 and 2.17
4) The user must run the main.py file from the classes folder



