import React, { useState } from 'react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("user_id", data.user_id.toString());
        setMessage(`Login successful! User ID: ${data.user_id}`);
        window.location.reload();
      } else {
        setMessage(data.error || 'Login failed');
      }
    } catch {
      setMessage('Network error');
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/sign_up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('Signup successful! You can now log in.');
      } else {
        setMessage(data.error || 'Signup failed');
      }
    } catch {
      setMessage('Network error');
    }
  };

  const handleAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('admin_id', data.admin_id.toString());
      localStorage.setItem('isAdmin', 'true');
      setMessage('Admin login successful');
      window.location.reload();
    } else {
      setMessage(data.error);
    }
  };

  return (
    <div className="container">
      <h2>Login / Sign Up</h2>
      <form>
        <input
          type="text"
          placeholder="Name (for signup)"
          value={name}
          onChange={(e) => setName(e.target.value)}
        /><br />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br />
        <button onClick={handleLogin}>User Login</button>
        <button onClick={handleSignUp} style={{ marginLeft: '10px' }}>Sign Up</button>
        <button onClick={handleAdminLogin} style={{ marginLeft: '10px', backgroundColor: '#ffbf00' }}>Admin Login</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default Login;
