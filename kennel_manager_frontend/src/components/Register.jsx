import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, TextField, Button, Card, CardContent, Typography } from "@mui/material";
import api from "../services/api.js";

const Register = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await api.post("/register/", formData);
      alert("Registration successful!");
      navigate("/login");
    } catch (error) {
      alert("Registration failed");
    }
  };

  return (
    <Container>
      <Card>
        <CardContent>
          <Typography variant="h5">Register</Typography>
          <TextField label="Username" name="username" fullWidth margin="normal" onChange={handleChange} />
          <TextField label="Password" type="password" name="password" fullWidth margin="normal" onChange={handleChange} />
          <Button variant="contained" color="primary" onClick={handleSubmit}>Submit</Button>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Register;
