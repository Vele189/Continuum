import axiosClient from './axiosClient';

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  priority?: string;
  projectId: string;
  assignedTo?: string;
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  status?: string;
  priority?: string;
  projectId: string;
  assignedTo?: string;
  dueDate?: string;
}

export const tasksApi = {
  getAll: async (projectId?: string): Promise<Task[]> => {
    const url = projectId ? `/tasks?projectId=${projectId}` : '/tasks';
    const response = await axiosClient.get(url);
    return response.data;
  },

  getById: async (id: string): Promise<Task> => {
    const response = await axiosClient.get(`/tasks/${id}`);
    return response.data;
  },

  create: async (data: CreateTaskData): Promise<Task> => {
    const response = await axiosClient.post('/tasks', data);
    return response.data;
  },

  update: async (id: string, data: Partial<CreateTaskData>): Promise<Task> => {
    const response = await axiosClient.put(`/tasks/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosClient.delete(`/tasks/${id}`);
  },
};

