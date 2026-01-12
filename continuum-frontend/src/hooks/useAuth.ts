import { useState, useEffect, useCallback } from 'react';
import { authApi, type AuthResponse } from '../api/auth';
import { useAuthStore } from '../store/authStore';

interface ApiError {
  response?: {
    data?: {
      message?: string;
      detail?: string;
    };
  };
}

export const useAuth = () => {
  const { user, setAuth, clearAuth } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCurrentUser = useCallback(async () => {
    try {
      const userData = await authApi.getCurrentUser();
      const token = localStorage.getItem('access_token') || '';
      setAuth(userData, token);
    } catch {
      clearAuth();
    } finally {
      setLoading(false);
    }
  }, [setAuth, clearAuth]);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [fetchCurrentUser]);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      const response: AuthResponse = await authApi.login({ email, password });
      localStorage.setItem('access_token', response.access_token);
      if (response.refresh_token) {
        localStorage.setItem('refresh_token', response.refresh_token);
      }
      if (response.user) {
        setAuth(response.user, response.access_token);
      } else {
        await fetchCurrentUser();
      }
      return response;
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Login failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, first_name: string, last_name: string) => {
    try {
      setLoading(true);
      setError(null);
      const response: AuthResponse = await authApi.register({ email, password, first_name, last_name });
      localStorage.setItem('access_token', response.access_token);
      if (response.refresh_token) {
        localStorage.setItem('refresh_token', response.refresh_token);
      }
      if (response.user) {
        setAuth(response.user, response.access_token);
      } else {
        await fetchCurrentUser();
      }
      return response;
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Registration failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch {
     // Logout error - silently fail
    } finally {
      clearAuth();
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('token');
    }
  };

  const forgotPassword = async (email: string) => {
    try {
      setLoading(true);
      setError(null);
      return await authApi.forgotPassword(email);
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Password recovery request failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (token: string, newPassword: string) => {
    try {
      setLoading(true);
      setError(null);
      return await authApi.resetPassword({ token, new_password: newPassword });
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Password reset failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    user,
    loading,
    error,
    setError,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    isAuthenticated: !!user,
  };
};
