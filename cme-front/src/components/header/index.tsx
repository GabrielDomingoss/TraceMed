import { Grid, IconButton, Toolbar } from "@mui/material";
// import AzapeLogo from '../../assets/logo.png';
import AppBar from "./appBar";
import { UserMenu } from "./userMenu";
import './styles.scss';
import { NotificationMenu } from "./notificationsMenu";

interface HeaderProps {
    open: boolean,
    handleDrawerOpen: () => void
    drawerWidth?: number
}
export function Header({
    open,
    handleDrawerOpen,
    drawerWidth = 240,
    ...props
}: HeaderProps) {
    return (
        <AppBar position="fixed" drawerWidth={drawerWidth} open={open} {...props}>
            <Toolbar>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    onClick={handleDrawerOpen}
                    edge="start"
                    sx={{ mr: 2, ...(open && { display: 'none' }) }}
                >
                    Logo
                    {/* <img src={AzapeLogo} className="appBarLogo" alt="" /> */}
                </IconButton>

                <Grid container display="flex" justifyContent={'end'}>
                    <Grid item marginTop={'auto'} marginBottom={'auto'} display={"inline-flex"} color={"#59666F"}>
                        <NotificationMenu></NotificationMenu>
                        <UserMenu></UserMenu>
                    </Grid>
                </Grid>
            </Toolbar>
        </AppBar>
    )
}