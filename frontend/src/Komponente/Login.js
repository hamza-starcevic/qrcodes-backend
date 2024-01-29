import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async () => {

    const backendUrl = 'https://7a77-147-161-130-104.ngrok-free.app';
  
    try {
      const response = await fetch(`${backendUrl}/api/user/login`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: username,
          password: password,
        }),
      });
  
      /*if (!response.ok) {
        console.error('Authentication failed. Server returned:', response.status, response.statusText);
        return;
      }*/
  
      const result = await response.json();
        const token = result.token;
        console.log('3');
        // Store the token in localStorage or state as needed
        // Example using localStorage:
        localStorage.setItem('authToken', token);
  
        console.log('Login successful! Token:', token);
        navigate('/predavanja')
  
        // Add your logic to redirect or perform additional actions after successful login
      
    } catch (error) {
      console.error('Error during login:', error);
    }
  };
  

  return (
    <div className="Prijava">
      <h2>Prijava</h2>
      <p>Molimo vas da se prijavite kako bi koristili nasu aplikaciju</p>
      <form>
        <label>
          Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <br/>
        <div className="wrapper">
        <label className="remember-label">
          <input className="remember" type="checkbox" checked={rememberMe} onChange={() => setRememberMe(!rememberMe)} />
          Remember me
        </label>
        <span className="forgot-password">Zaboravili ste lozinku?</span>
        </div>
        <br/>
        <div className="button-wrapper">
        <button type="button" onClick={handleLogin}>Login</button></div>
      </form>
    </div>
  );
};

export default Login;
