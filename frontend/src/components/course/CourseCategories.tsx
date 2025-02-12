import { Box, Chip } from '@mui/material';

interface CourseCategoriesProps {
  categories: string[];
  level: string;
}

export function CourseCategories({ categories = [], level = 'Not specified' }: CourseCategoriesProps) {
  return (
    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
      <Chip 
        size="small" 
        label={level}
        color="primary"
        variant="outlined"
      />
      {categories.slice(0, 2).map(category => (
        <Chip
          key={category}
          size="small"
          label={category}
          sx={{ backgroundColor: 'rgba(0,0,0,0.05)' }}
        />
      ))}
    </Box>
  );
} 