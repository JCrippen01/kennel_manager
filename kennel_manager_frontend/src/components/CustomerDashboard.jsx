import { Card, CardContent, Typography, Button } from "@mui/material";

const CustomerDashboard = () => {
  return (
    <Card style={{ marginTop: 20 }}>
      <CardContent>
        <Typography variant="h5">Customer Dashboard</Typography>
        <Typography variant="body1">Book kennel space and manage reservations.</Typography>
        <Button variant="contained" color="primary" style={{ marginTop: 10 }}>
          Book Now
        </Button>
        <Button variant="contained" color="secondary" style={{ marginLeft: 10, marginTop: 10 }}>
          View Reservations
        </Button>
      </CardContent>
    </Card>
  );
};

export default CustomerDashboard;
