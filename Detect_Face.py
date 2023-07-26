import face_recognition
import cv2
import os
import numpy as np
from sklearn.cluster import DBSCAN
    # eps (epsilon): maximum distance between two points for them to be considered as neighbors.
    # min_samples: minimum number of points required to form a dense region (core point).
from sklearn.preprocessing import StandardScaler
import shutil


def process_video():
    try:
        # Create a folder to save the detected faces if it doesn't exist
        output_folder = "face_images"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the input movie file
        input_movie = cv2.VideoCapture("cut.mp4")
        length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create an output movie file (make sure resolution/frame rate matches input video!)
        frame_width = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = input_movie.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('output.avi', fourcc, frame_rate, (frame_width, frame_height))

        # Initialize some variables
        face_locations = []
        face_names = []
        frame_number = 0

        while True:
            # Grab a single frame of video
            ret, frame = input_movie.read()
            frame_number += 1

            # Quit when the input video file ends
            if not ret:
                break

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)

            # Labeling results
            for (top, right, bottom, left) in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Write the resulting image to the output video file
                print("Writing frame {} / {}".format(frame_number, length))
                output_movie.write(frame)

                # Save detected face to a new file
                face_image = frame[top:bottom, left:right]
                name = os.path.join(output_folder, f"{frame_number}.jpg")
                cv2.imwrite(name, face_image)

        input_movie.release()
        output_movie.release()
        cv2.destroyAllWindows()

    except Exception as e:
        # Capture the error message and return it
        return str(e)

def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces, image

def main():
    current_script_path = os.path.abspath(__file__)

    script_directory = os.path.dirname(current_script_path)

    input_directory = str(script_directory) + r'\face_images'
    image_files = [f for f in os.listdir(input_directory) if f.endswith('.jpg')]

    all_faces = []
    image_file_paths = []  #the original file paths
    for image_file in image_files:
        image_path = os.path.join(input_directory, image_file)
        faces, _ = detect_faces(image_path)
        all_faces.extend(faces)
        image_file_paths.extend([image_path] * len(faces))

    if len(all_faces) == 0:
        print("No faces were found in the provided images.")
        return

    X = np.array(all_faces)
    X = StandardScaler().fit_transform(X)

    eps = 0.5  # DBSCAN epsilon (distance threshold for clustering)
    min_samples = 5  # Minimum number of samples in a cluster
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)

    labels = db.labels_
    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # Count clusters (excluding noise points)

    # Create a new directory to store the clustered images
    output_directory = str(script_directory)
    os.makedirs(output_directory, exist_ok=True)

    # Move images to their respective cluster folders
    for cluster_id in range(num_clusters):
        cluster_indices = np.where(labels == cluster_id)[0]
        cluster_output_dir = os.path.join(output_directory, f"cluster_{cluster_id + 1}")
        os.makedirs(cluster_output_dir, exist_ok=True)

        for index in cluster_indices:
            image_path = image_file_paths[index]
            shutil.copy(image_path, cluster_output_dir)


if __name__ == "__main__":
    # error message (if any)
    error_message = process_video()

    if error_message:
        print("Error occurred:", error_message)
    else:
        main()