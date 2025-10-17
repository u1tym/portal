export interface GetKeyRequest {
  username: string;
}

export interface GetKeyResponse {
  key: string;
}

export interface LoginRequest {
  username: string;
  key: string;
  hash: string;
}

export interface LoginResponse {
  session_string: string;
  redirect_url: string;
}

export interface ApiError {
  detail: string;
}
