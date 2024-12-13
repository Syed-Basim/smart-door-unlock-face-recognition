import face_recognition
import cv2
import numpy as np
import sys


def detect_and_recognize_faces(frame, known_face_encodings, known_face_names):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)

    if not face_locations:
        print("No faces detected in the frame.")
        return [], []

    try:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    except Exception as e:
        print(f"Error in face_encodings: {e}")
        print(f"rgb_small_frame shape: {rgb_small_frame.shape}")
        print(f"rgb_small_frame dtype: {rgb_small_frame.dtype}")
        print(f"face_locations: {face_locations}")
        return [], []

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Convert back to original scale
    face_locations = [(top * 4, right * 4, bottom * 4, left * 4) for (top, right, bottom, left) in face_locations]

    return face_locations, face_names


def add_new_face(image):
    print("Entering add_new_face function")
    print(f"Image shape: {image.shape}")
    print(f"Image dtype: {image.dtype}")

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)
    print(f"Face locations: {face_locations}")

    if len(face_locations) != 1:
        raise ValueError("Image should contain exactly one face")

    try:
        face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        print("Face encoding generated successfully")
        return face_encoding
    except Exception as e:
        print(f"Error generating face encoding: {e}")
        raise\


print("face_recognition module imported successfully")
