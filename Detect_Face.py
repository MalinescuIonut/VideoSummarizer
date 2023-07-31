import face_recognition
from sklearn.cluster import KMeans
import os
import cv2
import dlib

def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return faces, image


def batch_detect_faces(folder_path, output_folder):
    def detect_faces(image_path):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = detector(gray_image)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return image, faces

    def save_detected_faces(image_path, output_folder):
        image, faces = detect_faces(image_path)
        if image is None:
            return

        image_name = os.path.splitext(os.path.basename(image_path))[0]

        # Create the output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the original image with rectangles around the detected faces
        # output_image_path = os.path.join(output_folder, image_name + "_detected.png")
        # cv2.imwrite(output_image_path, image)

        # Save each detected face as a separate image
        for i, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            face_image = image[y:y + h, x:x + w]
            face_output_path = os.path.join(output_folder, f"{image_name}.png")
            print(face_output_path)
            cv2.imwrite(face_output_path, face_image)

    png_files = [file for file in os.listdir(folder_path) if file.endswith(".png")]

    for png_file in png_files:
        image_path = os.path.join(folder_path, png_file)
        save_detected_faces(image_path, output_folder)
    return

def get_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings

def get_image_paths(folder_path):
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg', '.png'))]
    return image_paths

def cluster_faces(image_folder, output_folder):
    image_paths = get_image_paths(image_folder)
    face_encodings = []
    image_names = []

    for image_path in image_paths:
        encodings = get_face_encodings(image_path)
        if len(encodings) > 0:
            face_encodings.append(encodings[0])  # We only take on face if multiple are detected (for now)
            image_names.append(os.path.basename(image_path))

    if len(face_encodings) == 0:
        print("No faces found in the images.")
        return

    kmeans = KMeans(n_clusters=len(face_encodings), random_state=0)
    kmeans.fit(face_encodings)

    # Create separate folders for each person
    for i, cluster_label in enumerate(kmeans.labels_):
        person_folder = os.path.join(output_folder, f"Person_{cluster_label}")
        os.makedirs(person_folder, exist_ok=True)
        person_image_path = os.path.join(image_folder, image_names[i])
        os.rename(person_image_path, os.path.join(person_folder, image_names[i]))

    print("Clustering completed successfully.")
    return


def ffmpegFaceExtractor():
    import subprocess

    script_directory = os.path.dirname(os.path.abspath(__file__))
    frames_folder = os.path.join(script_directory, "frames")
    face_images_folder = os.path.join(script_directory, "Face_Images")

    # Create the frames folder if it doesn't exist
    os.makedirs(frames_folder, exist_ok=True)

    # FFmpeg command to extract frames from the video
    ffmpeg_command = f'ffmpeg -i cut1.mp4 -r 1/1 "{frames_folder}/frame%05d.png"'
    subprocess.run(ffmpeg_command, shell=True)

    # Create the face images folder if it doesn't exist
    os.makedirs(face_images_folder, exist_ok=True)

    # Move the extracted frames to the face images folder
    frame_files = os.listdir(frames_folder)
    for frame_file in frame_files:
        if frame_file.endswith(".png"):
            frame_path = os.path.join(frames_folder, frame_file)
            face_image_path = os.path.join(face_images_folder, frame_file)
            os.rename(frame_path, face_image_path)
    return


if __name__ == "__main__":
    ffmpegFaceExtractor()

    current_script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(current_script_path)
    folder_path = str(script_directory) + r'\Face_Images'
    output_folder = str(script_directory) + r'\Detected_Face_Images'

    batch_detect_faces(folder_path, output_folder)

    cluster_folder = str(script_directory) + r'\Clustered_Detected_Face_Images'
    cluster_faces(output_folder, cluster_folder)
