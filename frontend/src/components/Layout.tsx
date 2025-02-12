import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Courses Catalog
          </Typography>
          <Button color="inherit" component={RouterLink} to="/">
            Courses
          </Button>
          <Button color="inherit" component={RouterLink} to="/schools">
            Schools
          </Button>
          <Button color="inherit" component={RouterLink} to="/platforms">
            Platforms
          </Button>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flexGrow: 1, py: 3 }}>
        {children}
      </Container>
    </Box>
  );
} 