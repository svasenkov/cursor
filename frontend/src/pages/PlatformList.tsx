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
  Link,
} from '@mui/material';
import { platformsApi } from '../api/client';
import { Language } from '@mui/icons-material';

export default function PlatformList() {
  const { data: platforms, isLoading, error, isError } = useQuery({
    queryKey: ['platforms'],
    queryFn: platformsApi.getAll,
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
        {error instanceof Error ? error.message : 'Error loading platforms'}
      </Alert>
    );
  }

  if (!platforms?.length) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        No platforms found
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Platforms
      </Typography>
      
      <Grid container spacing={3}>
        {platforms.map((platform) => (
          <Grid item xs={12} sm={6} md={4} key={platform.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              {platform.logo && (
                <CardMedia
                  component="img"
                  height="140"
                  image={platform.logo}
                  alt={platform.name}
                  sx={{ objectFit: 'contain', p: 2, bgcolor: 'background.paper' }}
                />
              )}
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" gutterBottom>
                  {platform.name}
                </Typography>
                
                {platform.description && (
                  <Typography color="textSecondary" paragraph>
                    {platform.description}
                  </Typography>
                )}
                
                {platform.url && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Language sx={{ mr: 1, color: 'text.secondary' }} />
                    <Link href={platform.url} target="_blank" rel="noopener noreferrer">
                      Visit Platform
                    </Link>
                  </Box>
                )}

                {platform.features && platform.features.length > 0 && (
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {platform.features.map((feature, index) => (
                      <Chip
                        key={index}
                        label={feature}
                        size="small"
                        variant="outlined"
                        sx={{ mb: 1 }}
                      />
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
} 