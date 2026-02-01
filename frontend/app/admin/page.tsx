/**
 * Admin Dashboard
 * ===============
 * Главная страница админ-панели с аналитикой.
 */

"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

// Иконки
const Icons = {
    Posts: () => (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
        </svg>
    ),
    Views: () => (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
    ),
    Likes: () => (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
    ),
    Comments: () => (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
    ),
};

function StatCard({
    title,
    value,
    change,
    icon: Icon,
    color,
}: {
    title: string;
    value: string;
    change: string;
    icon: () => JSX.Element;
    color: string;
}) {
    return (
        <div className="card p-6">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">{title}</p>
                    <p className="text-3xl font-bold text-slate-900 dark:text-white mt-1">
                        {value}
                    </p>
                    <p className={`text-sm mt-2 ${change.startsWith("+") ? "text-green-600" : "text-red-600"}`}>
                        {change} за неделю
                    </p>
                </div>
                <div className={`p-4 rounded-xl ${color}`}>
                    <Icon />
                </div>
            </div>
        </div>
    );
}

export default function AdminDashboard() {
    const { user, isLoading, isAuthenticated, logout } = useAuth();
    const router = useRouter();

    // Редирект если не авторизован
    useEffect(() => {
        if (!isLoading && !isAuthenticated) {
            router.push("/login");
        }
    }, [isLoading, isAuthenticated, router]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
            {/* Sidebar */}
            <aside className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 p-6">
                <Link href="/" className="text-xl font-heading font-bold gradient-text">
                    Blog Platform
                </Link>

                <nav className="mt-10 space-y-2">
                    <Link
                        href="/admin"
                        className="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary-50 dark:bg-primary-900/20 text-primary-600"
                    >
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                        </svg>
                        Дашборд
                    </Link>
                    <Link
                        href="/admin/posts"
                        className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700"
                    >
                        <Icons.Posts />
                        Статьи
                    </Link>
                    <Link
                        href="/admin/posts/new"
                        className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700"
                    >
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        Новая статья
                    </Link>
                    <Link
                        href="/admin/comments"
                        className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700"
                    >
                        <Icons.Comments />
                        Комментарии
                    </Link>
                </nav>

                {/* User */}
                <div className="absolute bottom-6 left-6 right-6">
                    <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-100 dark:bg-slate-700">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-accent flex items-center justify-center text-white font-medium">
                            {user?.username?.[0]?.toUpperCase()}
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="font-medium text-slate-900 dark:text-white truncate">
                                {user?.username}
                            </p>
                            <p className="text-xs text-slate-500 truncate">{user?.email}</p>
                        </div>
                        <button
                            onClick={() => logout()}
                            className="p-2 text-slate-400 hover:text-red-500"
                            title="Выйти"
                        >
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                            </svg>
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="ml-64 p-8">
                <div className="max-w-6xl">
                    <h1 className="text-3xl font-heading font-bold text-slate-900 dark:text-white mb-2">
                        Дашборд
                    </h1>
                    <p className="text-slate-600 dark:text-slate-400 mb-8">
                        Добро пожаловать, {user?.username}! Вот ваша статистика.
                    </p>

                    {/* Stats Grid */}
                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                        <StatCard
                            title="Всего статей"
                            value="12"
                            change="+2"
                            icon={Icons.Posts}
                            color="bg-blue-100 dark:bg-blue-900/30 text-blue-600"
                        />
                        <StatCard
                            title="Просмотры"
                            value="2,847"
                            change="+18%"
                            icon={Icons.Views}
                            color="bg-green-100 dark:bg-green-900/30 text-green-600"
                        />
                        <StatCard
                            title="Лайки"
                            value="142"
                            change="+12"
                            icon={Icons.Likes}
                            color="bg-red-100 dark:bg-red-900/30 text-red-600"
                        />
                        <StatCard
                            title="Комментарии"
                            value="38"
                            change="+5"
                            icon={Icons.Comments}
                            color="bg-purple-100 dark:bg-purple-900/30 text-purple-600"
                        />
                    </div>

                    {/* Quick Actions */}
                    <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">
                        Быстрые действия
                    </h2>
                    <div className="grid md:grid-cols-3 gap-4">
                        <Link
                            href="/admin/posts/new"
                            className="card p-6 hover:border-primary-500 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 mb-4 group-hover:scale-110 transition-transform">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                </svg>
                            </div>
                            <h3 className="font-semibold text-slate-900 dark:text-white mb-1">
                                Написать статью
                            </h3>
                            <p className="text-sm text-slate-500">
                                Создайте новую публикацию
                            </p>
                        </Link>
                        <Link
                            href="/admin/posts"
                            className="card p-6 hover:border-primary-500 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 mb-4 group-hover:scale-110 transition-transform">
                                <Icons.Posts />
                            </div>
                            <h3 className="font-semibold text-slate-900 dark:text-white mb-1">
                                Мои статьи
                            </h3>
                            <p className="text-sm text-slate-500">
                                Управляйте публикациями
                            </p>
                        </Link>
                        <Link
                            href="/"
                            className="card p-6 hover:border-primary-500 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center text-purple-600 mb-4 group-hover:scale-110 transition-transform">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                            </div>
                            <h3 className="font-semibold text-slate-900 dark:text-white mb-1">
                                Открыть блог
                            </h3>
                            <p className="text-sm text-slate-500">
                                Посмотреть публичную версию
                            </p>
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
}
