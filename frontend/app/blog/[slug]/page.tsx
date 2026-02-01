/**
 * Blog Post Page
 * ==============
 * Страница статьи с SSG и SEO.
 */

import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Получить статью
async function getPost(slug: string) {
    try {
        const res = await fetch(`${API_URL}/posts/${slug}`, {
            next: { revalidate: 60 },
        });
        if (!res.ok) return null;
        return res.json();
    } catch {
        return null;
    }
}

// Генерация metadata для SEO
export async function generateMetadata({
    params,
}: {
    params: { slug: string };
}): Promise<Metadata> {
    const post = await getPost(params.slug);

    if (!post) {
        return {
            title: "Статья не найдена",
        };
    }

    return {
        title: post.metaTitle || post.title,
        description: post.metaDescription || post.excerpt,
        authors: [{ name: post.author?.username }],
        openGraph: {
            title: post.title,
            description: post.excerpt,
            type: "article",
            publishedTime: post.publishedAt,
            modifiedTime: post.updatedAt,
            authors: [post.author?.username],
            images: post.coverImage ? [post.coverImage] : [],
            tags: post.tags?.map((t: any) => t.name),
        },
        twitter: {
            card: "summary_large_image",
            title: post.title,
            description: post.excerpt,
            images: post.coverImage ? [post.coverImage] : [],
        },
    };
}

// Генерация статических путей (SSG)
export async function generateStaticParams() {
    try {
        const res = await fetch(`${API_URL}/posts?per_page=100`);
        if (!res.ok) return [];
        const data = await res.json();
        return data.items?.map((post: any) => ({
            slug: post.slug,
        })) || [];
    } catch {
        return [];
    }
}

// Форматирование даты
function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString("ru-RU", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
}

export default async function BlogPostPage({
    params,
}: {
    params: { slug: string };
}) {
    const post = await getPost(params.slug);

    if (!post) {
        notFound();
    }

    return (
        <div className="min-h-screen bg-white dark:bg-slate-900">
            {/* Header */}
            <header className="sticky top-0 z-50 glass border-b border-slate-200 dark:border-slate-700">
                <div className="container-blog flex items-center justify-between h-16">
                    <Link href="/" className="text-xl font-heading font-bold gradient-text">
                        Blog Platform
                    </Link>
                    <nav className="flex items-center gap-4">
                        <Link href="/blog" className="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                            Статьи
                        </Link>
                    </nav>
                </div>
            </header>

            <article className="animate-in">
                {/* Cover Image */}
                {post.coverImage && (
                    <div className="relative h-[400px] md:h-[500px] overflow-hidden">
                        <img
                            src={post.coverImage}
                            alt={post.title}
                            className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 to-transparent" />
                    </div>
                )}

                {/* Article Header */}
                <div className="container-blog max-w-4xl py-10">
                    {/* Tags */}
                    <div className="flex flex-wrap gap-2 mb-6">
                        {post.tags?.map((tag: any) => (
                            <Link
                                key={tag.id}
                                href={`/blog?tag=${tag.slug}`}
                                className="badge-primary hover:opacity-80 transition-opacity"
                                style={{ backgroundColor: `${tag.color}20`, color: tag.color }}
                            >
                                {tag.name}
                            </Link>
                        ))}
                    </div>

                    {/* Title */}
                    <h1 className="text-4xl md:text-5xl font-heading font-bold text-slate-900 dark:text-white mb-6 leading-tight">
                        {post.title}
                    </h1>

                    {/* Meta */}
                    <div className="flex flex-wrap items-center gap-6 text-slate-600 dark:text-slate-400 mb-10 pb-10 border-b border-slate-200 dark:border-slate-700">
                        {/* Author */}
                        <div className="flex items-center gap-3">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-accent flex items-center justify-center text-white text-lg font-medium">
                                {post.author?.username?.[0]?.toUpperCase()}
                            </div>
                            <div>
                                <p className="font-medium text-slate-900 dark:text-white">
                                    {post.author?.username}
                                </p>
                                <p className="text-sm">{formatDate(post.publishedAt || post.createdAt)}</p>
                            </div>
                        </div>

                        {/* Stats */}
                        <div className="flex items-center gap-4 text-sm">
                            <span className="flex items-center gap-1">
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                                {post.viewCount} просмотров
                            </span>
                            <span className="flex items-center gap-1">
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                </svg>
                                {post.likesCount} лайков
                            </span>
                            <span className="flex items-center gap-1">
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                </svg>
                                {post.commentsCount} комментариев
                            </span>
                        </div>
                    </div>

                    {/* Content */}
                    <div
                        className="prose-blog"
                        dangerouslySetInnerHTML={{ __html: post.content }}
                    />

                    {/* Share & Like */}
                    <div className="flex items-center justify-between mt-12 pt-8 border-t border-slate-200 dark:border-slate-700">
                        <button className="btn-primary flex items-center gap-2">
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            Нравится
                        </button>
                        <div className="flex gap-2">
                            <button className="btn-ghost p-2" title="Поделиться в Twitter">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                                </svg>
                            </button>
                            <button className="btn-ghost p-2" title="Копировать ссылку">
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </article>

            {/* Footer */}
            <footer className="bg-slate-900 text-slate-400 py-12 mt-16">
                <div className="container-blog text-center">
                    <p>© 2024 Blog Platform. Все права защищены.</p>
                </div>
            </footer>
        </div>
    );
}
