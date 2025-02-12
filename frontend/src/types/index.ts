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
  address: string;
  logo: string;
  foundation_date: string;
}

export interface Platform {
  id: number;
  name: string;
  url: string;
  logo: string;
  description: string;
  features: string[];
} 