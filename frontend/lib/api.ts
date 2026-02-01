/**
 * API Client
 * ==========
 * Axios instance с интерсепторами для JWT.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import type { TokenPair } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Создаём instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// === Token Management ===
const TOKEN_KEY = "blog_access_token";
const REFRESH_KEY = "blog_refresh_token";

export const getAccessToken = (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
};

export const getRefreshToken = (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(REFRESH_KEY);
};

export const setTokens = (tokens: TokenPair): void => {
    localStorage.setItem(TOKEN_KEY, tokens.accessToken);
    localStorage.setItem(REFRESH_KEY, tokens.refreshToken);
};

export const clearTokens = (): void => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
};

// === Request Interceptor ===
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = getAccessToken();
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// === Response Interceptor (Auto Refresh) ===
let isRefreshing = false;
let failedQueue: Array<{
    resolve: (token: string) => void;
    reject: (error: AxiosError) => void;
}> = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
    failedQueue.forEach((prom) => {
        if (error) {
            prom.reject(error);
        } else if (token) {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & {
            _retry?: boolean;
        };

        // Если 401 и не retry запрос
        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                // Ждём пока refresh завершится
                return new Promise((resolve, reject) => {
                    failedQueue.push({
                        resolve: (token: string) => {
                            if (originalRequest.headers) {
                                originalRequest.headers.Authorization = `Bearer ${token}`;
                            }
                            resolve(api(originalRequest));
                        },
                        reject: (err: AxiosError) => {
                            reject(err);
                        },
                    });
                });
            }

            originalRequest._retry = true;
            isRefreshing = true;

            const refreshToken = getRefreshToken();

            if (!refreshToken) {
                clearTokens();
                window.location.href = "/login";
                return Promise.reject(error);
            }

            try {
                const response = await axios.post<TokenPair>(`${API_URL}/auth/refresh`, {
                    refresh_token: refreshToken,
                });

                const newTokens = response.data;
                setTokens(newTokens);
                processQueue(null, newTokens.accessToken);

                if (originalRequest.headers) {
                    originalRequest.headers.Authorization = `Bearer ${newTokens.accessToken}`;
                }

                return api(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError as AxiosError, null);
                clearTokens();
                window.location.href = "/login";
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }

        return Promise.reject(error);
    }
);

export default api;

// === API Functions ===
export const authApi = {
    register: (data: { email: string; username: string; password: string }) =>
        api.post("/auth/register", data),

    login: (data: { email: string; password: string }) =>
        api.post<TokenPair>("/auth/login", data),

    logout: () => api.post("/auth/logout"),

    me: () => api.get("/auth/me"),
};

export const postsApi = {
    list: (params?: { page?: number; perPage?: number; tag?: string; search?: string }) =>
        api.get("/posts", { params }),

    get: (slug: string) => api.get(`/posts/${slug}`),

    create: (data: any) => api.post("/posts", data),

    update: (id: string, data: any) => api.put(`/posts/${id}`, data),

    delete: (id: string) => api.delete(`/posts/${id}`),

    like: (id: string) => api.post(`/posts/${id}/like`),
};

export const tagsApi = {
    list: () => api.get("/tags"),
};
