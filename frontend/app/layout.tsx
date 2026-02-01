/**
 * Root Layout
 * ===========
 * Главный layout приложения с провайдерами.
 */

import type { Metadata } from "next";
import { AuthProvider } from "@/context/AuthContext";
import "./globals.css";

export const metadata: Metadata = {
    title: {
        default: "Blog Platform",
        template: "%s | Blog Platform",
    },
    description: "Modern blog platform built with Next.js and FastAPI",
    keywords: ["blog", "articles", "tech", "programming"],
    authors: [{ name: "Blog Platform" }],
    openGraph: {
        type: "website",
        locale: "ru_RU",
        siteName: "Blog Platform",
    },
    twitter: {
        card: "summary_large_image",
    },
    robots: {
        index: true,
        follow: true,
    },
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="ru" suppressHydrationWarning>
            <body className="min-h-screen bg-slate-50 dark:bg-slate-900">
                <AuthProvider>{children}</AuthProvider>
            </body>
        </html>
    );
}
