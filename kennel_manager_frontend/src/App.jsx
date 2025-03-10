import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

const App = () => {
    const [authTokens, setAuthTokens] = useState(null);

    return (
        <Router>
            <Routes>
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login setAuthTokens={setAuthTokens} />} />
                <Route path="/dashboard" element={<Dashboard authTokens={authTokens} />} />
            </Routes>
        </Router>
    );
};

export default App;
