import cv2
from face_recognition_implementation import add_new_face
from setup_database import add_face_to_db, check_database
import sys


def capture_and_add_face():
    name = input("Enter the name of the person: ")

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open camera")
        return

    print("\nInstructions:")
    print("- Position your face in the camera")
    print("- Press 'c' to capture")
    print("- Press 'q' to quit")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Add instruction text to frame
        cv2.putText(frame, "Press 'c' to capture, 'q' to quit",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            try:
                print("Capturing face...")
                face_encoding = add_new_face(frame)
                add_face_to_db(name, face_encoding)
                print(f"Success: Face of {name} added to database!")

                # Verify the face was added
                if check_database():
                    print("Database verification successful")
                else:
                    print("Warning: Face may not have been saved correctly")
                break
            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.")
            except Exception as e:
                print(f"Unexpected error: {e}")
                print("Please try again.")
        elif key == ord('q'):
            print("Quitting without adding a face.")
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_and_add_face()