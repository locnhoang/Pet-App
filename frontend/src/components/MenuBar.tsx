import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const MenuBar: React.FC = () => {
  const isAdmin = localStorage.getItem('isAdmin') === 'true';
  const isUser = localStorage.getItem('user_id') !== null;
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <nav>
      <ul>
        <li><h3><Link to="/">Adopt Me!</Link></h3></li>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/questionnaire">Questionnaire</Link></li>
        {localStorage.getItem('user_id') && (
        <li><Link to="/status">Status</Link></li>)}
        <li><Link to="/pets">Pets</Link></li>
        {localStorage.getItem('user_id') && (
        <li><Link to="/saved">Saved</Link></li>)}
        <li><Link to="/documents">Documents</Link></li>
        <li><Link to="/faqs">FAQ</Link></li>
        {isAdmin && <li><Link to="/admin">Review Questionnaires</Link></li>}
        {localStorage.getItem("isAdmin") === "true" && <li><Link to="/add-pet">Add Pet</Link></li>}
        {localStorage.getItem('isAdmin') === 'true' && (<><li><Link to="/admin/review-applications">Review Applications</Link></li></>)}
        {(isUser || isAdmin) && <li><button onClick={handleLogout}>Logout</button></li>}
      </ul>
    </nav>
  );
};

export default MenuBar;
