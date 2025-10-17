import axios from 'axios';
import type { GetKeyRequest, GetKeyResponse, LoginRequest, LoginResponse, ApiError } from '../types/auth';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export class AuthService {
  static async getKey(request: GetKeyRequest): Promise<GetKeyResponse> {
    try {
      const response = await api.post<GetKeyResponse>('/api/get-key', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const apiError = error.response.data as ApiError;
        throw new Error(apiError.detail);
      }
      throw new Error('ネットワークエラーが発生しました');
    }
  }

  static async login(request: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await api.post<LoginResponse>('/api/login', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const apiError = error.response.data as ApiError;
        throw new Error(apiError.detail);
      }
      throw new Error('ネットワークエラーが発生しました');
    }
  }
}
