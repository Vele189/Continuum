import axiosClient from './axiosClient';

// Type definitions
export type Project = {
  id: number;
  name: string;
  description?: string;
  status: string;
  client_id: number;
  created_at: string;
  updated_at: string;
};

export type CreateProjectData = {
  name: string;
  description?: string;
};

export const projectsApi = {
  getAll: async (): Promise<Project[]> => {
    const response = await axiosClient.get('/v1/projects/');
    return response.data;
  },

  getById: async (id: string): Promise<Project> => {
    const response = await axiosClient.get(`/v1/projects/${id}/`);
    return response.data;
  },

  create: async (data: CreateProjectData): Promise<Project> => {
    const response = await axiosClient.post('/v1/projects/', data);
    return response.data;
  },

  update: async (id: string, data: Partial<CreateProjectData>): Promise<Project> => {
    const response = await axiosClient.put(`/v1/projects/${id}/`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosClient.delete(`/v1/projects/${id}/`);
  },
};
