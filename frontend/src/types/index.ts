// User types
export interface User {
  id: number;
  username: string;
  email: string;
}

export interface UserRegistration {
  username: string;
  email: string;
  password: string;
  password2: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

// Book types
export type BookStatus = 
  | 'draft' 
  | 'generating' 
  | 'content_generated' 
  | 'cover_pending' 
  | 'ready' 
  | 'error';

export type Domain = 
  | 'language_kids' 
  | 'tech_ai' 
  | 'nutrition' 
  | 'meditation' 
  | 'home_workout';

export type SubNiche =
  // Language and Kids
  | 'ai_learning_stories'
  | 'multilingual_coloring'
  | 'kids_mindful_journals'
  // Technology and AI
  | 'ai_ethics'
  | 'nocode_guides'
  | 'smart_home_diy'
  // Nutrition and Wellness
  | 'specialty_diet'
  | 'plant_based_cooking'
  | 'nutrition_mental_health'
  // Meditation
  | 'mindfulness_anxiety'
  | 'sleep_meditation'
  | 'gratitude_journals'
  // Home Workout
  | 'equipment_free'
  | 'yoga_remote_workers'
  | 'mobility_training';

export type PageLength = 15 | 20 | 25 | 30;

export interface Book {
  id: number;
  title: string;
  domain: Domain;
  sub_niche: SubNiche;
  page_length: PageLength;
  status: BookStatus;
  created_at: string;
  updated_at: string;
  content_generated_at: string | null;
  completed_at: string | null;
  covers: Cover[];
  selected_cover: Cover | null;
  can_download: boolean;
  download_url: string | null;
  error_message: string | null;
  user_username?: string;
}

export interface BookCreate {
  domain: Domain;
  sub_niche: SubNiche;
  page_length: PageLength;
}

// Cover types
export type CoverStyle = 'modern' | 'bold' | 'elegant';

export interface Cover {
  id: number;
  template_style: CoverStyle;
  image_path: string;
  image_url: string;
  is_selected: boolean;
  created_at: string;
  generation_params: Record<string, any>;
}

export interface CoverSelect {
  cover_id: number;
}

// Configuration types
export interface DomainOption {
  value: Domain;
  label: string;
}

export interface SubNicheOption {
  value: SubNiche;
  label: string;
}

export interface ConfigResponse {
  domains: DomainOption[];
  sub_niches: Record<Domain, SubNicheOption[]>;
  page_lengths: PageLength[];
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  error: string;
  details?: Record<string, string[]>;
}
