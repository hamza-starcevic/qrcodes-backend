
import React from 'react';
import { Link } from 'react-router-dom'; // If you are using React Router

const Navbar = () => {
  return (
    <nav>
               <img src="Brand.png" alt="profile" />
      <ul>
      
        <li>
          <Link to="/">Početna</Link>
        </li>
        <li>
          <Link to="/predavanja">Predavanja</Link>
        </li>
        <li>
          <Link to="/predmet">Predmet</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;