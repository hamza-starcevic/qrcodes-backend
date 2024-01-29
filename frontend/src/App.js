import React from 'react';
import './App.css';
import Login from './Komponente/Login';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Komponente/Navbar';
import Predavanja from './Komponente/Predavanja';
import Predmet from './Komponente/Predmet';
import Prisustvo from './Komponente/Prisustvo';
import Profesor from './Komponente/Profesor';
import Ucenici from './Komponente/Ucenici';
import LandingPage from './Komponente/Landingpage';

function App() {
  const authToken = localStorage.getItem('authToken');
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          {/* Public routes (accessible without authentication) */}
          <Route path="/prijava" element={<Login />} />
          <Route path="/" element={<LandingPage />} />

          {/* Protected routes (require authentication) */}
          {authToken ? (
            <>
              <Route path="/predavanja" element={<Predavanja />} />
              <Route path="/predmet" element={<Predmet />} />
              <Route path="/prisustvo" element={<Prisustvo />} />
              <Route path="/profesor" element={<Profesor />} />
              <Route path="/ucenici" element={<Ucenici />} />
            </>
          ) : (
            <Route path="/" element={<LandingPage />} />
          )}
        </Routes>
      </div>
    </Router>

  );
}

export default App;
