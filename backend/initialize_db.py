import sqlite3

def initialize_db():
    conn = sqlite3.connect('pet.db') 
    cursor = conn.cursor()

    # Create PetTypes table first as it is referenced by Pets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS PetTypes (
        PetTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        NameType TEXT NOT NULL
    );''')
    
    # Create Pets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Pets (
        PetID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Age INTEGER NOT NULL,
        Animal TEXT NOT NULL,
        Breed TEXT NOT NULL,
        PictureUrl TEXT,
        Description TEXT,
        PetTypeID INTEGER,
        FOREIGN KEY (PetTypeID) REFERENCES PetTypes(PetTypeID)
    );''')
    
    # Create Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    );''')
    
    # Create Survey table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Survey (
        SurveyID INTEGER PRIMARY KEY AUTOINCREMENT,
        QuestionText TEXT NOT NULL
    );''')
    
    # Create Admin table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
        AdminID  INTEGER PRIMARY KEY AUTOINCREMENT,
        Name     TEXT NOT NULL,
        Email    TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    );''')
    
    # Create SavedPets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS SavedPets (
        SavedPetID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        PetID INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (PetID) REFERENCES Pets(PetID)
    );''')
    
    # Create Applications table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Applications (
        ApplicationID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        PetID INTEGER,
        Approved INTEGER
    );''')
    
    # Create UserAnswers table
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserAnswers (
        AnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        QuestionID INTEGER,
        ChoiceID INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (QuestionID) REFERENCES Survey(SurveyID),
        FOREIGN KEY (ChoiceID) REFERENCES Choices(ChoiceID)
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS QuestionnaireText (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Responses TEXT NOT NULL,
        Approved INTEGER,                     -- NULL = pending, 1=yes, 0=no
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );''')

    cursor.execute("SELECT * FROM Admin WHERE Email = ?", ('admin@pao.com',))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO Admin (Name, Email, Password) VALUES (?, ?, ?)",
                    ('Admin', 'admin@pao.com', 'admin'))
        
    conn.execute("INSERT INTO pets (Name, Age, Animal, Breed, PictureUrl, Description) VALUES (?, ?, ?, ?, ?, ?)", ("Charlie", 5, "Cat", "N/A", "/images/charlie.jpg", "A good cat"))
    conn.execute("INSERT INTO pets (Name, Age, Animal, Breed, PictureUrl, Description) VALUES (?, ?, ?, ?, ?, ?)", ("Nacho", 3, "Lizard", "N/A", "/images/nacho.jpg", "A cool lizard"))
    conn.execute("INSERT INTO pets (Name, Age, Animal, Breed, PictureUrl, Description) VALUES (?, ?, ?, ?, ?, ?)", ("Theo", 4, "Dog", "Bernese Mountain", "/images/theo.jpeg", "A funny dog"))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Open connection to the database
def get_database_connection():
    connection = sqlite3.connect('pet.db')
    connection.row_factory = sqlite3.Row
    return connection


if __name__ == "__main__":
    initialize_db()
