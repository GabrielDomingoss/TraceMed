import { useEffect, useState } from "react";
import { useAuth } from "../hooks/authProvider";
import { Drawer } from "../components/drawer";
import { Container, Grid } from "@mui/material";
import { Outlet } from "react-router-dom";
import { Footer } from "../components/footer";
import './styles.scss'
export function DefaultLayout() {
    const [open, setOpen] = useState(() => window.innerWidth > 768);
    // const { isAuthenticated } = useAuth();

    const handleDrawerOpen = () => {
        setOpen(!open);
    };

    useEffect(() => {
        const handleResize = () => {
            setOpen(window.innerWidth > 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return (
        <div className="layoutBox">
            <Drawer
                open={open} 
                handleDrawerOpen={handleDrawerOpen}
                drawerWidth={240}
            />
            <main className={`main ${open ? "open" : "closed"}`}>
                <div className="layoutDrawerHeader"/>
                <Container>
                    <Grid marginTop={1}>
                        <Outlet />
                    </Grid>
                </Container>

            </main>

            <div className={`footerContainer ${open ? "open" : "closed"}`}>
                {/* {isAuthenticated && <Footer />} */}
            </div>
        </div>
    );
}
