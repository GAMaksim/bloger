/**
 * Homepage
 * ========
 * Главная страница блога со списком статей.
 */

import Link from "next/link";
import { Suspense } from "react";

// В реальном проекте это будет fetch с сервера
async function getPosts() {
    try {
        const res = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/posts?per_page=9`,
            { next: { revalidate: 60 } } // ISR - обновляем каждую минуту
        );
        if (!res.ok) return { items: [], total: 0 };
        return res.json();
    } catch {
        return { items: [], total: 0 };
    }
}

function PostCardSkeleton() {
    return (
        <div className="card p-4 space-y-4">
            <div className="skeleton h-48 w-full rounded-lg" />
            <div className="skeleton h-4 w-3/4" />
            <div className="skeleton h-4 w-1/2" />
            <div className="flex gap-2">
                <div className="skeleton h-6 w-16 rounded-full" />
                <div className="skeleton h-6 w-16 rounded-full" />
            </div>
        </div>
    );
}

async function PostsList() {
    const data = await getPosts();
    const posts = data.items || [];

    if (posts.length === 0) {
        return (
            <div className="text-center py-20">
                <p className="text-slate-500 text-lg">Статей пока нет</p>
                <p className="text-slate-400 mt-2">Будьте первым, кто напишет!</p>
            </div>
        );
    }

    return (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post: any) => (
                <Link key={post.id} href={`/blog/${post.slug}`}>
                    <article className="card-hover overflow-hidden group">
                        {post.coverImage && (
                            <div className="relative h-48 overflow-hidden">
                                <img
                                    src={post.coverImage}
                                    alt={post.title}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                                />
                            </div>
                        )}
                        <div className="p-5">
                            <div className="flex gap-2 mb-3">
                                {post.tags?.slice(0, 2).map((tag: any) => (
                                    <span
                                        key={tag.id}
                                        className="badge-primary"
                                        style={{ backgroundColor: `${tag.color}20`, color: tag.color }}
                                    >
                                        {tag.name}
                                    </span>
                                ))}
                            </div>
                            <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
                                {post.title}
                            </h2>
                            <p className="text-slate-600 dark:text-slate-400 line-clamp-2 text-sm mb-4">
                                {post.excerpt}
                            </p>
                            <div className="flex items-center justify-between text-sm text-slate-500">
                                <div className="flex items-center gap-2">
                                    <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary-500 to-accent flex items-center justify-center text-white text-xs font-medium">
                                        {post.author?.username?.[0]?.toUpperCase()}
                                    </div>
                                    <span>{post.author?.username}</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className="flex items-center gap-1">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                        {post.viewCount}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                        </svg>
                                        {post.likesCount}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </article>
                </Link>
            ))}
        </div>
    );
}

export default function HomePage() {
    return (
        <div className="min-h-screen">
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
                        <Link href="/login" className="btn-secondary text-sm">
                            Войти
                        </Link>
                        <Link href="/register" className="btn-primary text-sm">
                            Регистрация
                        </Link>
                    </nav>
                </div>
            </header>

            {/* Hero */}
            <section className="py-20 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50" />
                <div className="container-blog relative">
                    <div className="max-w-3xl mx-auto text-center">
                        <h1 className="text-5xl md:text-6xl font-heading font-bold mb-6 animate-fade-in">
                            Место, где рождаются
                            <span className="block mt-2 bg-gradient-to-r from-primary-400 via-accent to-primary-400 bg-clip-text text-transparent">
                                великие идеи
                            </span>
                        </h1>
                        <p className="text-xl text-slate-300 mb-8 animate-slide-up">
                            Читайте, пишите и делитесь знаниями с сообществом разработчиков
                        </p>
                        <div className="flex gap-4 justify-center animate-slide-up">
                            <Link href="/blog" className="btn-primary text-base px-6 py-3">
                                Читать статьи
                            </Link>
                            <Link href="/register" className="btn-secondary text-base px-6 py-3">
                                Начать писать
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Posts */}
            <main className="py-16 container-blog">
                <div className="flex items-center justify-between mb-10">
                    <h2 className="text-3xl font-heading font-bold text-slate-900 dark:text-white">
                        Последние статьи
                    </h2>
                    <Link href="/blog" className="text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
                        Все статьи
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </Link>
                </div>

                <Suspense
                    fallback={
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {[1, 2, 3].map((i) => (
                                <PostCardSkeleton key={i} />
                            ))}
                        </div>
                    }
                >
                    <PostsList />
                </Suspense>
            </main>

            {/* Footer */}
            <footer className="bg-slate-900 text-slate-400 py-12">
                <div className="container-blog">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <p>© 2024 Blog Platform. Все права защищены.</p>
                        <div className="flex gap-6">
                            <a href="#" className="hover:text-white transition-colors">GitHub</a>
                            <a href="#" className="hover:text-white transition-colors">Twitter</a>
                            <a href="#" className="hover:text-white transition-colors">Telegram</a>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
