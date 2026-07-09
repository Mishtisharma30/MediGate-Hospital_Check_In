import json
import face_recognition
import mysql.connector

def identify(image_path, db_user, db_password):
    """Compare the check-in photo against every stored encoding.
       Returns the matching User_ID, or None if nothing matches closely enough."""
    try:
        image = face_recognition.load_image_file(image_path)
        unknown_encodings = face_recognition.face_encodings(image)
    except Exception as e:
        print(e)
        return None

    if len(unknown_encodings) == 0:
        return None
    unknown_encoding = unknown_encodings[0]

    conn = mysql.connector.connect(host='localhost', user=db_user, password=db_password, database='master')
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, FaceEncoding FROM user")
    rows = cursor.fetchall()
    conn.close()

    THRESHOLD = 0.6  # lower = stricter. 0.6 is face_recognition's standard default.
    best_match_id, best_distance = None, THRESHOLD

    for user_id, encoding_json in rows:
        distance = face_recognition.face_distance([json.loads(encoding_json)], unknown_encoding)[0]
        if distance < best_distance:
            best_distance, best_match_id = distance, user_id

    return best_match_id