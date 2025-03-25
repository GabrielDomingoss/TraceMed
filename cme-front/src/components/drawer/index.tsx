import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/authProvider";
import {  ListItem, ListItemButton, ListItemText } from "@mui/material";
import TraceMedLogo from '../../assets/traceMedLogo.png';
import './styles.scss';

interface PageProps {
    path: string;
    label: string;
}

interface DrawerProps {
    pages: PageProps[];
}

export function Drawer({
    pages
}: DrawerProps) {
    const { logout } = useAuth();
    const navigate = useNavigate();

    return (
        <div className="drawerBox">
          <img src={TraceMedLogo} alt="TraceMed" className="drawerLogo" />
          {pages.map((page: PageProps) => (
            <ListItem key={page.label}>
                <ListItemButton onClick={() => {
                    navigate(page.path);
                }}>
                    <ListItemText primary={page.label} />
                </ListItemButton>
            </ListItem>
          ))}
          <ListItem>
            <ListItemText
              primary={`${sessionStorage.getItem("user_name") || "Usuário"} (${sessionStorage.getItem("role") || "Função"})`}
              primaryTypographyProps={{ fontWeight: 500 }}
            />
          </ListItem>
          <ListItem>
            <ListItemButton onClick={logout}>
                <ListItemText primary="Sair" primaryTypographyProps={{ color: "error" }} />
            </ListItemButton>
          </ListItem>
        </div>
    )
}