/**
 * Register Page
 * =============
 * Страница регистрации.
 */

"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function RegisterPage() {
    const router = useRouter();
    const { register } = useAuth();
    const [formData, setFormData] = useState({
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
    });
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        // Валидация
        if (formData.password !== formData.confirmPassword) {
            setError("Пароли не совпадают");
            return;
        }

        if (formData.password.length < 8) {
            setError("Пароль должен быть минимум 8 символов");
            return;
        }

        if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
            setError("Username может содержать только буквы, цифры и _");
            return;
        }

        setIsLoading(true);

        try {
            await register({
                email: formData.email,
                username: formData.username,
                password: formData.password,
            });
            router.push("/admin");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Ошибка регистрации");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4">
            <div className="w-full max-w-md">
                {/* Logo */}
                <div className="text-center mb-8">
                    <Link href="/" className="text-3xl font-heading font-bold gradient-text">
                        Blog Platform
                    </Link>
                    <p className="text-slate-400 mt-2">Создайте аккаунт</p>
                </div>

                {/* Form */}
                <div className="card p-8">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {error && (
                            <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm">
                                {error}
                            </div>
                        )}

                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Email
                            </label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="input"
                                placeholder="your@email.com"
                                required
                            />
                        </div>

                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Username
                            </label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                value={formData.username}
                                onChange={handleChange}
                                className="input"
                                placeholder="username"
                                required
                                minLength={3}
                                maxLength={50}
                            />
                            <p className="text-xs text-slate-500 mt-1">
                                3-50 символов, только буквы, цифры и _
                            </p>
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Пароль
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="input"
                                placeholder="••••••••"
                                required
                                minLength={8}
                            />
                            <p className="text-xs text-slate-500 mt-1">
                                Минимум 8 символов, хотя бы 1 цифра и 1 буква
                            </p>
                        </div>

                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                Подтвердите пароль
                            </label>
                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                type="password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                className="input"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <div className="flex items-start gap-2">
                            <input type="checkbox" id="terms" className="mt-1 rounded border-slate-300" required />
                            <label htmlFor="terms" className="text-sm text-slate-600 dark:text-slate-400">
                                Я согласен с{" "}
                                <a href="#" className="text-primary-600 hover:underline">условиями использования</a>
                                {" "}и{" "}
                                <a href="#" className="text-primary-600 hover:underline">политикой конфиденциальности</a>
                            </label>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="btn-primary w-full py-3 text-base"
                        >
                            {isLoading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                    </svg>
                                    Регистрация...
                                </span>
                            ) : (
                                "Создать аккаунт"
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
                        Уже есть аккаунт?{" "}
                        <Link href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                            Войдите
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
