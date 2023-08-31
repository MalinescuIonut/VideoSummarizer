# Import Libraries
import cv2
import numpy as np
import face_recognition
import os

import os
from typing import Union

import cv2

from hat_beard_classifier import HatBeardClassifier, SimpleFaceDetector, draw_results, get_coordinates
from config import (
    INPUT_SHAPE, CLASSIFIER_MODEL_PATH, CASCADE_FILE_PATH, SCALE_FACTOR, MIN_NEIGHBOURS, COORDINATES_EXTEND_VALUE
)

# The gender model architecture
# https://drive.google.com/open?id=1W_moLzMlGiELyPxWiYQJ9KFaXroQ_NFQ
GENDER_MODEL = 'weights/deploy_gender.prototxt'
# The gender model pre-trained weights
# https://drive.google.com/open?id=1AW3WduLk1haTVAxHOkVS_BEzel1WXQHP
GENDER_PROTO = 'weights/gender_net.caffemodel'
# Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
# substraction to eliminate the effect of illunination changes
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Represent the gender classes
GENDER_LIST = ['Male', 'Female']
# https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
FACE_PROTO = "weights/deploy.prototxt.txt"
# https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
FACE_MODEL = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"

# load face Caffe model
face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
# Load gender prediction model
gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)

# Initialize frame size
frame_width = 1280
frame_height = 720


def get_faces(frame, confidence_threshold=0.5):
    # convert the frame into a blob to be ready for NN input
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
    # set the image as input to the NN
    face_net.setInput(blob)
    # perform inference and get predictions
    output = np.squeeze(face_net.forward())
    # initialize the result list
    faces = []
    # Loop over the faces detected
    for i in range(output.shape[0]):
        confidence = output[i, 2]
        if confidence > confidence_threshold:
            box = output[i, 3:7] * \
                  np.array([frame.shape[1], frame.shape[0],
                            frame.shape[1], frame.shape[0]])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int)
            # widen the box a little
            start_x, start_y, end_x, end_y = start_x - \
                                             10, start_y - 10, end_x + 10, end_y + 10
            start_x = 0 if start_x < 0 else start_x
            start_y = 0 if start_y < 0 else start_y
            end_x = 0 if end_x < 0 else end_x
            end_y = 0 if end_y < 0 else end_y
            # append to our list
            faces.append((start_x, start_y, end_x, end_y))
    return faces


def display_img(title, img):
    """Displays an image on screen and maintains the output until the user presses a key"""
    # Display Image on screen
    cv2.imshow(title, img)
    # Mantain output until user presses a key
    cv2.waitKey(0)
    # Destroy windows when user presses a key
    cv2.destroyAllWindows()


def get_optimal_font_scale(text, width):
    """Determine the optimal font scale based on the hosting frame width"""
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale / 10
    return 1


# from: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    return cv2.resize(image, dim, interpolation=inter)


def process_images(images_path: str, use_detector: bool, confidence_threshold: float) -> int:
    """
    Process all images from folder and return the count of detected beards.

    :param images_path: path to folder with images.
    :param use_detector: if False, then don't use the face detector and classify the whole image.
    :param confidence_threshold: threshold for considering a prediction as valid.
    :return: The count of detected beards.
    """

    detector = SimpleFaceDetector(CASCADE_FILE_PATH, SCALE_FACTOR, MIN_NEIGHBOURS)
    classifier = HatBeardClassifier(CLASSIFIER_MODEL_PATH, INPUT_SHAPE)

    beard_count = 0  # Initialize the beard count

    images_paths = [os.path.join(images_path, p) for p in os.listdir(images_path)]
    for img_path in images_paths:
        image = cv2.imread(img_path)
        if image is None:
            print('Can\'t read image: "{}".'.format(img_path))
            continue
        if use_detector:
            faces = detector.inference(image)
            for face_coordinates in faces:
                x, y, w, h = get_coordinates(image, face_coordinates, COORDINATES_EXTEND_VALUE)
                class_result = classifier.inference(image[y:y + h, x:x + w, :])
                if class_result == 1 and classifier.get_confidence() > confidence_threshold:
                    print("1")
                    beard_count += 1  # Increment the beard count
        else:
            class_result = classifier.inference(image)
            if class_result == 1 and classifier.get_confidence() > confidence_threshold:
                print("1")
                beard_count += 1  # Increment the beard count

    return beard_count  # Return the total count of detected beards




def get_image_paths(input_folder):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_paths = [os.path.join(input_folder, f) for f in image_files]
    return image_paths


def find_matching_strings(input_list):
    import re
    male_pattern = r"Male-(\d+\.\d+)%"
    female_pattern = r"Female-(\d+\.\d+)%"

    male_matches = []
    female_matches = []

    for item in input_list:
        male_match = re.match(male_pattern, item)
        female_match = re.match(female_pattern, item)

        if male_match:
            male_percentage = float(male_match.group(1))
            male_matches.append(male_percentage)
        if female_match:
            female_percentage = float(female_match.group(1))
            female_matches.append(female_percentage)

    return male_matches, female_matches


def get_clusters(base_folder):
    import re
    folder_names = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    cluster_folders = [f for f in folder_names if re.match(r'cluster_\d+', f)]
    return cluster_folders


