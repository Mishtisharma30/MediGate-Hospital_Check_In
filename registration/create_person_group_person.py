import face_recognition

def create_pgp(userId, path_to_image):
    """Extract a face encoding from the uploaded registration photo.
       Returns a 128-d numpy array, or 'Failed' if no usable face is found."""
    try:
        image = face_recognition.load_image_file(path_to_image)
        encodings = face_recognition.face_encodings(image)
    except Exception as e:
        print(e)
        return "Failed"

    if len(encodings) == 0:
        print("No face detected in uploaded photo.")
        return "Failed"

    return encodings[0]