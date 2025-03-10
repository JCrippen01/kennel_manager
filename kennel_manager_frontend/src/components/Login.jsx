import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Login = ({ setAuthTokens }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/token/', { username, password });
            setAuthTokens(response.data);
            navigate('/dashboard');
        } catch (error) {
            setMessage('Login failed.');
        }
    };

    return (
        <Container>
            <Typography variant="h4">Login</Typography>
            <form onSubmit={handleLogin}>
                <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth margin="normal" />
                <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth margin="normal" />
                <Button type="submit" variant="contained" color="primary">Login</Button>
            </form>
            {message && <Typography>{message}</Typography>}
        </Container>
    );
};

export default Login;
