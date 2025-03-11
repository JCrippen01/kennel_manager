import React from "react";
import { useNavigate } from "react-router-dom";
import { Container, Button } from "@mui/material";

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <h1>Welcome to Kennel Manager</h1>
      <Button variant="contained" color="primary" onClick={() => navigate("/register")}>Register</Button>
      <Button variant="contained" color="secondary" onClick={() => navigate("/login")} style={{ marginLeft: "10px" }}>Login</Button>
    </Container>
  );
};

export default Home;
