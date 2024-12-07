import React, { useState } from 'react';
import './App.css';
import Login from './Login';
import Register from './Register';

function App() {
  const [userToken, setUserToken] = useState(null);

  console.log("User Token:", userToken); // Check the value of userToken on load and during renders

  const [weatherData, setWeatherData] = useState({
    temperature: '',
    humidity: '',
    pressure: ''
  });

  const handleChange = (event) => {
    const newWeatherData = {
      ...weatherData,
      [event.target.name]: event.target.value
    };
    setWeatherData(newWeatherData);
    console.log("Updated Weather Data:", newWeatherData); // Log weather data updates
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Submitting:", weatherData);
  };

  if (!userToken) {
    return (
      <div className="App">
        <header className="App-header">
          <Login setUserToken={setUserToken} />
          <Register setUserToken={setUserToken} />
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Weather Predictor</h1>
        <form onSubmit={handleSubmit}>
          <input type="text" name="temperature" placeholder="Enter temperature (°C)" value={weatherData.temperature} onChange={handleChange} />
          <input type="text" name="humidity" placeholder="Enter humidity (%)" value={weatherData.humidity} onChange={handleChange} />
          <input type="text" name="pressure" placeholder="Enter pressure (hPa)" value={weatherData.pressure} onChange={handleChange} />
          <button type="submit">Predict Temperature</button>
        </form>
        <button onClick={() => setUserToken(null)}>Logout</button>
      </header>
    </div>
  );
}

export default App;
