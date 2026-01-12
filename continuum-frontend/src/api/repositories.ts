import axiosClient from './axiosClient';

export type GitProvider = 'github' | 'gitlab' | 'bitbucket';

export interface Repository {
  id: number;
  project_id: number;
  repository_url: string;
  repository_name: string;
  provider: GitProvider;
  webhook_secret: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateRepositoryData {
  project_id: number;
  repository_url: string;
  repository_name: string;
  provider: GitProvider;
  webhook_secret?: string;
}

export interface UpdateRepositoryData {
  is_active?: boolean;
  webhook_secret?: string;
}

export const repositoriesApi = {
  /**
   * Get all repositories linked to a project
   */
  getByProject: async (projectId: number): Promise<Repository[]> => {
    const response = await axiosClient.get(`/v1/projects/${projectId}/repositories`);
    return response.data;
  },

  /**
   * Link a repository to a project
   */
  link: async (projectId: number, data: CreateRepositoryData): Promise<Repository> => {
    const response = await axiosClient.post(`/v1/projects/${projectId}/repositories`, data);
    return response.data;
  },

  /**
   * Unlink a repository
   */
  unlink: async (repositoryId: number): Promise<void> => {
    await axiosClient.delete(`/v1/repositories/${repositoryId}`);
  },
};
