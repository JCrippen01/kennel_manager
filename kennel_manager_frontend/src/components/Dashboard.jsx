import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid';
import { Container, Button } from '@mui/material';

const Dashboard = ({ authTokens }) => {
    const [users, setUsers] = useState([]);
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/users/', {
                    headers: { Authorization: `Bearer ${authTokens.access}` },
                });
                setUsers(response.data);
                const userRole = response.data.find(user => user.username === authTokens.username)?.is_staff;
                setIsAdmin(userRole);
            } catch (error) {
                console.error('Failed to fetch users:', error);
            }
        };

        fetchUsers();
    }, [authTokens]);

    const columns = [
        { field: 'id', headerName: 'ID', width: 90 },
        { field: 'username', headerName: 'Username', width: 150 },
        { field: 'email', headerName: 'Email', width: 200 },
        { field: 'is_staff', headerName: 'Admin', width: 150 },
    ];

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:8000/api/users/${id}/`, {
                headers: { Authorization: `Bearer ${authTokens.access}` },
            });
            setUsers(users.filter(user => user.id !== id));
        } catch (error) {
            console.error('Failed to delete user:', error);
        }
    };

    return (
        <Container>
            <div style={{ height: 400, width: '100%' }}>
                <DataGrid rows={users} columns={columns} pageSize={5} rowsPerPageOptions={[5]} disableSelectionOnClick />
            </div>
            {isAdmin && (
                <div>
                    <Button variant="contained" color="primary">Add User</Button>
                    <Button variant="contained" color="secondary" onClick={() => handleDelete(selectedUser.id)}>Delete User</Button>
                </div>
            )}
        </Container>
    );
};

export default Dashboard;
