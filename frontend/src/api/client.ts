import axios, { AxiosError } from 'axios';
import { Course, School, Platform } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    if (error.response?.status === 422) {
      // Handle validation errors
      return Promise.reject(new Error('Validation error'));
    }
    if (error.response?.status === 503) {
      // Handle service unavailable
      return Promise.reject(new Error('Service temporarily unavailable'));
    }
    return Promise.reject(error);
  }
);

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
  }): Promise<CourseResponse> => {
    try {
      const { data } = await api.get<CourseResponse>('/courses', { params });
      console.log('Raw API response:', data);
      
      // Check if response has the expected structure
      if (!data || typeof data !== 'object' || !('items' in data) || !('total' in data)) {
        throw new Error('Invalid response format from API');
      }
      
      return {
        items: data.items,
        total: data.total,
      };
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  getById: async (id: number) => {
    const { data } = await api.get<Course>(`/courses/${id}`);
    return data;
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