import React, { useEffect, useState } from 'react';
import api from '../api';
import { List, ListItem, ListItemText } from '@mui/material';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await api.get('/users/');
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <List>
      {users.map((user) => (
        <ListItem key={user.id}>
          <ListItemText primary={user.username} />
        </ListItem>
      ))}
    </List>
  );
}

export default UserList;
