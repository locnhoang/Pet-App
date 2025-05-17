from flask import request, jsonify
from initialize_db import get_database_connection
from pets import get_individual_pet_info

def submit_application():
    data = request.get_json()
    user_id = data.get("user_id")
    pet_id = data.get("pet_id")

    if not user_id or not pet_id:
        return jsonify({"error": "Missing user_id or pet_id"}), 400

    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Applications (UserID, PetID) VALUES (?, ?)",
            (user_id, pet_id)
        )
        conn.commit()
        return jsonify({"message": "Application submitted"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Submission failed"}), 500
    finally:
        conn.close()
        
def get_application_status(user_id):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT PetID FROM Applications WHERE UserID = ?", (user_id,))
    pet_ids = cursor.fetchall()
    cursor.execute("SELECT Approved FROM Applications WHERE UserID = ?", (user_id,))
    applications = cursor.fetchall()
    conn.close()

    application_list = [dict(row) for row in applications]
    pet_id_list = [dict(row) for row in pet_ids]
    output = []
    for i in range(len(application_list)):
        pet_info = get_individual_pet_info(pet_id_list[i]['PetID'])
        petName = pet_info['Name']
        if application_list[i] is None:
            output.append({'status': 'not submitted', 'pet_name': petName})
        elif application_list[i]['Approved'] is None:
            output.append({'status': 'pending', 'pet_name': petName})
        elif application_list[i]['Approved'] == 1:
            output.append({'status': 'approved', 'pet_name': petName})
        else:
            output.append({'status': 'denied', 'pet_name': petName})
    return jsonify(output), 200
