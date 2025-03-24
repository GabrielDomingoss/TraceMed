import { Avatar, Button, Grid, ListItemIcon, Menu, MenuItem } from '@mui/material';
import { Logout, Person } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { useAuth } from '../../../hooks/authProvider';
import './styles.scss';

export function UserMenu() {
  const [username, setUsername] = useState('');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  // const { logout } = useAuth();

  useEffect(() => {
    const username = localStorage.getItem('username');
    if (username) {
      setUsername(username);
    }
  }, [])

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  }

  const handleClose = () => {
    setAnchorEl(null);
  }

  // const handleLogout = () => {
  //   logout();
  //   handleClose();
  // }

  return (
    <div className='menu'>
      <Grid container className='welcome'>
        <Grid item xs={12}>
          Olá,
        </Grid>
        <Grid item xs={12} className='username'>
          {username}
        </Grid>
      </Grid>
      <Button
        size="small"
        variant="text"
        className="menuAvatarButton"
        aria-label="account of current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleMenu}
        color="secondary"
      >
        <Avatar className='customAvatar'>
          <Person />
        </Avatar>
      </Button>
      <Menu
        id="menu-appbar"
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {/* <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem> */}
      </Menu>
    </div>
  )
}
