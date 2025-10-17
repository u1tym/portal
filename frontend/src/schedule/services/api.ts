import axios from 'axios';
import type { ScheduleRequest, ScheduleResponse, ApiError } from '../types/schedule';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export class ScheduleService {
  static async getSchedule(request: ScheduleRequest): Promise<ScheduleResponse> {
    try {
      const response = await api.post<ScheduleResponse>('/api/get-schedule', request);
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
