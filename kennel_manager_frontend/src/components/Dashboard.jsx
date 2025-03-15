import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Button, Card, CardContent, Typography, CircularProgress, Container } from "@mui/material";

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await api.get("users/profile/");
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching profile:", error);
        navigate("/login"); // Redirect to login if unauthorized
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("userRole");
    navigate("/login");
  };

  if (loading) return <CircularProgress />; // Show loading spinner

  if (!user) return null; // Prevent rendering if user is undefined

  return (
    <Container maxWidth="md">
      <Card>
        <CardContent>
          <Typography variant="h4">Welcome, {user.username}!</Typography>
          <Typography variant="subtitle1">Role: {user.role}</Typography>
          <Typography variant="subtitle2">Email: {user.email}</Typography>

          {/* Render role-specific components */}
          {user.role === "admin" && <AdminDashboard />}
          {user.role === "staff" && <StaffDashboard />}
          {user.role === "customer" && <CustomerDashboard />}

          <Button variant="contained" color="secondary" onClick={handleLogout} style={{ marginTop: 20 }}>
            Logout
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Dashboard;
