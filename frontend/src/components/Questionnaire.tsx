import React, { useState } from 'react';

const Questionnaire: React.FC = () => {
  const [responses, setResponses] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const user_id = localStorage.getItem('user_id');
    if (!user_id) {
      setMessage("You're not logged in.");
      return;
    }

    const payload = {
      user_id: Number(user_id),
      responses: responses.trim()
    };

    try {
      const res = await fetch('http://localhost:5000/api/questionnaire', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        setMessage('Questionnaire submitted successfully!');
        setResponses(''); // clear form
      } else {
        const data = await res.json();
        setMessage(data.error || 'Submission failed.');
      }
    } catch (error) {
      console.error('Network error:', error);
      setMessage('Network error.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Adoption Questionnaire</h2>
      <textarea
        value={responses}
        onChange={(e) => setResponses(e.target.value)}
        placeholder="Describe your experience with pets, why you want to adopt, etc."
        rows={6}
        style={{ width: '100%', padding: '0.5rem' }}
        required
      />
      <br />
      <button type="submit">Submit Questionnaire</button>
      <p>{message}</p>
    </form>
  );
};

export default Questionnaire;
