/* eslint-disable @typescript-eslint/no-unused-vars */
import { 
    Box,
    Button,
    Card,
    CardContent,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    SelectChangeEvent,
    TextField,
    Typography 
} from "@mui/material";
import { useEffect, useState } from "react";
import api from "../../services/api";
import { DataGrid } from "@mui/x-data-grid";
import './styles.scss'
import { Material } from "../../models/material";

export function Materials() {
    const [materials, setMaterials] = useState<Material[]>([]);
    const [open, setOpen] = useState(false);
    const [reload, setReload] = useState(false);
    const [formData, setFormData] = useState<Material>({
        name: "",
        type: "",
        vadility: "",
    });
    const handleOpen = () => setOpen(true);
    const handleClose = () => {
      setOpen(false);
      setReload(true);
      setFormData({ name: "", type: "", vadility: "" });
    };

    const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<string>
    ) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async(e: { preventDefault: () => void; }) => {
        e.preventDefault()
        try {
            const postData =  {
                nome: formData.name,
                tipo: formData.type,
                data_validade: formData.vadility,
            }
            await api.post('/materials', postData);
            alert('Material cadastrado com sucesso');
            handleClose();
        }
        catch {
          alert('Erro ao cadastrar Material')
        }
    };

    const columns = [
        { field: "id", headerName: "ID", width: 70 },
        { field: "nome", headerName: "Nome", width: 200 },
        { field: "tipo", headerName: "Tipo", width: 250 },
        { field: "data_validade", headerName: "Data de Validade", width: 150 },
    ];

    useEffect(() => {
        const getMaterials = async () => {
          try {
            const response = await api.get('/materials');
            const materiais = response.data;
            setMaterials(materiais);
          }
          catch (error: unknown) {
            console.log('erro no get de materiais')
          }
        }
    
        if(materials.length===0 || reload){
          getMaterials();
          setReload(false);
        }
    }, [reload, materials.length])

    return (
        <Box className="materials-container">
           <Typography variant="h4" className="materials-title">Materiais</Typography>
            <div className="add-container">
                <Button variant="contained" onClick={handleOpen} className="add-user-button">
                    Adicionar Material
                </Button>
            </div>

            <Card className="materials-card">
                <CardContent>
                <DataGrid
                    rows={materials}
                    columns={columns}
                    autoHeight
                    pageSizeOptions={[5, 10, 20]}
                    pagination
                />
                </CardContent>
            </Card>

            <Dialog open={open} onClose={handleClose} maxWidth="lg" className="create-dialog">
                <DialogTitle>Adicionar Material</DialogTitle>
                <form onSubmit={handleSubmit}>
                <DialogContent>
                    <Grid container spacing={2}>
                    <Grid item xs>
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
                        label="Tipo"
                        name="type"
                        required
                        value={formData.type}
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
                            label="Data de Validade"
                            name="vadility"
                            required
                            value={formData.vadility}
                            onChange={handleChange}
                            margin="normal"
                            />
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
    )
}