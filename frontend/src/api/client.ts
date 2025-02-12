import axios from 'axios';
import { Course, School, Platform } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
    const { data } = await api.get<{ items: Course[]; total: number }>('/courses', { params });
    return data;
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