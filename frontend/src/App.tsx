import React from 'react';
//import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import MenuBar from './components/MenuBar';
import Home from './components/Home';
import Login from './components/Login';
import Questionnaire from './components/Questionnaire';
import Pets from './components/Pets';
import PetDescription from './components/PetDescription';
import Saved from './components/Saved'
import Documents from './components/Documents'
import FAQ from './components/FAQ'
import AdminDashboard from './components/AdminDashboard';
import Status from './components/Status';
import AddPet from './components/AddPet';
import ReviewApplications from './components/ReviewApplications';

//function App() {
//const [count, setCount] = useState(0)
const App: React.FC = () => {
  return (
    /*<>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + Reac</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>*/

    <Router>
      <div>
        <MenuBar /> {/* Include the navigation bar */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/questionnaire" element={<Questionnaire />} />
          <Route path="/status" element={<Status />} />
          <Route path="/pets" element={<Pets />} />
          <Route path="/pet_description/:id" element={<PetDescription />} />
          <Route path="/saved" element={<Saved />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/faqs" element={<FAQ />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/review-applications" element={<ReviewApplications />} />
          <Route path="/add-pet" element={<AddPet />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
