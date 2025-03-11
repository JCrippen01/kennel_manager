import React from "react";
import { Container, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

const columns = [{ field: "id", headerName: "ID", width: 90 }, { field: "message", headerName: "Message", width: 300 }];
const rows = [{ id: 1, message: "Hello, World" }];

const Dashboard = () => {
  return (
    <Container>
      <Typography variant="h4">Dashboard</Typography>
      <DataGrid rows={rows} columns={columns} pageSize={5} />
    </Container>
  );
};

export default Dashboard;
