import { 
    AppBar,
    Box,
    Button,
    Drawer,
    Grid,
    IconButton,
    Toolbar,
    useMediaQuery,
    useTheme
} from "@mui/material";
import Logo from '../../assets/traceMedLogo.png';
import './styles.scss';
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Menu } from "@mui/icons-material";
import { useAuth } from "../../hooks/authProvider";
import { Drawer as CustomDrawer } from "../drawer";

export function Header() {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
    const navigate = useNavigate();
    const [mobileOpen, setMobileOpen] = useState(false);
    const { logout } = useAuth();

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const pages = [
        { label: "Usuários", path: "/users" },
        { label: "Materiais", path: "/materials" },
        { label: "Rastreabilidade", path: "/traceability" },
    ];

    return (
        <div>
            <AppBar position="static" className="appBar">
                <Toolbar >
                    {isMobile && (
                        <Grid className="mobileGrid">
                            <IconButton
                                color="inherit"
                                aria-label="open drawer"
                                edge="start"
                                onClick={handleDrawerToggle}
                                className="menuButton"
                            >
                                <Menu />
                            </IconButton>
                            <div className="logoMobile" onClick={() => {
                                navigate('/dashboard')
                            }}>
                                <img src={Logo} alt="TraceMed" />
                            </div>
                        </Grid>
                    )}

                    {!isMobile && (
                        <Grid className="webMainGrid">
                            <Grid className="webSecondaryGrid">
                                {pages.slice(0,2).map((page) => (
                                    <Button
                                        key={page.label}
                                        color="inherit"
                                        onClick={() => navigate(page.path)}
                                        className="pageItem"
                                    >
                                        {page.label}
                                    </Button>
                                ))}

                                <Box onClick={() => {
                                    navigate('/dashboard')
                                }}>
                                    <img src={Logo} alt="TraceMed" className="webLogo"/>
                                </Box>

                                {pages.slice(2,4).map((page) => (
                                    <Button
                                        key={page.label}
                                        color="inherit"
                                        onClick={() => navigate(page.path)}
                                        className="pageItem"
                                    >
                                        {page.label}
                                    </Button>
                                ))}
                            </Grid>
                            
                            <Button className="logoutButton" onClick={logout}>
                                Sair
                            </Button>
                        </Grid>
                        
                    )}
                </Toolbar>
            </AppBar>
            <Box component="nav">
                <Drawer
                    variant="temporary"
                    open={mobileOpen}
                    onClose={handleDrawerToggle}
                    ModalProps={{ keepMounted: true }}
                    sx={{
                        display: { xs: "block", sm: "none" },
                    }}
                >
                    <CustomDrawer pages={pages}/>
                </Drawer>
            </Box>
        </div>
    )
}