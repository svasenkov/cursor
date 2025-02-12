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
import { CourseCard } from '../components/course/CourseCard';
import { Search, FilterList } from '@mui/icons-material';
import { CourseFilters } from '../components/course/CourseFilters';
import '../styles/CourseList.css';

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
      try {
        const result = await coursesApi.getAll({
          skip: (page - 1) * ITEMS_PER_PAGE,
          limit: ITEMS_PER_PAGE,
          engineer_level: level || undefined,
          search_term: search || undefined,
        });
        return result;
      } catch (error) {
        console.error('Error fetching courses:', error);
        throw error;
      }
    },
    keepPreviousData: true,
    retry: 1, // Only retry once
  });

  if (isLoading || !data) {
    return (
      <Box className="course-list-container">
        <Typography variant="h4" gutterBottom>
          Loading Courses...
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
      <Box className="course-list-container">
        <Alert 
          severity="error" 
          sx={{ mt: 2 }}
          action={
            <Button color="inherit" size="small" onClick={() => window.location.reload()}>
              Retry
            </Button>
          }
        >
          {error instanceof Error ? error.message : 'Error loading courses'}
        </Alert>
      </Box>
    );
  }

  const courses = Array.isArray(data?.items) ? data.items : [];
  const totalCourses = typeof data?.total === 'number' ? data.total : 0;

  console.log('Rendering courses:', courses);

  return (
    <Box className="course-list-container">
      <Box className="course-list-header">
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 600,
            color: 'rgb(67, 67, 68)'
          }}
        >
          Courses {totalCourses > 0 && (
            <Typography 
              component="span" 
              color="text.secondary"
            >
              ({totalCourses})
            </Typography>
          )}
        </Typography>
      </Box>

      <Box className="course-filters">
        <CourseFilters
          onSearch={debouncedSearch}
          level={level}
          onLevelChange={(value) => setLevel(value)}
        />
      </Box>

      {courses.length > 0 ? (
        <>
          <Grid container spacing={3}>
            {courses.map((course) => (
              <Grid item xs={12} sm={6} md={4} key={course.id}>
                <CourseCard course={course} />
              </Grid>
            ))}
          </Grid>

          {totalCourses > ITEMS_PER_PAGE && (
            <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
              <Pagination
                count={Math.ceil(totalCourses / ITEMS_PER_PAGE)}
                page={page}
                onChange={(_, value) => setPage(value)}
                color="primary"
                size="large"
                shape="rounded"
              />
            </Box>
          )}
        </>
      ) : (
        <Box 
          sx={{ 
            textAlign: 'center', 
            py: 8,
            backgroundColor: 'background.paper',
            borderRadius: 2,
          }}
        >
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No courses found
          </Typography>
          <Typography color="text.secondary">
            Try adjusting your search or filter criteria
          </Typography>
        </Box>
      )}
    </Box>
  );
} 