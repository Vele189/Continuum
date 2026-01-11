import { useState, useEffect } from 'react';
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

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchCurrentUser = async () => {
    try {
      const userData = await authApi.getCurrentUser();
      const token = localStorage.getItem('access_token') || '';
      setAuth(userData, token);
    } catch {
      clearAuth();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
    setLoading(true);
    const response: AuthResponse = await authApi.login({ email, password });
    setAuth(response.user, response.access_token);
    setError(null);
    setLoading(false);
    return response;
  } catch (err: unknown) {
    const apiError = err as ApiError;
    const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Login failed';
    setError(errorMessage);
    setLoading(false);
    throw err;
  }
  };

  const register = async (email: string, password: string, first_name: string, last_name: string) => {
    try {
      setLoading(true);
      setError(null);
      const response: AuthResponse = await authApi.register({ email, password, first_name, last_name });
      setAuth(response.user, response.access_token);
      return response;
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.response?.data?.message || 'Registration failed';
      setError(errorMessage);
      throw err;
      //return null;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (err) {
     // console.error('Logout error:', err);
    } finally {
      clearAuth();
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
