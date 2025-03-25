import { useEffect, useState } from "react";
import { Container, Grid } from "@mui/material";
import { Outlet, useNavigate } from "react-router-dom";
import './styles.scss'
import { Header } from "../components/header";
import { useAuth } from "../hooks/authProvider";
export function DefaultLayout() {
    const [open, setOpen] = useState(() => window.innerWidth > 768);
    const { isAuthenticated, loading } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const handleResize = () => {
            setOpen(window.innerWidth > 768);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    
    useEffect(() => {
        if (!loading && !isAuthenticated) {
          navigate('/login');
        }
      }, [isAuthenticated, loading, navigate]);
      
    return (
        <div className="layoutBox">
            <Header />
            <main className={`main ${open ? "open" : "closed"}`}>
                <Container>
                    <Grid marginTop={1}>
                        <Outlet />
                    </Grid>
                </Container>
            </main>
        </div>
    );
}
