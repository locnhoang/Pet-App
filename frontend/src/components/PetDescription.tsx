import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

interface Pet {
    PetID: number;
    Name: string;
    Age: number;
    Animal: string;
    Breed: string;
    PictureUrl: string;
    Description: string;
}

const PetDescription: React.FC = () => {
    let { id } = useParams();

    const user_id = localStorage.getItem('user_id');

    const [pet, setPet] = useState<Pet>();
    const [error, setError] = useState<string>('');

    const [save, setSave] = useState(false);

    const [status, setStatus] = useState<string>('Loading...');


    useEffect(() => {
        const fetchPet = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/pets/${id}`);
                const data: Pet = await response.json();
                setPet(data);
            } catch (err) {
                setError('Could not fetch pet. Please try again later.');
                console.error('Error fetching pet:', err);
            }
        };

        const fetchSave = async () => {
            try {
                const response2 = await fetch(`http://127.0.0.1:5000/api/saved/${user_id}/${id}`);
                const data2: boolean = await response2.json();
                setSave(data2);
            } catch (err) {
                console.error('Error fetching save:', err);
            }
        };
        
        const fetchStatus = async () => {
            fetch(`http://localhost:5000/api/user/${user_id}/status`)
                .then(res => res.json())
                .then(data => {
                    if (data.status) {
                        setStatus(`${data.status}`);
                    } else {
                        setStatus('Unable to retrieve status.');
                        }
                    })
                .catch(() => setStatus('Network error.'));
            
            // if (status != "approved") {
            //     if (status == "not submitted") {
            //         setMessage(`Please fill out the questionnaire and wait for it to be approved!`);
            //         return;
            //     }
            //     setMessage(`Your questionnaire was not approved, sorry!`);
            //     return;
            // }
        };

        fetchPet();
        fetchSave();
        fetchStatus();
    }, []);


    const [message, setMessage] = useState('');

    const handleApply = async (e: React.FormEvent) => {
        e.preventDefault();
    
        //const user_id = localStorage.getItem('user_id');
        if (!user_id) {
          setMessage("You're not logged in.");
          return;
        }

        if (!pet || !pet.Name) {
            setMessage("Invalid pet.")
            return;
        }
    
        const payload = {
          user_id: Number(user_id),
          pet_id: Number(pet.PetID)
        };

        if (status != "approved") {
            if (status == "not submitted") {
                setMessage(`Please fill out the questionnaire and wait for it to be approved!`);
                return;
            }
            setMessage(`Your questionnaire was not approved, sorry!`);
            return;
        }
    
        try {
          const res = await fetch('http://localhost:5000/api/application', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });
    
          if (res.ok) {
            setMessage('Application submitted successfully!');
          } else {
            const data = await res.json();
            setMessage(data.error || 'Submission failed.');
          }
        } catch (error) {
          console.error('Network error:', error);
          setMessage('Network error.');
        }
      };


    const [message2, setMessage2] = useState('');

    const handleSave = async (e: React.FormEvent) => {    
        e.preventDefault();
    
        if (!user_id) {
          setMessage2("You're not logged in.");
          return;
        }

        if (!pet || !pet.Name) {
            setMessage2("Invalid pet.")
            return;
        }
    
        const payload = {
          user_id: Number(user_id),
          pet_id: Number(pet.PetID)
        };
        

        try {
          const res = await fetch('http://localhost:5000/api/saved', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });
    
          if (res.ok) {
            setMessage2('');

            try {
                const response2 = await fetch(`http://127.0.0.1:5000/api/saved/${user_id}/${id}`);
                const data2: boolean = await response2.json();
                setSave(data2);
            } catch (err) {
                console.error('Error fetching save:', err);
            }
          } else {
            const data = await res.json();
            setMessage2(data.error || 'Submission failed.');
          }
        } catch (error) {
          console.error('Network error:', error);
          setMessage2('Network error.');
        }
    };

    return (
        <div className="pet_description">
            <br></br>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {pet ? (
                pet.Name ? (
                    <div className="pet_description2">
                        <img src={`http://127.0.0.1:5000${pet.PictureUrl}`} alt={pet.Name} className="pet-description-image"/>
                        <br></br>
                        <h2>{ pet.Name }</h2>
                        {(pet.Breed != "N/A") && <h3>Animal: { pet.Animal }, Breed: { pet.Breed }</h3>}
                        {(pet.Breed == "N/A") && <h3>Animal: { pet.Animal }, No Breed Specified</h3>}
                        <a>{ pet.Name } is { pet.Age } years old!</a>
                        <br></br>
                        <a>{ pet.Description }</a>
                        <br></br>
                        <br></br>
                        <form onSubmit={handleApply}>
                            <button className="select-btn" >Apply for Adoption</button>
                            <p>{message}</p>
                        </form>
                        <form onSubmit={handleSave}>
                            {!save && <button className="select-btn" style={{ marginLeft: '10px'}}>Save for Later</button>}
                            {save && <button className="select-btn" style={{ marginLeft: '10px'}}>Unsave Pet</button>}
                            <p>{message2}</p>
                        </form>
                    </div>
                ) : (<p>This PetID does not exist</p>)
            ) : (
                <p>Something went wrong</p>
            )}

            {/* {pet && <img src={`http://127.0.0.1:5000${pet.PictureUrl}`} alt={pet.Name} className="pet-description-image"/>}
            <br></br>
            {pet && <h2>{ pet.Name }</h2>}
            { pet && (pet.Breed != "N/A") && <h3>Animal: { pet.Animal }, Breed: { pet.Breed }</h3>}
            { pet && (pet.Breed == "N/A") && <h3>Animal: { pet.Animal }, No Breed Specified</h3>}
            {pet && <a>{ pet.Name } is { pet.Age } years old!</a>}
            <br></br>
            {pet && <a>{ pet.Description }</a>} */}

        </div>
    );

};

export default PetDescription;
