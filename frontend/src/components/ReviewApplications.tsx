import React, { useEffect, useState } from 'react';

interface Application {
  ApplicationID: number;
  UserName: string;
  PetName: string;
}

const ReviewApplications: React.FC = () => {
  const [apps, setApps] = useState<Application[]>([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/api/admin/applications')
      .then(res => res.json())
      .then(setApps)
      .catch(() => setMessage("Failed to load applications."));
  }, []);

  const handleDecision = (id: number, approved: number) => {
    fetch(`http://localhost:5000/api/admin/applications/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approved })
    }).then(() => {
      setMessage("Updated.");
      setApps(apps.filter(app => app.ApplicationID !== id)); 
    });
  };

  return (
    <div>
      <h2>Pending Adoption Applications</h2>
      {apps.map(app => (
        <div key={app.ApplicationID}>
          <p><strong>{app.UserName}</strong> applied for <strong>{app.PetName}</strong></p>
          <button onClick={() => handleDecision(app.ApplicationID, 1)}>Approve</button>
          <button onClick={() => handleDecision(app.ApplicationID, 0)}>Deny</button>
        </div>
      ))}
      <p>{message}</p>
    </div>
  );
};

export default ReviewApplications;
