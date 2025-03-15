import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Container, TextField, Button, Card, CardContent, Typography, Alert } from "@mui/material";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    try {
      const response = await api.post("users/login/", formData);
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      localStorage.setItem("userRole", response.data.role);

      navigate("/dashboard");
    } catch (err) {
      if (err.response) {
        setError(err.response.data.message || "Login failed. Please try again.");
      } else {
        setError("Unable to connect to the server.");
      }
    }
  };

  return (
    <Container maxWidth="sm">
      <Card>
        <CardContent>
          <Typography variant="h5">Login</Typography>
          <Typography variant="body2" color="textSecondary">
            Enter your username and password to log in.
          </Typography>

          {error && <Alert severity="error">{error}</Alert>}

          <form onSubmit={handleSubmit}>
            <TextField 
              label="Username" 
              name="username" 
              fullWidth 
              margin="normal" 
              onChange={handleChange} 
              required
            />
            <TextField 
              label="Password" 
              name="password" 
              type="password" 
              fullWidth 
              margin="normal" 
              onChange={handleChange} 
              required
            />

            <Button type="submit" variant="contained" color="primary" fullWidth>
              Login
            </Button>
          </form>

          <Typography variant="body2" color="textSecondary" style={{ marginTop: 10 }}>
            Forgot password? <a href="/reset-password">Reset it here</a>.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Login;
