import axios, { AxiosError } from 'axios';
import { Course, School, Platform } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Custom error class
export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Error handler
const handleError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const message = error.response?.data?.detail || error.message;
    
    switch (status) {
      case 404:
        throw new APIError('Resource not found', status);
      case 422:
        throw new APIError('Validation error', status);
      case 503:
        throw new APIError('Service temporarily unavailable', status);
      default:
        throw new APIError(message, status);
    }
  }
  throw error;
};

interface CourseResponse {
  items: Course[];
  total: number;
}

export const coursesApi = {
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    engineer_level?: string;
    min_price?: number;
    max_price?: number;
    categories?: string[];
    search_term?: string;
  }) => {
    try {
      const { data } = await api.get<CourseResponse>('/courses', { params });
      return data;
    } catch (error) {
      throw handleError(error);
    }
  },

  getById: async (id: number) => {
    try {
      const { data } = await api.get<Course>(`/courses/${id}`);
      return data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 404) {
        throw new Error('Course not found');
      }
      console.error('Error fetching course:', error);
      throw error;
    }
  },

  getStatistics: async () => {
    const { data } = await api.get('/courses/statistics');
    return data;
  },
};

export const schoolsApi = {
  getAll: async () => {
    const { data } = await api.get<School[]>('/schools');
    return data;
  },
};

export const platformsApi = {
  getAll: async () => {
    const { data } = await api.get<Platform[]>('/platforms');
    return data;
  },
}; 