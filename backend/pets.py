from flask import jsonify, request
from initialize_db import get_database_connection
import sqlite3

def get_pets():
    """Get all available pets.
    ---
    responses:
        200:
            description: A list of pets
            schema:
                type: array
                items:
                    $ref: '#/definitions/Pet'
        500:
            description: Internal Server Error
    definitions:
        Pet:
            type: object
            properties:
                id:
                    type: integer
                name:
                    type: string
                breed:
                    type: string
                age:
                    type: integer
                temperament:
                    type: string
                pictureUrl:
                    type: string
    """

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM pets")
        pets = cursor.fetchall()
        pet_list = [dict(row) for row in pets]
        return jsonify(pet_list), 200
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()

    #mock = [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'test2',}]
    #return jsonify(mock), 200

def get_individual_pet_info(id):
    connection = get_database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pets WHERE PetID = ?", (id,))
        pet = cursor.fetchone()
        if pet is None:
            return {'error': 'Pet not found'}
        return dict(pet)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {'error': 'Internal Server Error'}
    finally:
        connection.close()

def get_pet_info(id):
    """Get a pet by its ID.
    ---
    responses:
        200:
            description: A single pet
        404:
            description: Pet not found
    """
    # pet = get_individual_pet_info(id)
    # if pet == {'error': 'Pet not found'}:
    #     jsonify({'error': 'Pet not found'}), 404
    # elif pet == {'error': 'Internal Server Error'}:
    #     jsonify({'error': 'Internal Server Error'}), 500
    # return jsonify(pet), 200

    connection = get_database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pets WHERE PetID = ?", (id,))
        pet = cursor.fetchone()
        if pet is None:
            return jsonify({'error': 'Pet not found'}), 404
        return jsonify(dict(pet)), 200
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()

    #mock = {'id': 1, 'name': 'test'}
    #return jsonify(mock), 200

# def add_pet():
#     data = request.get_json()
#     name = data.get('name')
#     age = data.get('age')
#     breed = data.get('breed')

#     if not name or not age or not breed:
#         return jsonify({'error': 'Name, age and breed are required'}), 400

#     connection = get_database_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("INSERT INTO Pets (PetID, Name, Age, Breed) VALUES (?, ?, ?, ?)", (1, name, age, breed))
#         connection.commit()
#         return jsonify({'message': 'Pet created successfully'}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({'error': 'Pet already exists'}), 409
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         return jsonify({'error': 'Internal Server Error'}), 500
#     finally:
#         connection.close()

def search_pets(input):
    return input