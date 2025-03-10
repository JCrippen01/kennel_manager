import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography } from '@mui/material';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/api/register/', { username, email, password });
            setMessage('Registration successful.');
        } catch (error) {
            setMessage('Registration failed.');
        }
    };

    return (
        <Container>
            <Typography variant="h4">Register</Typography>
            <form onSubmit={handleRegister}>
                <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth margin="normal" />
                <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} fullWidth margin="normal" />
                <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth margin="normal" />
                <Button type="submit" variant="contained" color="primary">Register</Button>
            </form>
            {message && <Typography>{message}</Typography>}
        </Container>
    );
};

export default Register;
