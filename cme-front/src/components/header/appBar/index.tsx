import React, { ReactNode } from "react";
import MuiAppBar from "@mui/material/AppBar";
import "./styles.scss";

interface AppBarProps {
  open: boolean;
  drawerWidth: number;
  children: ReactNode;
  position: string;
}

const AppBar: React.FC<AppBarProps> = ({ open, ...props}) => {
  return (
    <MuiAppBar
      className={`app-bar ${open ? "open" : ""}`}
    >
        {props.children}
    </MuiAppBar>
  );
};

export default AppBar;
