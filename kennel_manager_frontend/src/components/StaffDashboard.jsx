import { Card, CardContent, Typography, Button } from "@mui/material";

const StaffDashboard = () => {
  return (
    <Card style={{ marginTop: 20 }}>
      <CardContent>
        <Typography variant="h5">Staff Dashboard</Typography>
        <Typography variant="body1">View and manage customer reservations.</Typography>
        <Button variant="contained" color="primary" style={{ marginTop: 10 }}>
          View Reservations
        </Button>
        <Button variant="contained" color="secondary" style={{ marginLeft: 10, marginTop: 10 }}>
          Update Availability
        </Button>
      </CardContent>
    </Card>
  );
};

export default StaffDashboard;
