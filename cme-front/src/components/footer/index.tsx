import { Grid } from '@mui/material';
import { useAuth } from '../../hooks/authProvider';
// import AzapeLogoFooter from '../../assets/logoFooter.png';
import './styles.scss';

export function Footer() {
    // const {isAuthenticated} = useAuth();
    
    // if(isAuthenticated) {
    //     return (
    //         <footer className='homeFooter'>
    //             <Grid container display={"flex"} justifyContent={"space-between"}>
    //                 <Grid item xs>
    //                     <Grid container spacing={3}>
    //                         <Grid item className='textMiddle'>
    //                             <a href="https://azape.co/polices">Termos de Uso</a>
    //                         </Grid>
    //                         <Grid item className='textMiddle'>
    //                             <a href="https://azape.co/polices">Política de Privacidade</a>
    //                         </Grid>
    //                     </Grid>
    //                 </Grid>
    //                 <Grid item xs>
    //                     <Grid container spacing={3} display={'flex'} justifyContent={"end"}>
    //                         <Grid item>
    //                             Logo
    //                         </Grid>
    //                         <Grid item className='textMiddle'>
    //                             © Desenvolvido por Azape
    //                         </Grid>
    //                     </Grid>
    //                 </Grid>
    //             </Grid>
    //         </footer>
    //     )
    // }
    // else {
        return (
            <footer className='loginFooter'>
                © Desenvolvido por Azape
            </footer>
        )
    // }
}