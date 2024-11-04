import mediapipe as mp
import numpy as np
import math
import cv2

from Hair_Detection import detect_hair

def detect_face(image_rgb, image_resized, width, height):
    # Initialize Mediapipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils

    # Initialize Face Mesh model
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5) as face_mesh:
    
        # Process the image to detect facial landmarks
        results = face_mesh.process(image_rgb)

        # Check if landmarks are detected
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw facial landmarks on the image (optional)
                #mp_drawing.draw_landmarks(
                    #image_resized,
                    #face_landmarks,
                    #mp_face_mesh.FACEMESH_CONTOURS,
                    #mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    #mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1))

                # Get bounding box coordinates
                face_coords = [(landmark.x, landmark.y) for landmark in face_landmarks.landmark]
                face_coords = np.array(face_coords)
                x_min = int(np.min(face_coords[:, 0]) * width)
                x_max = int(np.max(face_coords[:, 0]) * width)
                y_min = int(np.min(face_coords[:, 1]) * height)
                y_max = int(np.max(face_coords[:, 1]) * height)

                # Ensure coordinates are within image bounds
                x_min = max(0, x_min)
                y_min = max(0, y_min)
                x_max = min(width, x_max)
                y_max = min(height, y_max)

                # Calculate face orientation angle
                left_eye = face_landmarks.landmark[33]  # Left eye landmark
                right_eye = face_landmarks.landmark[263]  # Right eye landmark

                x1 = int(left_eye.x * width)
                y1 = int(left_eye.y * height)
                x2 = int(right_eye.x * width)
                y2 = int(right_eye.y * height)

                delta_x = x2 - x1
                delta_y = y2 - y1
                angle = math.atan2(delta_y, delta_x) * 180 / math.pi
                # Extract specific landmark points
                forehead_points = [(int(face_landmarks.landmark[i].x * image_resized.shape[1]), 
                                    int(face_landmarks.landmark[i].y * image_resized.shape[0])) for i in [10, 338, 297, 332]]
                jawline_points = [(int(face_landmarks.landmark[i].x * image_resized.shape[1]), 
                                int(face_landmarks.landmark[i].y * image_resized.shape[0])) for i in [152, 379, 400, 152]]
            
                # Detect hair and facial hair
                hair_present, facial_hair_present = detect_hair(image_resized, forehead_points, jawline_points)
                print("Hair Present:", hair_present)
                print("Facial Hair Present:", facial_hair_present)
                return angle, x_max, x_min, y_max, y_min
        else:
            print("No facial landmarks detected.")