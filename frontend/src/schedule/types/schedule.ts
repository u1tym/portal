export interface ScheduleRequest {
  username: string;
  hash_value: string;
}

export interface ScheduleResponse {
  success: boolean;
  hash_value: string;
}

export interface ApiError {
  detail: string;
}
