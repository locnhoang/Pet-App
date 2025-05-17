from flask import jsonify, request
from initialize_db import get_database_connection
from pets import get_individual_pet_info
import sqlite3

def changeSaveState():
    data = request.get_json()
    user_id = data.get("user_id")
    pet_id = data.get("pet_id")

    if not user_id or not pet_id:
        return jsonify({"error": "Missing user_id or pet_id"}), 400

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        if petSaveState(user_id, pet_id):
            #cursor.execute("DELETE FROM SavedPets WHERE UserID = 1")
            cursor.execute("DELETE FROM SavedPets WHERE UserID = ? AND PetID = ?", (user_id, pet_id))
            connection.commit()
            return jsonify({'message': 'Pet added removed'}), 202
        else:
            cursor.execute("INSERT INTO SavedPets (UserID, PetID) VALUES (?, ?)", (user_id, pet_id))
            connection.commit()
            return jsonify({'message': 'Pet added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Pet already exists in saved'}), 409
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()

def getSavedPets(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM SavedPets WHERE UserID = ?", (user_id,))
        pets = cursor.fetchall()
        if pets is None:
            return {'error': 'Not pets found'}
        return pets
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {'error': 'Internal Server Error'}
    finally:
        connection.close()

def savedPets(user_id):
    pets = getSavedPets(user_id)
    if (pets == {'error': 'Not pets found'}):
        return jsonify({'error': 'Not pets found'}), 404
    elif (pets == {'error': 'Internal Server Error'}):
        return jsonify({'error': 'Internal Server Error'}), 500
    pet_list = [dict(row) for row in pets]
    new_pet_list = []
    for pet in pet_list:
        print(get_individual_pet_info(pet["PetID"]))
        new_pet_list.append(get_individual_pet_info(pet["PetID"]))
    return jsonify(new_pet_list), 200

def petSaveState(user_id, pet_id):
    pets = getSavedPets(user_id)
    for pet in pets:
        if pet["PetID"] == pet_id:
            return True
    return False

def isPetSaved(user_id, pet_id):
    return jsonify(petSaveState(user_id, pet_id)), 200