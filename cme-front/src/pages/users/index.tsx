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
  Grid,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import "./styles.scss";
import { User } from "../../models/user";
import api from "../../services/api";

export const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [open, setOpen] = useState(false);
  const [reload, setReload] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "",
  });

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setReload(true);
    setFormData({ name: "", email: "", password: "", role: "" });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<string>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async(e: { preventDefault: () => void; }) => {
    e.preventDefault()
    try {
      await api.post('/users', formData);
      alert('Usuário cadastrado com sucesso');
      handleClose();
    }
    catch {
      alert('Erro ao cadastrar usuário')
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
        api.defaults.headers.common["Authorization"] = `Bearer ${sessionStorage.getItem("token")}`;
        const response = await api.get('/users');
        const usuarios = response.data;
        setUsers(usuarios);
      }
      catch (error) {
        console.log('erro no get de usuários')
      }
    }

    if(users.length===0 || reload){
      getUsers();
      setReload(false);
    }
  }, [reload, users.length])

  return (
    <Box className="users-container">
      <Typography variant="h4" className="users-title">Usuários</Typography>
      <div className="add-container">
        <Button variant="contained" onClick={handleOpen} className="add-user-button">
          Adicionar Usuário
        </Button>
      </div>

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

      <Dialog open={open} onClose={handleClose} maxWidth="lg" className="create-dialog">
        <DialogTitle>Adicionar Usuário</DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={7}>
                <TextField
                  fullWidth
                  size="small"
                  label="Nome"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs>
                <TextField
                  fullWidth
                  size="small"
                  label="E-mail"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  margin="normal"
                />
              </Grid>
            </Grid>
          
            <Grid container spacing={2}>
              <Grid item xs>
                <TextField
                  fullWidth
                  size="small"
                  label="Senha"
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs>
                <FormControl 
                  fullWidth 
                  margin="normal"
                  required
                  size="small"
                >
                  <InputLabel>Função</InputLabel>
                  <Select name="role" value={formData.role} onChange={handleChange}label="Função">
                    <MenuItem value="Admin">Administrador</MenuItem>
                    <MenuItem value="Técnico">Técnico</MenuItem>
                    <MenuItem value="Enfermeiro">Enfermeiro</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} className="cancel-button" variant="contained">Cancelar</Button>
            <Button onClick={handleSubmit} className="confirm-button" variant="contained" type="submit">Salvar</Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};
