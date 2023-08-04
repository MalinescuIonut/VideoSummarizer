import cv2
import face_recognition
# from deepface import DeepFace
import os

current_script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(current_script_path)
input_directory = os.path.join(script_directory, 'Face_Images') # pcitures extracted using ffmpeg
output_directory = os.path.join(script_directory, 'Only_Faces')

if not os.path.exists(output_directory):
    os.makedirs(output_directory)



try:
    face_locations = []
    face_names = []
    frame_number = 0
    for image in os.listdir(input_directory):
        # Open the input movie file
        print("image: ", input_directory, image)
        frame = cv2.imread(os.path.join(input_directory, image))
        frame_number += 1
        print("#: " + str(frame_number))
        #            cv2.imshow('video', frame)
        #            input("pulse")
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_frame = frame[:, :, ::-1]
        rgb_frame = frame

        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        # print(face_locations)

        # Labeling results
        face_location = 0
        for (top, right, bottom, left) in face_locations:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Save detected face to a new file
            face_image = frame[top:bottom, left:right]
            face_location += 1
            output_directory = os.path.join(script_directory, 'Only_Faces')
            name = os.path.join(str(output_directory), f"face{frame_number}_{face_location}.png")
            # print(str(output_directory) + rf"\face{frame_number}_{face_location}.png")
            cv2.imwrite(name, face_image)

            if cv2.imwrite(output_directory, face_image):
                print(f"Extracted face saved successfully: {output_directory}")
            else:
                print(f"Failed to save the extracted face: {output_directory}")
        else:
            print(f"No valid face detected in {image}")
    else:
        print(f"No face detected in {image}")
except Exception as e:
    print(f"Error processing {image}: {e}")

