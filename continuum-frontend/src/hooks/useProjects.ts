import { useState, useEffect } from 'react';
import { projectsApi, type Project, type CreateProjectData } from '../api/projects';

export const useProjects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await projectsApi.getAll();
      setProjects(data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (data: CreateProjectData) => {
    try {
      setError(null);
      const newProject = await projectsApi.create(data);
      setProjects([...projects, newProject]);
      return newProject;
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to create project';
      setError(errorMessage);
      throw err;
    }
  };

  const updateProject = async (id: string, data: Partial<CreateProjectData>) => {
    try {
      setError(null);
      const updatedProject = await projectsApi.update(id, data);
      setProjects(projects.map(p => p.id === id ? updatedProject : p));
      return updatedProject;
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to update project';
      setError(errorMessage);
      throw err;
    }
  };

  const deleteProject = async (id: string) => {
    try {
      setError(null);
      await projectsApi.delete(id);
      setProjects(projects.filter(p => p.id !== id));
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to delete project';
      setError(errorMessage);
      throw err;
    }
  };

  return {
    projects,
    loading,
    error,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };
};

