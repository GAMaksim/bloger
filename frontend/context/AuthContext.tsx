/**
 * Auth Context
 * ============
 * Контекст аутентификации с хранением пользователя и токенов.
 */

"use client";

import {
    createContext,
    useContext,
    useEffect,
    useState,
    useCallback,
    ReactNode,
} from "react";
import api, {
    authApi,
    setTokens,
    clearTokens,
    getAccessToken,
} from "@/lib/api";
import type { User, TokenPair, LoginCredentials, RegisterData } from "@/types";

interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (credentials: LoginCredentials) => Promise<void>;
    register: (data: RegisterData) => Promise<void>;
    logout: () => Promise<void>;
    refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Загрузка пользователя при старте
    const loadUser = useCallback(async () => {
        const token = getAccessToken();
        if (!token) {
            setIsLoading(false);
            return;
        }

        try {
            const response = await authApi.me();
            setUser(response.data);
        } catch (error) {
            clearTokens();
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        loadUser();
    }, [loadUser]);

    // Логин
    const login = async (credentials: LoginCredentials) => {
        console.log("Login: starting...");
        const response = await authApi.login(credentials);
        console.log("Login: response received", response.data);
        // API возвращает snake_case, конвертируем в camelCase
        const tokens: TokenPair = {
            accessToken: (response.data as any).access_token,
            refreshToken: (response.data as any).refresh_token,
            tokenType: (response.data as any).token_type,
        };
        console.log("Login: tokens extracted", { hasAccessToken: !!tokens.accessToken, hasRefreshToken: !!tokens.refreshToken });
        setTokens(tokens);
        console.log("Login: tokens saved to localStorage");
        await loadUser();
        console.log("Login: loadUser completed");
    };

    // Регистрация
    const register = async (data: RegisterData) => {
        await authApi.register(data);
        // После регистрации делаем автоматический логин
        await login({ email: data.email, password: data.password });
    };

    // Выход
    const logout = async () => {
        try {
            await authApi.logout();
        } catch {
            // Игнорируем ошибки logout
        } finally {
            clearTokens();
            setUser(null);
        }
    };

    // Обновить данные пользователя
    const refreshUser = async () => {
        await loadUser();
    };

    const value: AuthContextType = {
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refreshUser,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
