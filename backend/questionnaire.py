from flask import request, jsonify
from initialize_db import get_database_connection

def submit_text_questionnaire():
    data = request.get_json()
    user_id = data.get("user_id")
    responses = data.get("responses")

    if not user_id or not responses:
        return jsonify({"error": "Missing user_id or responses"}), 400

    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO QuestionnaireText (UserID, Responses) VALUES (?, ?)",
            (user_id, responses)
        )
        conn.commit()
        return jsonify({"message": "Questionnaire submitted"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Submission failed"}), 500
    finally:
        conn.close()
        
def get_questionnaire_status(user_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Approved FROM QuestionnaireText WHERE UserID = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({'status': 'not submitted'}), 200
    elif row['Approved'] is None:
        return jsonify({'status': 'pending'}), 200
    elif row['Approved'] == 1:
        return jsonify({'status': 'approved'}), 200
    else:
        return jsonify({'status': 'denied'}), 200
