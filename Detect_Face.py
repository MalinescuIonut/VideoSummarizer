import face_recognition
import cv2
import os

# Create a folder to save the detected faces if it doesn't exist
output_folder = "detected_faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the input movie file
input_movie = cv2.VideoCapture("cut.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Initialize some variables
face_locations = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    #Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    #Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)

    #Label the results
    for (top, right, bottom, left) in face_locations:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Save the detected face to a new file
        face_image = frame[top:bottom, left:right]
        name = os.path.join(output_folder, f"face_{frame_number}.jpg")
        cv2.imwrite(name, face_image)

    # Write the resulting image
    print("Writing frame {} / {}".format(frame_number, length))

input_movie.release()
cv2.destroyAllWindows()
