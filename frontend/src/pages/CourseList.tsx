import { useState } from 'react';
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
} from '@mui/material';
import { coursesApi } from '../api/client';

const ITEMS_PER_PAGE = 10;

export default function CourseList() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['courses', page, search, level],
    queryFn: () =>
      coursesApi.getAll({
        skip: (page - 1) * ITEMS_PER_PAGE,
        limit: ITEMS_PER_PAGE,
        engineer_level: level || undefined,
        search_term: search || undefined,
      }),
  });

  if (isLoading) return <Typography>Loading...</Typography>;
  if (error) return <Typography color="error">Error loading courses</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Search courses"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Engineer Level</InputLabel>
            <Select value={level} onChange={(e) => setLevel(e.target.value)}>
              <MenuItem value="">All Levels</MenuItem>
              <MenuItem value="junior">Junior</MenuItem>
              <MenuItem value="middle">Middle</MenuItem>
              <MenuItem value="senior">Senior</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {data?.items.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{course.title}</Typography>
                <Typography color="textSecondary">{course.instructor}</Typography>
                <Typography variant="body2">{course.description}</Typography>
                <Typography variant="h6" sx={{ mt: 2 }}>
                  ${course.price}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
        <Pagination
          count={Math.ceil((data?.total || 0) / ITEMS_PER_PAGE)}
          page={page}
          onChange={(_, value) => setPage(value)}
        />
      </Box>
    </Box>
  );
} 