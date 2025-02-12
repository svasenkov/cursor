import { Grid, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { Search, FilterList } from '@mui/icons-material';

interface CourseFiltersProps {
  onSearch: (value: string) => void;
  level: string;
  onLevelChange: (value: string) => void;
}

export function CourseFilters({ onSearch, level, onLevelChange }: CourseFiltersProps) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <TextField
          fullWidth
          placeholder="Search courses..."
          onChange={(e) => onSearch(e.target.value)}
          InputProps={{
            startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
          sx={{ backgroundColor: 'background.default' }}
        />
      </Grid>
      <Grid item xs={12} md={4}>
        <FormControl fullWidth>
          <InputLabel>Level</InputLabel>
          <Select
            value={level}
            onChange={(e) => onLevelChange(e.target.value as string)}
            startAdornment={<FilterList sx={{ mr: 1, color: 'text.secondary' }} />}
            sx={{ backgroundColor: 'background.default' }}
          >
            <MenuItem value="">All Levels</MenuItem>
            <MenuItem value="junior">Junior</MenuItem>
            <MenuItem value="middle">Middle</MenuItem>
            <MenuItem value="senior">Senior</MenuItem>
          </Select>
        </FormControl>
      </Grid>
    </Grid>
  );
} 