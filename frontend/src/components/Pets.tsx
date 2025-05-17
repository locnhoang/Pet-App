import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Pet {
    PetID: number;
    Name: string;
    Age: number;
    Animal: string;
    Breed: string;
    PictureUrl: string;
}

const Pets: React.FC = () => {
    const [pets, setPets] = useState<Pet[]>([]);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        const fetchPets = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/pets');
                const data: Pet[] = await response.json();
                setPets(data);
            } catch (err) {
                setError('Could not fetch pets. Please try again later.');
                console.error('Error fetching pets:', err);
            }
        };

        fetchPets();
    }, []);

    const renderPetCard = (pet: Pet) => (
        <div className="pet-card" key={pet.PetID}>
            <img src={`http://127.0.0.1:5000${pet.PictureUrl}`} alt={pet.Name} className="pet-image"/>
            <h3>{pet.Name}</h3>
            <p>Age: {pet.Age}</p>
            <p>Animal: {pet.Animal}</p>
            {(pet.Breed != "N/A") && <p>Breed: {pet.Breed}</p>}
            {(pet.Breed == "N/A") && <p> No Breed Specified</p>}
            <Link to={`/pet_description/${pet.PetID}`}>
                <button className="select-btn">Select Pet</button>
            </Link>
        </div>
        
        // <Card bg={"light-blue"} border="primary" style={{ width: '18rem' }}>
        //     <Card.Body>
        //         <Card.Title>{pet.Name} - {pet.Age}</Card.Title>
        //         <Card.Text>
        //             {pet.Breed}
        //         </Card.Text>
        //         <div className="pet-card" key={pet.PetID}>
        //             <img src={`http://127.0.0.1:5000${pet.PictureUrl}`} alt={pet.Name} width="200" className="pet-image"/>
        //             <h3>{pet.Name}</h3>
        //             <p>Age: {pet.Age}</p>
        //             <p>Breed: {pet.Breed}</p>
        //             <button className="select-btn">Select Pet</button>
        //         </div>
        //     </Card.Body>
        // </Card>
    );

    const [query, setQuery] = useState<string>("");
  
    console.log("Available pets:", pets);
    
    const filteredPets = pets.filter((pet) =>
        (pet.Breed != "N/A") ? (
            `${pet.Name} ${pet.Animal} ${pet.Breed} ${pet.Age}`.toLowerCase().includes(query.toLowerCase())
        ) : (
            `${pet.Name} ${pet.Animal} ${pet.Age}`.toLowerCase().includes(query.toLowerCase())
        )
    );

    return (
        <div className="pets-list">
            <h1>These Pets Need A New Home!</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            
            <div className="search-container">
                <input
                    type="text"
                    placeholder="Search by name, breed, or age..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="search-input"
                />

                <div className="pet-list-container">
                    {pets.length > 0 ? (
                        filteredPets.length > 0 ? (
                            filteredPets.map(renderPetCard)
                        ) : (
                            <p>No matching pets found.</p>
                        )
                    ) : (
                        <p>No pets available at this moment.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Pets;