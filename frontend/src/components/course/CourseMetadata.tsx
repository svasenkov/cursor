import { Box, Typography } from '@mui/material';
import { AccessTime, People } from '@mui/icons-material';

interface CourseMetadataProps {
  duration: string;
  studentsAmount: number;
}

export function CourseMetadata({ duration, studentsAmount }: CourseMetadataProps) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
      <Box className="course-metadata">
        <AccessTime sx={{ fontSize: '1rem', color: 'text.secondary' }} />
        <Typography variant="body2" color="text.secondary">
          {duration || 'Not specified'}
        </Typography>
      </Box>
      <Box className="course-metadata">
        <People sx={{ fontSize: '1rem', color: 'text.secondary' }} />
        <Typography variant="body2" color="text.secondary">
          {studentsAmount.toLocaleString() || '0'}
        </Typography>
      </Box>
    </Box>
  );
} 