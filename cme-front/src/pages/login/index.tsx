import { useState } from "react";
import { TextField, Box, Typography, useTheme, useMediaQuery } from "@mui/material";
import { motion } from "framer-motion";
import logo from "../../assets/logo.png";
import './styles.scss';

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const handleLogin = () => {
    if (!email || !password) {
      setError("Preencha todos os campos");
      return;
    }
    console.log("Logando com", email, password);
  };

  return (
    <div className="login-container">
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className={isMobile ? "login-motion-div-fullwidth" : "login-motion-div-auto"}
        >
            <Box className={`login-card ${isMobile ? "login-card-fullwidth" : "login-card-limited"}`}>
                <img 
                    src={logo} 
                    alt="Logo CME"
                    className="login-logo"
                />
                <Typography 
                    variant="h5"
                    mb={2}
                    component={motion.div}
                    initial={{ y: -10, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="login-title"
                >
                    Login
                </Typography>
                <motion.div 
                    initial={{ y: -20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                >
                    <TextField
                        label="E-mail"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </motion.div>
                <motion.div
                    initial={{ y: -20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                >
                    <TextField
                        label="Senha"
                        type="password"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </motion.div>
                {error && (
                    <Typography 
                        color="error"
                        variant="body2"
                        mt={1}
                        component={motion.div}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.5 }}
                    >
                        {error}
                    </Typography>
                )}
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6 }}>
                    <motion.button
                        className="login-button"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleLogin}
                    >
                        Entrar
                    </motion.button>
                </motion.div>
            </Box>
        </motion.div>
    </div>
  );
};
