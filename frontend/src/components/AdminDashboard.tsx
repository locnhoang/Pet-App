import React, { useEffect, useState } from 'react';

interface Item { ID:number; UserID:number; Responses:string; }

const AdminDashboard: React.FC = () => {
  const [items,setItems] = useState<Item[]>([]);
  const [msg,setMsg] = useState('');

  const load = () =>
    fetch('http://localhost:5000/api/admin/questionnaires')
      .then(r=>r.json()).then(setItems);

      useEffect(() => {
        load();
      }, []);
      

  const decide = (id:number, approve:number) =>
    fetch(`http://localhost:5000/api/admin/questionnaires/${id}`,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({approve})
    }).then(()=>{setMsg('Updated'); load();});

  return (
    <div>
      <h2>Pending Questionnaires</h2>
      {items.length <= 0 && <p>No Current Pending Questionnaires</p>}
      {items.map(it=>(
        <div key={it.ID} style={{border:'1px solid #ccc',padding:8,margin:8}}>
          <p><strong>User {it.UserID}</strong></p>
          <p>{it.Responses}</p>
          <button onClick={()=>decide(it.ID,1)}>Approve</button>
          <button onClick={()=>decide(it.ID,0)} style={{marginLeft:8}}>Deny</button>
        </div>
      ))}
      <p>{msg}</p>
      <br></br>
      {/* <h2>Pending Applications</h2> */}
      
    </div>
  );
};
export default AdminDashboard;
