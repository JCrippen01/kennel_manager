import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { Button, Container, Typography } from "@mui/material";

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate(); // Get navigate from Router context

  return (
    <Container>
      <Typography variant="h4">Welcome, {user}!</Typography>
      <Button 
        variant="contained" 
        color="secondary" 
        onClick={() => logout(navigate)}  // Pass navigate to logout
        style={{ marginTop: "20px" }}
      >
        Logout
      </Button>
    </Container>
  );
};

export default Dashboard;
