# Object Detection using YOLOv5 AI.

yolov5.rar must be unarchived and placed inside a folder called "Image_Detection".

The folder "Image_Detection" must be placed inside the "summarizer" folder.

"yolov5s.pt" must be placed inside the "yolov5" folder.

"run.bat" will be placed inside the Image_Detection folder alongside the movie seq. named "video.mp4" (name can be changed inside the batch file)

After running the program, the movie seq. will have all the detectable objects, of each frame, highlighted.

Inside the "Image_Detection" folder a file containing all the objects and their appearances will be created.

!Important: Some of the objects detected may be false detections, considering the framerate of a movie to be 24 fps, 

objects that appear under a threshold, let's say 24 times, are likely to be erroneous, as their nr. of appearances is too 
small to be considerd relevant.

https://github.com/ultralytics/yolov5
