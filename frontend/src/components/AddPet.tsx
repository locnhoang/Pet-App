import React, { useState } from 'react';

const AddPet: React.FC = () => {
  const [formData, setFormData] = useState({
    Name: '',
    Age: '',
    Breed: '',
    Animal: '',
    PictureUrl: '',
    Description: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch('http://localhost:5000/api/admin/add_pet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    const data = await res.json();
    alert(data.message || data.error);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add New Pet</h2>
      <input name="Name" placeholder="Name" onChange={handleChange} required />
      <input name="Age" placeholder="Age" type="number" onChange={handleChange} required />
      <input name="Breed" placeholder="Breed" onChange={handleChange} />
      <input name="Animal" placeholder="Animal" onChange={handleChange} required />
      <input name="PictureUrl" placeholder="Image URL" onChange={handleChange} />
      <textarea name="Description" placeholder="Description" onChange={handleChange} />
      <button type="submit">Add Pet</button>
    </form>
  );
};

export default AddPet;
