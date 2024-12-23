import cv2
import face_recognition
import numpy as np
from .models import Voter

def register_voter(voter_id):
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the webcam.")
        return

    try:
        if Voter.objects.filter(voter_id=voter_id).exists():
            print(f"Voter ID {voter_id} is already registered.")
            return

        print("Please position your face within the frame for registration.")
        face_registered = False

        while not face_registered:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Could not capture image from webcam.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Green rectangle
                cv2.imshow("Register Face", frame)

            if len(face_locations) == 1:
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                face_encoding_bytes = face_encoding.tobytes()
                voter = Voter(voter_id=voter_id, face_encoding=face_encoding_bytes)
                voter.save()
                print(f"Voter ID {voter_id} registered successfully.")
                face_registered = True

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting registration process.")
                break

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        video_capture.release()
        cv2.destroyAllWindows()

def start_video_capture(voter_id):
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the webcam.")
        return False

    print("Please position your face within the frame to log in.")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not capture image from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)  # Blue rectangle
            cv2.imshow("Login Face", frame)

        if len(face_locations) > 0:
            login_face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            try:
                voter = Voter.objects.get(voter_id=voter_id)
                db_face_encoding = np.frombuffer(voter.face_encoding, dtype=np.float64)
                matches = face_recognition.compare_faces([db_face_encoding], login_face_encoding)

                if matches[0]:
                    print("Login Successful!")
                    cv2.putText(frame, "Login Successful!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Login Face", frame)
                    cv2.waitKey(2000)  # Wait for 2 seconds to display success message
                    return True
                else:
                    print("Face did not match. Login failed.")
                    cv2.putText(frame, "Login Failed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("Login Face", frame)
                    cv2.waitKey(2000)  # Wait for 2 seconds to display failure message
                    return False

            except Voter.DoesNotExist:
                print("Voter ID not found in the database.")
                cv2.putText(frame, "Voter ID not found", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Login Face", frame)
                cv2.waitKey(2000)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting login process.")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return False
