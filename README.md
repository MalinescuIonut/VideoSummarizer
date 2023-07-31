# Update 1
- new FFMPEG frame extractor implemented, which extracts one frame per second
- face_recognition still caused some problems for me, so I tried using dlib which extracts the faces with a good enough accuracy and also crops and saves them inside a folder "Detected_Face_Images"
- I also reimplemented a clustering function that creates a big folder in which all the small folders, belonging to every detected character, are stored
- I still encounter some errors with cv2 whenever cropping the images this being the error: cv2.error: OpenCV(4.5.2) C:\Users\runneradmin\AppData\Local\Temp\pip-req-build-m8us58q4\opencv\modules\imgcodecs\src\loadsave.cpp:721: error: (-215:Assertion failed) !_img.empty() in function 'cv::imwrite'
- I tried working it out, but I couldn't yet do it; for a sample of 10 min, it works perfectly until a random frame after which it stops and I don't yet know exactly why
- dlib also provides other functionalities like highlighting facial features(mouth, eyes, etc.) - a line of code has been written for that, but not yet used - these features however require a .dat file which I found here:
  https://github.com/italojs/facial-landmarks-recognition/tree/master



# Code Usage
The files listed here must be placed inside a folder named "Face_Detection" inside the "summarizer" folder.


# Libraries
python3 -m pip install opencv-python
python3 -m pip install face_recognition


# Resources

https://medium.com/analytics-vidhya/face-detection-on-recorded-videos-using-opencv-in-python-windows-and-macos-407635c699

https://github.com/ageitgey/face_recognition/blob/master/README.rst
