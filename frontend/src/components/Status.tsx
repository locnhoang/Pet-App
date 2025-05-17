import React, { useEffect, useState } from 'react';

const Status: React.FC = () => {
  const [status, setStatus] = useState<string>('Loading...');
  const [applyStatus, setApplyStatus] = useState<string[]>(['Loading...']);
  const userId = localStorage.getItem('user_id');

  useEffect(() => {
    if (!userId) {
      setStatus('You are not logged in.');
      return;
    }

    fetch(`http://localhost:5000/api/user/${userId}/status`)
      .then(res => res.json())
      .then(data => {
        if (data.status) {
          setStatus(`Your questionnaire status: ${data.status}`);
        } else {
          setStatus('Unable to retrieve status.');
        }
      })
      .catch(() => setStatus('Network error.'));

    fetch(`http://localhost:5000/api/user/${userId}/apply_status`)
      .then(res2 => res2.json())
      .then(data2 => {
        if (data2.length > 0) {
          const applications: string[] = [];
          for (let i=0; i<data2.length; i++) {
            applications.push(`Your application status for ${data2[i].pet_name}: ${data2[i].status}`)
          }
          setApplyStatus(applications);
        } else {
          setApplyStatus(['No status to retrieve.']);
        }
        
      })
      .catch(() => setApplyStatus(['Network error.']));
  }, [userId]);

  return (
    <div>
      <h2>Status Page</h2>
      <h3>Questionnaire Status:</h3>
      <p>{status}</p>
      <br></br>
      <h3>Application Status:</h3>
      {applyStatus.map((status, index) => (
        <p key={index}>{status}</p> ))}
    </div>
  );
};

export default Status;
