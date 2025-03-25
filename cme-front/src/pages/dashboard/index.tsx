import { Box, Grid, Typography, Card, CardContent, CardHeader } from "@mui/material";
import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts";
import "./styles.scss";

export const Dashboard = () => {
  const chartOptionsPie = {
    chart: { type: "pie", backgroundColor: "#e6e8e6" },
    title: {
      text: "Materiais por Status",
      style: {
        color: "#30597f",
      }
    },
    colors: ['#345369', '#5e8faa', '#c2ccd5', '#44c6e7'],
    credits: {
      enabled: false
    },
    series: [{
      name: "Materiais",
      shadow: true,
      data: [
        { name: "Recebimento", y: 30, },
        { name: "Lavagem", y: 45 },
        { name: "Esterilização", y: 20 },
        { name: "Distribuição", y: 55 },
      ],
    }],
  };

  const chartOptionsBar = {
    chart: { type: "column", backgroundColor: "#e6e8e6" },
    title: { 
      text: "Falhas por Etapa",
      style: {
        color: "#30597f",
      }
    },
    xAxis: { categories: ["Recebimento", "Lavagem", "Esterilização", "Distribuição"] },
    yAxis: { title: { text: "Falhas Registradas" } },
    colors: ["#185885"],
    credits: {
      enabled: false
    },
    series: [{
      name: "Falhas",
      data: [5, 10, 3, 8],
    }],
  };

  return (
    <Box className="dashboard-container">

      <Grid container spacing={3} justifyContent="center" className="dashboard-grid" marginBottom={3}>
        {/* Cards Resumo */}
        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardHeader 
              className="card-title"
              title="Usuários Cadastrados"
            />
            <CardContent className="card-indicators-content" >
              <Typography className="card-value">50</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardHeader 
              className="card-title"
              title="Materiais Cadastrados"
            />
            <CardContent className="card-indicators-content">
              <Typography className="card-value">120</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardHeader 
              className="card-title"
              title="Processos em Andamento"
            />
            <CardContent className="card-indicators-content">
              <Typography className="card-value">32</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardHeader 
              className="card-title"
              title="Falhas Registradas"
            />
            <CardContent className="card-indicators-content">
              <Typography className="card-value">5</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Gráficos */}
      <Grid container spacing={3} justifyContent="center" className="dashboard-charts">
        <Grid item xs={12} md={6}>
          <Card className="dashboard-card">
            <CardContent>
              <HighchartsReact highcharts={Highcharts} options={chartOptionsPie} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card className="dashboard-card">
            <CardContent>
              <HighchartsReact highcharts={Highcharts} options={chartOptionsBar} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
