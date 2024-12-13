import cv2
import time
from face_recognition_implementation import detect_and_recognize_faces
from setup_database import get_known_faces_from_db
from lock_control import setup_lock, open_lock, cleanup_lock


def main():
    # Initialize the lock
    setup_lock()

    # Get known faces from database
    known_names, known_encodings = get_known_faces_from_db()

    # Check if database has any faces
    if not known_names or not known_encodings:
        print("Error: No faces found in database. Please add faces using capture_and_add_face.py first.")
        return

    print(f"Loaded {len(known_names)} faces from database.")

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open video capture device")
        return

    # Variables for cooldown mechanism
    last_unlock_time = 0
    cooldown_period = 10  # seconds
    currently_unlocked = False

    print("Starting face recognition system. Press 'q' to quit.")

    try:
        while True:
            # Read frame
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame")
                continue

            # Create a copy for display
            display_frame = frame.copy()

            # Only attempt face recognition if we have known faces
            if known_encodings:
                try:
                    face_locations, face_names = detect_and_recognize_faces(frame, known_encodings, known_names)
                except Exception as e:
                    print(f"Error in face detection: {e}")
                    face_locations, face_names = [], []
            else:
                face_locations, face_names = [], []

            current_time = time.time()
            recognized_names = set()

            # Process detected faces
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw rectangle around the face
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)  # Green for known, Red for unknown
                cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)

                # Draw a filled rectangle for the name background
                cv2.rectangle(display_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

                # Add name text
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(display_frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

                if name != "Unknown":
                    recognized_names.add(name)

            # Handle lock control with cooldown
            if recognized_names and not currently_unlocked and (current_time - last_unlock_time) > cooldown_period:
                names_list = ", ".join(recognized_names)
                print(f"Access granted to: {names_list}")
                open_lock()
                last_unlock_time = current_time
                currently_unlocked = True
            elif current_time - last_unlock_time > 5:  # Lock has been open for 5 seconds
                currently_unlocked = False

            # Add system status display
            status_text = "UNLOCKED" if currently_unlocked else "LOCKED"
            color = (0, 255, 0) if currently_unlocked else (0, 0, 255)
            cv2.putText(display_frame, f"Status: {status_text}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Show the number of known faces
            cv2.putText(display_frame, f"Known faces: {len(known_names)}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Display the frame
            cv2.imshow('Face Recognition Access Control', display_frame)

            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Shutting down system...")
                break

    except KeyboardInterrupt:
        print("\nShutting down system...")

    finally:
        video_capture.release()
        cv2.destroyAllWindows()
        cleanup_lock()


if __name__ == "__main__":
    main()