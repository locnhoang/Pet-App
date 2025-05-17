import pytest
import sqlite3
from main import app
from initialize_db import initialize_db, get_database_connection

@pytest.fixture(autouse=True)
def setup_db():
    """Re-initialize the database before each test run"""
    initialize_db()
    yield

@pytest.fixture
def client():
    """Create a test client for Flask App"""
    app.testing = True
    with app.test_client() as client:
        clear_test_users()
        yield client
    #return app.test_client()

def clear_test_users():
    conn = sqlite3.connect('pet.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE name='test';")
    cursor.execute("DELETE FROM pets WHERE name='test';")
    conn.commit()
    conn.close()

def test_sign_up_user(client):
    """Test user sign up"""
    response = client.post('/api/sign_up', json={'name': 'test', 'email': 'test', 'password': 'test'})
    assert response.status_code == 201
    assert response.json == {'message': 'User created successfully'}
    conn = get_database_connection()
    user = conn.execute("SELECT * FROM users WHERE name = ?", ('test',)).fetchone()
    assert user is not None
    conn.close()

def test_login_user(client):
    """Test user login"""
    create_response = client.post('/api/sign_up', json={'name': 'test', 'email': 'test', 'password': 'test'})
    assert create_response.status_code == 201

    response = client.post('/api/login', json={'email': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert 'user_id' in response.json

def test_pets(client):
    """Test retrieve pets"""
    conn = get_database_connection()
    conn.execute("INSERT INTO pets (Name, Age, Animal, PictureUrl) VALUES (?, ?, ?, ?)", ("Nacho", 3, "Lizard", "/images/nacho.jpg"))
    conn.execute("INSERT INTO pets (Name, Age, Animal, Breed, PictureUrl) VALUES (?, ?, ?, ?, ?)", ("Test", 3, "Test", "Test", "/images/theo.jpeg"))
    conn.commit()
    conn.close()

    response = client.get('/api/pets')
    assert response.status_code == 200
    assert len(response.json) > 0

    in_db = False
    for i in response.json:
        if i["Name"] == "Test":
            in_db = True
    # assert response.json[0]["Name"] == "Test"
    assert in_db

def test_pet_info(client):
    """Test retrieve single pet info"""
    conn = get_database_connection()
    conn.execute("INSERT INTO pets (Name, Age, Aniaml, Breed, PictureUrl) VALUES (?, ?, ?, ?, ?)", ("Test", 4, "Test", "Test", "/images/charlie.jpg"))
    pet_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()

    response = client.get(f'/api/pets/{pet_id}')
    assert response.status_code == 200
    assert response.json["Name"] == "Test"


def test_home_page(client):
    """Test that the home page route returns successfully"""
    resp = client.get("/")
    assert resp.status_code == 200
