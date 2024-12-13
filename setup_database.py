import sqlite3
import numpy as np

def check_database():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM known_faces")
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def get_known_faces_from_db():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    c.execute("SELECT name, face_encoding FROM known_faces")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("Database is empty. No faces found.")
        return [], []

    known_names = []
    known_encodings = []
    for row in rows:
        try:
            known_names.append(row[0])
            known_encodings.append(np.frombuffer(row[1], dtype=np.float64))
        except Exception as e:
            print(f"Error processing face encoding for {row[0]}: {e}")
            continue

    print(f"Successfully loaded {len(known_names)} faces from database")
    return known_names, known_encodings

def setup_database():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS known_faces
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  face_encoding BLOB NOT NULL)''')
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()

def add_face_to_db(name, face_encoding):
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    face_encoding_bytes = face_encoding.tobytes()
    c.execute("INSERT INTO known_faces (name, face_encoding) VALUES (?, ?)",
              (name, face_encoding_bytes))
    conn.commit()
    conn.close()
    print(f"Face encoding for {name} added to database.")


def delete_face_from_db():
    # Connect to the database
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()

    # Get all names from the database
    c.execute("SELECT name FROM known_faces")
    names = c.fetchall()

    # Print all names
    print("Current faces in the database:")
    for idx, name in enumerate(names):
        print(f"{idx + 1}. {name[0]}")

    # Ask user which face to delete
    while True:
        try:
            choice = int(input("Enter the number of the face you want to delete (0 to cancel): "))
            if choice == 0:
                print("Operation cancelled.")
                conn.close()
                return
            if 1 <= choice <= len(names):
                name_to_delete = names[choice - 1][0]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Delete the chosen face
    c.execute("DELETE FROM known_faces WHERE name = ?", (name_to_delete,))
    conn.commit()

    print(f"Face '{name_to_delete}' has been deleted from the database.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    delete_face_from_db()