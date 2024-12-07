import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Make sure this is correct

function Login({ setUserToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Use navigate instead of history

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const { data } = await axios.post('/login', { username, password });
      setUserToken(data.token);
      navigate('/'); // Navigate to home or dashboard after login
    } catch (error) {
      alert('Login failed: ' + error.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
