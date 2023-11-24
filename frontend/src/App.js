import React from 'react';
import './App.css';
import Login from './Komponente/Login';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Komponente/Navbar';
import Predavanja from './Komponente/Predavanja';
import Predmet from './Komponente/Predmet';
import Prisustvo from './Komponente/Prisustvo';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/predavanja" element={<Predavanja/>} />
          <Route path="/predmet" element={<Predmet/>} />
          <Route path="/prisustvo" element={<Prisustvo/>} />

        </Routes>
      </div>
    </Router>
    
  );
}

export default App;