def predict_gender(input_path: str):
    current_script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(current_script_path)

    face_clusters = get_clusters(script_directory)

    with open(str(script_directory) + '\Cluster_Info.txt', 'w') as file:

        for nr, cluster in enumerate(face_clusters):

            input_folder = str(script_directory) + "\\" + str(cluster)
            print(input_folder)
            image_file_paths = get_image_paths(input_folder)

            gender_confidence_list = []

            beard_counter = 0

            for l, file_path in enumerate(image_file_paths):
                """Predict the gender of the faces showing in the image"""
                # Read Input Image
                img = cv2.imread(file_path)

                if img is None:
                    continue

                # resize the image, uncomment if you want to resize the image
                # img = cv2.resize(img, (frame_width, frame_height))
                # Take a copy of the initial image and resize it
                frame = img.copy()
                if frame.shape[1] > frame_width:
                    frame = image_resize(frame, width=frame_width)
                # predict the faces
                faces = get_faces(frame)
                # Loop over the faces detected
                # for idx, face in enumerate(faces):
                for i, (start_x, start_y, end_x, end_y) in enumerate(faces):
                    face_img = frame[start_y: end_y, start_x: end_x]
                    # image --> Input image to preprocess before passing it through our dnn for classification.
                    # scale factor = After performing mean substraction we can optionally scale the image by some factor. (if 1 -> no scaling)
                    # size = The spatial size that the CNN expects. Options are = (224*224, 227*227 or 299*299)
                    # mean = mean substraction values to be substracted from every channel of the image.
                    # swapRB=OpenCV assumes images in BGR whereas the mean is supplied in RGB. To resolve this we set swapRB to True.
                    blob = cv2.dnn.blobFromImage(image=face_img, scalefactor=1.0, size=(
                        227, 227), mean=MODEL_MEAN_VALUES, swapRB=False, crop=False)
                    # Predict Gender
                    gender_net.setInput(blob)
                    gender_preds = gender_net.forward()
                    i = gender_preds[0].argmax()
                    gender = GENDER_LIST[i]
                    gender_confidence_score = gender_preds[0][i]
                    # Draw the box
                    label = "{}-{:.2f}%".format(gender, gender_confidence_score * 100)
                    print(label)

                    gender_confidence_list.append(label)

                    yPos = start_y - 15
                    while yPos < 15:
                        yPos += 15
                    # get the font scale for this image size
                    optimal_font_scale = get_optimal_font_scale(label, ((end_x - start_x) + 25))
                    box_color = (255, 0, 0) if gender == "Male" else (147, 20, 255)
                    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)
                    # Label processed image
                    cv2.putText(frame, label, (start_x, yPos),
                                cv2.FONT_HERSHEY_SIMPLEX, optimal_font_scale, box_color, 2)

                    # Display processed image
                # display_img("Gender Estimator", frame)
                # uncomment if you want to save the image
                # cv2.imwrite("output.jpg", frame)
                # Cleanup
                cv2.destroyAllWindows()

                male_matches, female_matches = find_matching_strings(gender_confidence_list)
                total_male_percentage = sum(male_matches)
                total_female_percentage = sum(female_matches)

                # Set your hardcoded paths here

                parent_path = os.path.dirname(file_path)

                images_path = parent_path

                confidence_threshold = 0.5  # Adjust the confidence threshold as needed

                x = process_images(images_path, use_detector=True, confidence_threshold=confidence_threshold)
                beard_counter = beard_counter + x

            total_width = 0
            total_height = 0
            total_size = 0
            counter = 0

            for img_path in image_file_paths:
                print(img_path)
                img = cv2.imread(img_path)
                height, width, _ = img.shape
                size_kb = os.path.getsize(img_path) / 1024  # Convert to KB
                total_size += size_kb
                total_width += width
                total_height += height
                counter += 1

            num_images = counter
            avg_width = total_width / num_images
            avg_height = total_height / num_images
            avg_size_kb = total_size / num_images

            file.write(str(cluster))

            if total_male_percentage == 0 and total_female_percentage == 0:
                file.write(" Gender couldn't be predicted!\n")
            else:
                if total_male_percentage > total_female_percentage:
                    if len(male_matches) > 0:
                        file.write(": Male " + str(round(total_male_percentage / len(male_matches), 2)) + "%")
                    file.write(
                        " with " + str(len(male_matches)) + " matches out of: " + str(
                            len(gender_confidence_list)) + " pictures.")

                else:
                    if len(female_matches) > 0:
                        file.write(": Female " + str(round(total_female_percentage / len(female_matches), 2)) + "%")
                    file.write(" with " + str(len(female_matches)) + " matches out of: " + str(
                        len(gender_confidence_list)) + " pictures.")

                file.write("Dimension: " + str(round(avg_width, 2)) + "x" + str(round(avg_height, 2)) + " Size: " + str(
                    round(avg_size_kb, 2)))

            print(beard_counter)
            file.write(" Beard detected in: " + str(beard_counter) + " photos from " + str(
                len(gender_confidence_list)) + "\n")

            # print(str(gender_confidence_list) +'\n')
            # print(str(total_male_percentage) +"\n")
            # print(str(total_female_percentage) + "\n")


if __name__ == '__main__':
    current_script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(current_script_path)

    predict_gender(script_directory)
