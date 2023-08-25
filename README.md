# Gender Predicition

list of necessary files to include in our project directory:

gender_net.caffemodel: https://drive.google.com/open?id=1W_moLzMlGiELyPxWiYQJ9KFaXroQ_NFQ
deploy_gender.prototxt: https://drive.google.com/open?id=1AW3WduLk1haTVAxHOkVS_BEzel1WXQHP
res10_300x300_ssd_iter_140000_fp16.caffemodel: https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
deploy.prototxt.txt: https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt

All these files must be added to a "weights" folder inside the folder containing the script.
I also placed the script inside the folder containing all the clusters.

An output file will be created in the same directory containing the gender info about each cluster.
