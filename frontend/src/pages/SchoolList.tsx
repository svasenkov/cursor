import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Alert,
  CardMedia,
  Chip,
} from '@mui/material';
import { schoolsApi } from '../api/client';
import { format } from 'date-fns';

export default function SchoolList() {
  const { data: schools, isLoading, error, isError } = useQuery({
    queryKey: ['schools'],
    queryFn: schoolsApi.getAll,
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (isError) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error instanceof Error ? error.message : 'Error loading schools'}
      </Alert>
    );
  }

  if (!schools?.length) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        No schools found
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Schools
      </Typography>
      
      <Grid container spacing={3}>
        {schools.map((school) => (
          <Grid item xs={12} sm={6} md={4} key={school.id}>
            <Card>
              {school.logo && (
                <CardMedia
                  component="img"
                  height="140"
                  image={school.logo}
                  alt={school.name}
                  sx={{ objectFit: 'contain', p: 2, bgcolor: 'background.paper' }}
                />
              )}
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {school.name}
                </Typography>
                
                <Typography color="textSecondary" gutterBottom>
                  {school.address}
                </Typography>
                
                <Box sx={{ mt: 2 }}>
                  <Chip
                    label={`Founded: ${format(new Date(school.foundation_date), 'MMMM yyyy')}`}
                    variant="outlined"
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
} 