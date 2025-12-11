import axiosClient from './axiosClient';

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateProjectData {
  name: string;
  description?: string;
}

export const projectsApi = {
  getAll: async (): Promise<Project[]> => {
    const response = await axiosClient.get('/projects');
    return response.data;
  },

  getById: async (id: string): Promise<Project> => {
    const response = await axiosClient.get(`/projects/${id}`);
    return response.data;
  },

  create: async (data: CreateProjectData): Promise<Project> => {
    const response = await axiosClient.post('/projects', data);
    return response.data;
  },

  update: async (id: string, data: Partial<CreateProjectData>): Promise<Project> => {
    const response = await axiosClient.put(`/projects/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosClient.delete(`/projects/${id}`);
  },
};

