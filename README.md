# Object Detection using YOLOv5 AI.

yolov5.rar must be unarchived and placed inside a folder called "Image_Detection".

The folder "Image_Detection" must be placed inside the "summarizer" folder.

"yolov5s.pt" must be placed inside the "yolov5" folder.

"run.bat" will be placed inside the Image_Detection folder alongside the movie seq. named "video.mp4" (name can be changed inside the batch file)

After running the program, the movie seq. will have all the detectable objects, of each frame, highlighted.

Inside the "Image_Detection" folder a file containing all the objects and their appearances will be created.

!Important: Some of the objects detected may be false detections, considering the framerate of a movie to be 24 fps, 

objects that appear under a threshold, let's say 24 times, are likely to be erroneous, as their nr. of appearances is too 

small to be considered even relevant.

https://github.com/ultralytics/yolov5

# 1st Update
The main program has been optimized :
 - no more hard-coded paths
 - the numbering function had some issues detecting objects composed of multiple words, an issue which has been solved
 - a configuration file can be now found in the folder containing the main program which can be used to change the threshold value and that can provide further uses down the line
 - started work on the DER computation, by first creating an automatic srt type file generator that should create subtitles with the help of the image detection done by YOLO


# 2nd Update

- implemented the sliding window, median filter
- implemented a conversion function to an .srt type file
- work still has to be done on implementing the dynamic subtitle length allocation (information regarding each word + occurrence + time stamps has been already prepared)

# 3rd Update

- a final .srt file is created, in which every object appearing in the frame is ordered on a per-second basis
- final results are to be improved by using scene change information

# 4th Update
- two .srt type files are now generated
  - a per second analysis of the detected objects is done and stored in the file "Subtitle_Second.srt"
  - the second file, "Subtitle_Scene.srt", contains objects present during one scene, whenever a scene change is detected another subtitle is generated
 - the sliding window filter is now more dynamic, it resets when a scene change is detected and restarted after the scene change; its results should resemble more accurate results
