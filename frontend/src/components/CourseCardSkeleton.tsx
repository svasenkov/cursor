import { Card, CardContent, Skeleton, Box } from '@mui/material';

export function CourseCardSkeleton() {
  return (
    <Card>
      <CardContent>
        <Skeleton variant="text" width="80%" height={32} />
        <Skeleton variant="text" width="60%" />
        <Skeleton variant="rectangular" height={80} sx={{ my: 2 }} />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Skeleton variant="text" width={80} />
          <Skeleton variant="rectangular" width={100} height={36} />
        </Box>
      </CardContent>
    </Card>
  );
} 