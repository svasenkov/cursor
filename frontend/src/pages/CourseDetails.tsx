import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { coursesApi } from '../api/client';

export default function CourseDetails() {
  const { id } = useParams<{ id: string }>();
  const courseId = parseInt(id || '0');

  const { data: course, isLoading, error, isError } = useQuery({
    queryKey: ['course', courseId],
    queryFn: () => coursesApi.getById(courseId),
    enabled: !!courseId,
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
        {error instanceof Error ? error.message : 'Error loading course details'}
      </Alert>
    );
  }

  if (!course) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        Course not found
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            {course.title}
          </Typography>
          
          <Typography color="textSecondary" gutterBottom>
            Instructor: {course.instructor}
          </Typography>

          <Typography variant="body1" paragraph>
            {course.description}
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1">Duration:</Typography>
              <Typography color="textSecondary">{course.duration}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1">Price:</Typography>
              <Typography color="textSecondary">${course.price}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1">Level:</Typography>
              <Typography color="textSecondary">{course.engineer_level}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1">Students:</Typography>
              <Typography color="textSecondary">{course.students_amount}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="subtitle1">Rating:</Typography>
              <Typography color="textSecondary">{course.rating}/5</Typography>
            </Grid>
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Categories:
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {course.categories.map((category) => (
                <Chip key={category} label={category} variant="outlined" />
              ))}
            </Box>
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              School:
            </Typography>
            <Typography color="textSecondary">
              {course.school.name}
            </Typography>
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Platform:
            </Typography>
            <Typography color="textSecondary">
              {course.platform.name}
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
} 