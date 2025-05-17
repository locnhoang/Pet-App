from flask import jsonify, request
from initialize_db import get_database_connection
import sqlite3

def create_user():
    """
    Creates a new user
    ---
    parameters:
      - name: username
        in: body
        type: string
        required: true
      - name: password
        in: body
        type: string
        required: true
    responses:
        200:
            description: User created successfully
        400:
            description: Invalid input
        409:
            description: Email already exists
    """
    
    # Replaced with mocks
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    # name = "test"
    # email = "test"
    # password = "test"

    if not name or not email or not password:
        return jsonify({'error': 'Name, email and password are required'}), 400

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (Name, Email, Password) VALUES (?, ?, ?)",
            (name, email, password))
        connection.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()

    #print("Created User")
    #return jsonify({'message': 'User created successfully'}), 201



def log_user():
    """
    Logs in user
    ---
    - name: username
        in: body
        type: string
        required: true
      - name: password
        in: body
        type: string
        required: true
    responses:
        200:
            description: Login successful
        401:
            description: Invalid email or password
    """

    # Replaced with mocks
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # username = "test"
    # password = "test"

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT UserID, Password FROM users WHERE Email = ?", (email,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Check if the provided password matches the hashed password stored in the database
        if user['Password'] == password:
            return jsonify({'message': 'Login successful', 'user_id': user['UserID']}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()

    #print("User Logged In")
    #return jsonify({'message': 'User logged in successfully'}), 200
