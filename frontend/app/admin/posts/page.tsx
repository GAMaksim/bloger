/**
 * Admin Posts List Page
 */

"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { postsApi } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

interface Post {
    id: string;
    title: string;
    slug: string;
    status: string;
    created_at: string;
    view_count: number;
}

export default function AdminPostsPage() {
    const { user } = useAuth();
    const [posts, setPosts] = useState<Post[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await postsApi.list({ perPage: 100 });
                setPosts(response.data.items || []);
            } catch (error) {
                console.error("Error fetching posts:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchPosts();
    }, []);

    return (
        <div className="min-h-screen bg-slate-900 p-8">
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-white">Мои посты</h1>
                    <Link
                        href="/admin/posts/new"
                        className="btn-primary px-6 py-3"
                    >
                        + Новый пост
                    </Link>
                </div>

                {isLoading ? (
                    <div className="text-center text-slate-400 py-12">
                        Загрузка...
                    </div>
                ) : posts.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-slate-400 mb-4">У вас пока нет постов</p>
                        <Link
                            href="/admin/posts/new"
                            className="btn-primary inline-block px-6 py-3"
                        >
                            Создать первый пост
                        </Link>
                    </div>
                ) : (
                    <div className="bg-slate-800 rounded-lg overflow-hidden">
                        <table className="w-full">
                            <thead className="bg-slate-700">
                                <tr>
                                    <th className="text-left p-4 text-slate-300">Заголовок</th>
                                    <th className="text-left p-4 text-slate-300">Статус</th>
                                    <th className="text-left p-4 text-slate-300">Просмотры</th>
                                    <th className="text-left p-4 text-slate-300">Дата</th>
                                    <th className="p-4"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {posts.map((post) => (
                                    <tr key={post.id} className="border-t border-slate-700 hover:bg-slate-700/50">
                                        <td className="p-4 text-white">{post.title}</td>
                                        <td className="p-4">
                                            <span className={`px-2 py-1 rounded text-xs ${post.status === 'PUBLISHED'
                                                    ? 'bg-green-500/20 text-green-400'
                                                    : 'bg-yellow-500/20 text-yellow-400'
                                                }`}>
                                                {post.status === 'PUBLISHED' ? 'Опубликован' : 'Черновик'}
                                            </span>
                                        </td>
                                        <td className="p-4 text-slate-400">{post.view_count}</td>
                                        <td className="p-4 text-slate-400">
                                            {new Date(post.created_at).toLocaleDateString('ru-RU')}
                                        </td>
                                        <td className="p-4">
                                            <Link
                                                href={`/admin/posts/${post.id}/edit`}
                                                className="text-sky-400 hover:text-sky-300"
                                            >
                                                Редактировать
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <div className="mt-8">
                    <Link href="/admin" className="text-slate-400 hover:text-white">
                        ← Назад в панель
                    </Link>
                </div>
            </div>
        </div>
    );
}
