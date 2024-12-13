# Face Recognition Security System

A Python-based security system that uses facial recognition for access control. The system can detect faces in real-time, match them against a database of known faces, and control an electronic lock based on successful recognition.

## Features

- Real-time face detection and recognition
- SQLite database for storing face encodings
- User interface for adding and managing authorized faces
- Electronic lock control system (GPIO-based)
- Visual feedback system with status display
- Cooldown mechanism to prevent repeated triggers
- Support for multiple face recognition
- Color-coded visual feedback (green for known faces, red for unknown)

## Prerequisites

```bash
Python 3.8+
OpenCV
face_recognition
numpy
sqlite3
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/face-recognition-security.git
cd face-recognition-security
```

2. Install required packages
```bash
pip install opencv-python
pip install face_recognition
pip install numpy
```

## Project Structure

```
face-recognition-security/
├── setup_database.py          # Database initialization and management
├── face_recognition_implementation.py # Core face recognition functions
├── user_interface.py    # Interface for adding new faces
├── lock_control.py           # Electronic lock control system
├── main_program.py           # Main application script
└── README.md
```

## Usage

1. Initialize the database:
```bash
python setup_database.py
```

2. Add faces to the system:
```bash
python user_interface.py
```
- Enter the person's name
- Position face in the camera
- Press 'c' to capture
- Press 'q' to quit

3. Run the main program:
```bash
python main_program.py
```

### Controls
- Press 'q' to quit the program
- System automatically unlocks when recognizing authorized faces
- 10-second cooldown between unlock attempts
- Lock automatically re-engages after 5 seconds

## Database Management

To delete faces from the database:
```bash
python setup_database.py
```
Then select the delete option and follow the prompts.

## Hardware Setup

The system is designed to work with:
- Standard USB webcam
- Electronic lock mechanism connected to GPIO pin 18
- Optional LED indicators

## Security Features

- Face recognition with deep learning
- Cooldown mechanism to prevent rapid re-triggering
- Automatic lock re-engagement
- Unknown face detection and marking
- Visual and console logging of access attempts

## Troubleshooting

### Common Issues

1. "No faces found in database"
   - Run setup_database.py first
   - Add at least one face using capture_and_add_face.py
   - Verify database file permissions

2. "Could not open video capture device"
   - Check webcam connection
   - Verify webcam permissions
   - Try different video capture device number

3. Face recognition issues
   - Ensure good lighting conditions
   - Position face clearly in frame
   - Verify database has correct face encodings

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- face_recognition library developers
- OpenCV community
- Python SQLite team

## Future Improvements

- [ ] Web interface for remote monitoring
- [ ] Email/SMS notifications
- [ ] Multiple camera support
- [ ] Face recognition statistics and logging
- [ ] Enhanced security features
