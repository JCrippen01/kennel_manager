import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Container, TextField, Button, Card, CardContent, Typography, List, ListItem } from "@mui/material";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
  });
  const [errors, setErrors] = useState({});
  const [password, setPassword] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });

    // Track password separately for validation hints
    if (e.target.name === "password") {
      setPassword(e.target.value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    try {
      await api.post("users/register/", formData);
      navigate("/login");
    } catch (error) {
      if (error.response && error.response.data) {
        setErrors(error.response.data);
      } else {
        setErrors({ general: "Something went wrong. Please try again." });
      }
    }
  };

  return (
    <Container maxWidth="sm">
      <Card>
        <CardContent>
          <Typography variant="h5">Register</Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              label="First Name"
              name="first_name"
              fullWidth
              margin="normal"
              onChange={handleChange}
              error={!!errors.first_name}
              helperText={errors.first_name ? errors.first_name[0] : ""}
            />
            <TextField
              label="Last Name"
              name="last_name"
              fullWidth
              margin="normal"
              onChange={handleChange}
              error={!!errors.last_name}
              helperText={errors.last_name ? errors.last_name[0] : ""}
            />
            <TextField
              label="Username"
              name="username"
              fullWidth
              margin="normal"
              onChange={handleChange}
              error={!!errors.username}
              helperText={errors.username ? errors.username[0] : ""}
            />
            <TextField
              label="Email"
              name="email"
              fullWidth
              margin="normal"
              onChange={handleChange}
              error={!!errors.email}
              helperText={errors.email ? errors.email[0] : ""}
            />
            <TextField
              label="Password"
              name="password"
              type="password"
              fullWidth
              margin="normal"
              onChange={handleChange}
              error={!!errors.password}
              helperText={errors.password ? errors.password[0] : ""}
            />

            {/* ✅ Password Rules Section */}
            <Typography variant="body2" sx={{ mt: 1 }}>
              Password must include:
            </Typography>
            <List dense>
              <ListItem sx={{ color: password.length >= 8 ? "green" : "red" }}>
                - At least 8 characters
              </ListItem>
              <ListItem sx={{ color: /[A-Z]/.test(password) ? "green" : "red" }}>
                - At least one uppercase letter
              </ListItem>
              <ListItem sx={{ color: /[a-z]/.test(password) ? "green" : "red" }}>
                - At least one lowercase letter
              </ListItem>
              <ListItem sx={{ color: /\d/.test(password) ? "green" : "red" }}>
                - At least one number
              </ListItem>
              <ListItem sx={{ color: /[@$!%*?&]/.test(password) ? "green" : "red" }}>
                - At least one special character (@$!%*?&)
              </ListItem>
            </List>

            {errors.general && (
              <Typography color="error" sx={{ mt: 2 }}>
                {errors.general}
              </Typography>
            )}
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Register
            </Button>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Register;
