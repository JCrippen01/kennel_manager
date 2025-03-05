import React from 'react';
import { Container, Typography, Button } from '@mui/material';
import UserList from './components/UserList';

function App() {
  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Kennel Manager Frontend
      </Typography>
      <Button variant="contained" color="primary">
        Get Started
      </Button>
      <UserList />
    </Container>
  );
}

export default App;
