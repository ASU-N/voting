import './App.css';
import React, { useEffect, useState } from 'react';  // Import React and hooks
import { RouterProvider, createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import axios from 'axios'; // Import axios

// Import your pages and layouts
import Kyc from './pages/kyc';
import HomeLayout from './layout/HomeLayout';
import Result from './pages/result';
import NotFoundPage from './pages/notfoundpage';
import Login from './pages/login';
import Guidelines from './pages/guidelines';
import Home from './pages/home';

// Create your router
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route index element={<Login />} />
      <Route path="/home" element={<HomeLayout />}>
        <Route index element={<Home />} />
        <Route path="kyc" element={<Kyc />} />
        <Route path="result" element={<Result />} />
        <Route path="guidelines" element={<Guidelines />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Route>
  )
);

const App = () => {
  const [elections, setElections] = useState([]); // Declare state for elections

  useEffect(() => {
    axios.get('http://localhost:8000/api/elections/')
      .then(response => {
        setElections(response.data.elections);  // Save elections data to state
      })
      .catch(error => {
        console.error('Error fetching elections:', error);
      });
  }, []);  // Empty dependency array ensures this runs only once when the component mounts

  return (
    <main>
      <RouterProvider router={router} />
      {/* Render elections data here if needed */}
      <div className="App">
        
        <ul>
          {elections.map((election) => (
            <li key={election.id}>{election.name}</li> // Render each election
          ))}
        </ul>
      </div>
    </main>
  );
};

export default App;
