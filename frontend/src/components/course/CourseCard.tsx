import { Card, CardContent, CardActions, Typography, Button, Box, Rating } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { School } from '@mui/icons-material';
import { Course } from '../../types';
import { CourseMetadata } from './CourseMetadata';
import { CourseCategories } from './CourseCategories';
import '../../styles/CourseCard.css';

interface CourseCardProps {
  course: Course;
}

export function CourseCard({ course }: CourseCardProps) {
  if (!course?.id) {
    return null;
  }

  const navigate = useNavigate();
  
  const handleViewDetails = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate(`/courses/${course.id}`, {
      state: { course }  // Pass course data to avoid additional API call
    });
  };

  const {
    id,
    title = 'Untitled Course',
    description = 'No description available',
    school = null,
    engineer_level = 'Not specified',
    categories = [],
    duration = 'Not specified',
    students_amount = 0,
    rating = 0,
    price = 0
  } = course;

  const schoolName = school?.name || 'Unknown School';

  return (
    <Card className="course-card">
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography className="course-title" variant="h6" gutterBottom>
          {title}
        </Typography>

        <Box className="course-metadata">
          <School sx={{ fontSize: '1rem', color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            {schoolName}
          </Typography>
        </Box>

        <Typography className="course-description" color="text.secondary" sx={{ mb: 2 }}>
          {description}
        </Typography>

        <CourseCategories 
          categories={Array.isArray(categories) ? categories : []} 
          level={engineer_level} 
        />

        <CourseMetadata 
          duration={duration}
          studentsAmount={students_amount}
        />

        <Box className="course-metadata">
          <Rating 
            value={typeof rating === 'number' ? rating : 0} 
            readOnly 
            size="small" 
            precision={0.5} 
          />
          <Typography variant="body2" color="text.secondary">
            ({typeof rating === 'number' ? rating.toFixed(1) : '0.0'})
          </Typography>
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', p: 2, pt: 0 }}>
        <Typography variant="h6" color="primary.main">
          ${typeof price === 'number' ? price.toFixed(2) : '0.00'}
        </Typography>
        <Button
          onClick={handleViewDetails}
          variant="contained"
          size="small"
          className="course-action-button"
        >
          View Details
        </Button>
      </CardActions>
    </Card>
  );
} 