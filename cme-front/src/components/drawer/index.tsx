import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/authProvider";
import { Header } from "../header";
import { List, ListItem, ListItemButton, ListItemText, Drawer as MaterialDrawer } from "@mui/material";
import TraceMedLogo from '../../assets/traceMedLogo.png';
import './styles.scss';
// import ChartIcon from '../../assets/chartIcon.png';

interface DrawerProps {
    open: boolean;
    drawerWidth: number;
    handleDrawerOpen: () => void
}

export function Drawer({
    open,
    drawerWidth,
    handleDrawerOpen,
}: DrawerProps) {
    // const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    // useEffect(() => {
    //     if(!isAuthenticated) {
    //       navigate('/login');
    //     }
    // },[isAuthenticated, navigate])
    
    return (
        <div>
            <Header
                open={open}
                handleDrawerOpen={handleDrawerOpen}
                drawerWidth={drawerWidth}    
            />

            <MaterialDrawer 
                className="customDrawer" 
                variant="permanent" 
                anchor="left" 
                open={true}
                sx={{
                    width: open ? drawerWidth : 0,
                    flexShrink: 0,
                    transition: "width 0.3s ease-in-out",
                    "& .MuiDrawer-paper": {
                        width: open ? drawerWidth : 0,
                        transition: "width 0.3s ease-in-out",
                    },
                }}
            >
                <div className="drawerHeader">
                    <img src={TraceMedLogo} className="appBarLogo" alt="" />
                </div>
                <List>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <div className="listItemButton">
                                {/* <ListItemIcon className="chartIcon">
                                    chartIcon
                                    <img src={ChartIcon} className="chartIcon" alt="" />
                                </ListItemIcon> */}
                                <ListItemText primary="Dashboard"></ListItemText>
                            </div>
                        </ListItemButton>
                    </ListItem>
                </List>
            </MaterialDrawer>
        </div>
    )
}