import { Button, Card, CardContent, Typography } from "@mui/material";

const AdminDashboard = () => {
  return (
    <Card style={{ marginTop: 20 }}>
      <CardContent>
        <Typography variant="h5">Admin Panel</Typography>
        <Typography variant="body1">Manage users, settings, and analytics.</Typography>
        <Button variant="contained" color="primary" style={{ marginTop: 10 }}>
          Manage Users
        </Button>
        <Button variant="contained" color="secondary" style={{ marginLeft: 10, marginTop: 10 }}>
          View Reports
        </Button>
      </CardContent>
    </Card>
  );
};

export default AdminDashboard;
