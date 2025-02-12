import { Card, CardContent, CardActions, Typography, Button, Box, Chip, Rating } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Course } from '../types';
import { AccessTime, People, School } from '@mui/icons-material';

interface CourseCardProps {
  course: Course;
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        }
      }}
    >
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography 
          variant="h6" 
          gutterBottom 
          sx={{ 
            fontSize: '1.1rem',
            fontWeight: 600,
            minHeight: '2.4em',
            display: '-webkit-box',
            overflow: 'hidden',
            WebkitBoxOrient: 'vertical',
            WebkitLineClamp: 2,
          }}
        >
          {course.title}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <School sx={{ fontSize: '1rem', mr: 0.5, color: 'text.secondary' }} />
          <Typography variant="body2" color="text.secondary">
            {course.school.name}
          </Typography>
        </Box>

        <Typography 
          color="text.secondary" 
          sx={{ 
            mb: 2,
            display: '-webkit-box',
            overflow: 'hidden',
            WebkitBoxOrient: 'vertical',
            WebkitLineClamp: 3,
            minHeight: '4.5em',
          }}
        >
          {course.description}
        </Typography>

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
          <Chip 
            size="small" 
            label={course.engineer_level}
            color="primary"
            variant="outlined"
          />
          {course.categories.slice(0, 2).map(category => (
            <Chip
              key={category}
              size="small"
              label={category}
              sx={{ backgroundColor: 'rgba(0,0,0,0.05)' }}
            />
          ))}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccessTime sx={{ fontSize: '1rem', mr: 0.5, color: 'text.secondary' }} />
            <Typography variant="body2" color="text.secondary">
              {course.duration}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <People sx={{ fontSize: '1rem', mr: 0.5, color: 'text.secondary' }} />
            <Typography variant="body2" color="text.secondary">
              {course.students_amount}
            </Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Rating value={course.rating} readOnly size="small" precision={0.5} />
          <Typography variant="body2" color="text.secondary">
            ({course.rating})
          </Typography>
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between', p: 2, pt: 0 }}>
        <Typography variant="h6" color="primary.main">
          ${course.price}
        </Typography>
        <Button
          component={RouterLink}
          to={`/courses/${course.id}`}
          variant="contained"
          size="small"
          sx={{ 
            borderRadius: '20px',
            textTransform: 'none',
            px: 2
          }}
        >
          View Details
        </Button>
      </CardActions>
    </Card>
  );
} 