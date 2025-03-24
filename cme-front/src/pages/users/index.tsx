/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  SelectChangeEvent,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import "./styles.scss";
import { User } from "../../models/user";
import api from "../../services/api";

export const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "",
  });

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setFormData({ name: "", email: "", password: "", role: "" });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<string>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    if (formData.name && formData.email && formData.password && formData.role) {
      setUsers([...users, { id: users.length + 1, ...formData }]);
      handleClose();
    }
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Nome", width: 200 },
    { field: "email", headerName: "E-mail", width: 250 },
    { field: "role", headerName: "Função", width: 150 },
  ];

  useEffect(() => {
    const getUsers = async () => {
      try {
        const response = await api.get('/users');
        const usuarios = response.data;
        setUsers(usuarios);
      }
      catch (error) {
        console.log('erro no get de usuários')
      }
    }

    if(users.length===0){
      getUsers();
    }
  })

  return (
    <Box className="users-container">
      <Typography variant="h4" className="users-title">Gerenciamento de Usuários</Typography>
      <Button variant="contained" color="primary" onClick={handleOpen} className="add-user-button">
        Adicionar Usuário
      </Button>

      <Card className="users-card">
        <CardContent>
        <DataGrid
            rows={users}
            columns={columns}
            autoHeight
            pageSizeOptions={[5, 10, 20]}
            pagination
        />
        </CardContent>
      </Card>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Adicionar Usuário</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Nome"
            name="name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            label="E-mail"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Senha"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Função</InputLabel>
            <Select name="role" value={formData.role} onChange={handleChange}>
              <MenuItem value="Admin">Administrador</MenuItem>
              <MenuItem value="Técnico">Técnico</MenuItem>
              <MenuItem value="Enfermeiro">Enfermeiro</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="secondary">Cancelar</Button>
          <Button onClick={handleSubmit} color="primary" variant="contained">Salvar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
