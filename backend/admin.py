from flask import request, jsonify
from initialize_db import get_database_connection

def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT AdminID FROM Admin WHERE Email=? AND Password=?", (email, password))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({"message": "Admin login successful", "admin_id": row["AdminID"]}), 200
    return jsonify({"error": "Invalid admin credentials"}), 401


def get_pending_questionnaires():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QuestionnaireText WHERE Approved IS NULL;")
    pending = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(pending), 200


def set_questionnaire_decision(q_id, approve):
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("UPDATE QuestionnaireText SET Approved=? WHERE ID=?", (approve, q_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "updated"}), 200

def add_pet():
    data = request.get_json()
    name = data.get('Name')
    age = data.get('Age')
    breed = data.get('Breed')
    animal = data.get('Animal')
    picture = data.get('PictureUrl')
    description = data.get('Description', '')

    if not name or not age or not animal:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO Pets (Name, Age, Animal, Breed, PictureUrl, Description, PetTypeID) VALUES (?, ?, ?, ?, ?, ?, NULL)",
    (name, age, animal, breed, picture, description)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Pet added successfully'}), 201

def get_pending_applications():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Applications.ApplicationID, Users.Name AS UserName, Pets.Name AS PetName, Applications.Approved
        FROM Applications
        JOIN Users ON Applications.UserID = Users.UserID
        JOIN Pets ON Applications.PetID = Pets.PetID
        WHERE Applications.Approved IS NULL
    """)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(results), 200

def set_application_decision(app_id, approved):
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Applications SET Approved = ? WHERE ApplicationID = ?", (approved, app_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Application updated"}), 200
