**I. Download the Git Repo**

cd ~desired path~ (I created a new folder called Objecttracking inside the Summarization Folder)

git clone https://github.com/theAIGuysCode/yolov4-deepsort.git

**II. Download the Yolov4 weights and place them inside the "data" folder of the downloaded git repo**
-Yolov4 weights:
https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

conda env create -f conda-gpu.yml

conda activate yolov4-gpu

**!!Cuda is required in order to run the script, as the GPU is used instead of the CPU, otherwise:**

pip install scipy

pip install easydict

**Convert darknet weights to tensorflow model**
python save_model.py --model yolov4

**Replace the object_tracker.py with the one that I provide in this branch**

**Place the batch file in the folder containing the Python script mentioned above**

**Run the batch file**

**Mention!!**:  _allowed_classes = ['person'] => only persons are tracked, param can be changed_

A file containing the tracking info will be generated in the same folder as the script
