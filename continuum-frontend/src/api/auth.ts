import axiosClient from './axiosClient';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await axiosClient.post('/auth/login', credentials);
    const { access_token, refresh_token } = response.data;

    // FETCH USER (Backend doesn't return it on login)
    const userResponse = await axiosClient.get('/users/me', {
      headers: { Authorization: `Bearer ${access_token}` }
    });

    return {
      access_token,
      refresh_token,
      user: userResponse.data
    };
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await axiosClient.post('/users/', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await axiosClient.post('/auth/logout');
  },

  getCurrentUser: async () => {
    const response = await axiosClient.get('/users/me');
    return response.data;
  },

  forgotPassword: async (email: string): Promise<{ message: string }> => {
    const response = await axiosClient.post(`/auth/password-recovery/${email}`);
    return response.data;
  },

  resetPassword: async (data: { token: string; new_password: string }): Promise<{ message: string }> => {
    const response = await axiosClient.post('/auth/reset-password', data);
    return response.data;
  },
};
