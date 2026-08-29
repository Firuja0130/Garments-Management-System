import cv2
import numpy as np
import os
from django.conf import settings

from .models import RegisteredFace


def recognize_face(image):
    """
    Compare the camera image with registered employee faces.
    Returns the matching RegisteredFace object or None.
    """

    # Convert camera image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load Haar Cascade from project folder
    base_dir = settings.BASE_DIR

    cascade_path = os.path.join(
        base_dir,
        "haarcascade_frontalface_default.xml"
    )

    detector = cv2.CascadeClassifier(cascade_path)

    if detector.empty():
        raise Exception(
            f"Face detector could not be loaded from: {cascade_path}"
        )

    # Detect face in captured camera image
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        return None

    # Use the first detected face
    x, y, w, h = faces[0]

    captured_face = gray[y:y+h, x:x+w]

    # Resize captured face
    captured_face = cv2.resize(
        captured_face,
        (200, 200)
    )

    # Get all registered faces
    registered_faces = RegisteredFace.objects.select_related(
        'employee',
        'employee__employee'
    )

    best_match = None
    best_score = float('inf')

    for registered in registered_faces:

        image_path = os.path.join(
            settings.MEDIA_ROOT,
            str(registered.face_image)
        )

        # Read registered face image
        stored_image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if stored_image is None:
            continue

        # Detect face in registered image
        stored_faces = detector.detectMultiScale(
            stored_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        if len(stored_faces) == 0:
            continue

        sx, sy, sw, sh = stored_faces[0]

        stored_face = stored_image[
            sy:sy+sh,
            sx:sx+sw
        ]

        # Resize registered face
        stored_face = cv2.resize(
            stored_face,
            (200, 200)
        )

        # Compare captured face with registered face
        difference = cv2.absdiff(
            captured_face,
            stored_face
        )

        score = np.mean(difference)

        if score < best_score:
            best_score = score
            best_match = registered

    # Recognition threshold
    if best_match and best_score < 60:
        return best_match

    return None