import { useState, useEffect, useCallback } from 'react';
import { tasksApi, type Task, type CreateTaskData } from '../api/tasks';

interface ApiError {
  response?: {
    data?: {
      message?: string;
    };
  };
}

export const useTasks = (projectId?: string) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await tasksApi.getAll(projectId);
      setTasks(data);
    } catch (err: unknown) {
      const apiError = err as ApiError;
      setError(apiError.response?.data?.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const createTask = async (data: CreateTaskData) => {
    try {
      setError(null);
      const newTask = await tasksApi.create(data);
      setTasks([...tasks, newTask]);
      return newTask;
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.message || 'Failed to create task';
      setError(errorMessage);
      throw err;
    }
  };

  const updateTask = async (id: string, data: Partial<CreateTaskData>) => {
    try {
      setError(null);
      const updatedTask = await tasksApi.update(id, data);
      setTasks(tasks.map(t => t.id === id ? updatedTask : t));
      return updatedTask;
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.message || 'Failed to update task';
      setError(errorMessage);
      throw err;
    }
  };

  const deleteTask = async (id: string) => {
    try {
      setError(null);
      await tasksApi.delete(id);
      setTasks(tasks.filter(t => t.id !== id));
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.message || 'Failed to delete task';
      setError(errorMessage);
      throw err;
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
  };
};
