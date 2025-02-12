export interface Course {
  id: number;
  title: string;
  description: string;
  instructor: string;
  duration: string;
  price: number;
  school: School;
  platform: Platform;
  categories: string[];
  engineer_level: string;
  students_amount: number;
  rating: number;
}

export interface School {
  id: number;
  name: string;
  address?: string;
  logo?: string;
  foundation_date?: string;
}

export interface Platform {
  id: number;
  name: string;
  url?: string;
  logo?: string;
  description?: string;
  features: string[];
}

export interface CourseResponse {
  items: Course[];
  total: number;
  page: number;
  size: number;
}

import { z } from 'zod';

export const CourseSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
  instructor: z.string(),
  duration: z.string(),
  price: z.number(),
  school: z.object({
    id: z.number(),
    name: z.string(),
  }),
  platform: z.object({
    id: z.number(),
    name: z.string(),
  }),
  categories: z.array(z.string()),
  engineer_level: z.string(),
  students_amount: z.number(),
  rating: z.number()
}); 