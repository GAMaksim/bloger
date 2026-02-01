/**
 * Create New Post Page
 */

"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { postsApi } from "@/lib/api";

export default function NewPostPage() {
    const router = useRouter();
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [excerpt, setExcerpt] = useState("");
    const [status, setStatus] = useState("draft");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setIsLoading(true);

        try {
            await postsApi.create({
                title,
                content,
                excerpt: excerpt || undefined,
                status,
            });
            router.push("/admin/posts");
        } catch (err: any) {
            const errorData = err.response?.data;
            if (errorData?.detail) {
                // Handle Pydantic validation errors
                if (Array.isArray(errorData.detail)) {
                    const messages = errorData.detail.map((e: any) => e.msg || e.message || JSON.stringify(e));
                    setError(messages.join(", "));
                } else if (typeof errorData.detail === "string") {
                    setError(errorData.detail);
                } else {
                    setError("Ошибка валидации");
                }
            } else {
                setError("Ошибка при создании поста");
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 p-8">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <Link href="/admin/posts" className="text-slate-400 hover:text-white">
                        ← Назад к постам
                    </Link>
                </div>

                <h1 className="text-3xl font-bold text-white mb-8">Новый пост</h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && (
                        <div className="p-4 rounded-lg bg-red-900/20 border border-red-800 text-red-400">
                            {error}
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Заголовок
                        </label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            className="input w-full"
                            placeholder="Введите заголовок..."
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Краткое описание (excerpt)
                        </label>
                        <textarea
                            value={excerpt}
                            onChange={(e) => setExcerpt(e.target.value)}
                            className="input w-full h-24"
                            placeholder="Краткое описание для превью..."
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Содержимое
                        </label>
                        <textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            className="input w-full h-64"
                            placeholder="Напишите ваш пост..."
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Статус
                        </label>
                        <select
                            value={status}
                            onChange={(e) => setStatus(e.target.value)}
                            className="input w-full"
                        >
                            <option value="draft">Черновик</option>
                            <option value="published">Опубликовать</option>
                        </select>
                    </div>

                    <div className="flex gap-4">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="btn-primary px-8 py-3"
                        >
                            {isLoading ? "Сохранение..." : "Сохранить"}
                        </button>
                        <Link
                            href="/admin/posts"
                            className="px-8 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600"
                        >
                            Отмена
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
}
