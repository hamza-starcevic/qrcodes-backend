import React, { useState } from 'react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleLogin = async () => {
    const backendUrl = 'http://127.0.0.1:8000';
  
    try {
      const response = await fetch(`${backendUrl}/api/user/login`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: String(username),
          password: String(password),
        }),
        credentials: 'include',
      });
  
      if (!response.ok) {
        console.error('Authentication failed. Server returned:', response.status, response.statusText);
        return;
      }
  
      const result = await response.json();
  
      if (Array.isArray(result) && result.length > 0) {
        const user = result[0];
  
        const token = user ? user.token : null;
  
        // Store the token in localStorage or state as needed
        // Example using localStorage:
        localStorage.setItem('authToken', token);
  
        console.log('Login successful! Token:', token);
  
        // Add your logic to redirect or perform additional actions after successful login
      } else {
        console.error('Authentication failed. Unexpected response:', result);
      }
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
