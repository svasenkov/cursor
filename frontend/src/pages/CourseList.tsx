import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Pagination,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { coursesApi } from '../api/client';
import { CourseCardSkeleton } from '../components/CourseCardSkeleton';

const ITEMS_PER_PAGE = 10;

// Simple debounce utility
function useDebounce<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
) {
  const timeoutRef = useCallback<any>(() => {}, []);

  return useCallback(
    (...args: Parameters<T>) => {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => callback(...args), delay);
    },
    [callback, delay, timeoutRef]
  );
}

export default function CourseList() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState('');

  const handleSearch = useCallback((value: string) => {
    setSearch(value);
    setPage(1); // Reset to first page when search changes
  }, []);

  const debouncedSearch = useDebounce(handleSearch, 300);

  const { data, isLoading, error, isError } = useQuery({
    queryKey: ['courses', page, search, level],
    queryFn: async () => {
      const result = await coursesApi.getAll({
        skip: (page - 1) * ITEMS_PER_PAGE,
        limit: ITEMS_PER_PAGE,
        engineer_level: level || undefined,
        search_term: search || undefined,
      });
      return result;
    },
    keepPreviousData: true,
  });

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Courses
        </Typography>
        <Grid container spacing={3}>
          {[...Array(6)].map((_, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <CourseCardSkeleton />
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  if (isError) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error instanceof Error ? error.message : 'Error loading courses'}
      </Alert>
    );
  }

  const courses = data?.items || [];
  const totalCourses = data?.total || 0;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Courses {totalCourses > 0 && `(${totalCourses})`}
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Search courses"
            onChange={(e) => debouncedSearch(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Engineer Level</InputLabel>
            <Select value={level} onChange={(e) => setLevel(e.target.value as string)}>
              <MenuItem value="">All Levels</MenuItem>
              <MenuItem value="junior">Junior</MenuItem>
              <MenuItem value="middle">Middle</MenuItem>
              <MenuItem value="senior">Senior</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {courses.length > 0 ? (
        <>
          <Grid container spacing={3}>
            {courses.map((course) => (
              <Grid item xs={12} sm={6} md={4} key={course.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {course.title}
                    </Typography>
                    <Typography color="textSecondary" gutterBottom>
                      {course.instructor}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 2 }}>
                      {course.description.substring(0, 150)}...
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h6" color="primary">
                        ${course.price}
                      </Typography>
                      <Button
                        component={RouterLink}
                        to={`/courses/${course.id}`}
                        variant="contained"
                        color="primary"
                        size="small"
                      >
                        View Details
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {totalCourses > ITEMS_PER_PAGE && (
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
              <Pagination
                count={Math.ceil(totalCourses / ITEMS_PER_PAGE)}
                page={page}
                onChange={(_, value) => setPage(value)}
                color="primary"
              />
            </Box>
          )}
        </>
      ) : (
        <Alert severity="info">
          No courses found. {search || level ? 'Try adjusting your filters.' : ''}
        </Alert>
      )}
    </Box>
  );
} 