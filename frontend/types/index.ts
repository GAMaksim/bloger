/**
 * TypeScript Types
 * ================
 * Типы данных для API и компонентов.
 */

// === User ===
export interface User {
    id: string;
    username: string;
    email?: string;
    avatarUrl: string | null;
    bio: string | null;
    role?: "user" | "admin";
    isVerified?: boolean;
    createdAt: string;
}

// === Auth ===
export interface TokenPair {
    accessToken: string;
    refreshToken: string;
    tokenType: string;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    email: string;
    username: string;
    password: string;
}

// === Post ===
export interface Post {
    id: string;
    title: string;
    slug: string;
    excerpt: string | null;
    content?: string;
    coverImage: string | null;
    status: "draft" | "published";
    viewCount: number;
    likesCount: number;
    commentsCount: number;
    publishedAt: string | null;
    createdAt: string;
    updatedAt?: string;
    author: User;
    tags: Tag[];
    metaTitle?: string | null;
    metaDescription?: string | null;
}

export interface PostCreate {
    title: string;
    content: string;
    excerpt?: string;
    coverImage?: string;
    status?: "draft" | "published";
    tagIds?: string[];
    metaTitle?: string;
    metaDescription?: string;
}

export interface PostUpdate extends Partial<PostCreate> { }

export interface PostListResponse {
    items: Post[];
    total: number;
    page: number;
    perPage: number;
    pages: number;
}

// === Comment ===
export interface Comment {
    id: string;
    content: string;
    isApproved: boolean;
    createdAt: string;
    user: User;
    replies: Comment[];
}

export interface CommentCreate {
    content: string;
    parentId?: string;
}

// === Tag ===
export interface Tag {
    id: string;
    name: string;
    slug: string;
    description: string | null;
    color: string | null;
    postsCount: number;
}

// === API ===
export interface ApiError {
    detail: string;
    status?: number;
}

export interface PaginationParams {
    page?: number;
    perPage?: number;
}

// === SEO ===
export interface SEOData {
    title: string;
    description: string;
    ogImage?: string;
    canonicalUrl?: string;
    author?: string;
    publishedTime?: string;
    modifiedTime?: string;
    tags?: string[];
}
