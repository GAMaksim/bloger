# Blog Platform

Production-ready блог-платформа на FastAPI + Next.js.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (для локальной разработки frontend)
- Python 3.11+ (для локальной разработки backend)

### Запуск через Docker

```bash
# Клонировать репозиторий
git clone <repo-url>
cd bloger

# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps
```

**Сервисы:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Локальная разработка

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env

# Запустить PostgreSQL и Redis через Docker
docker-compose up postgres redis -d

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## 📁 Структура проекта

```
bloger/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # REST endpoints
│   │   ├── core/      # Security, config
│   │   ├── db/        # Database, Redis
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── alembic/       # Migrations
├── frontend/          # Next.js frontend
│   ├── app/           # App Router pages
│   ├── components/    # React components
│   ├── context/       # Auth context
│   ├── lib/           # API client
│   └── types/         # TypeScript types
└── docker-compose.yml
```

## 🔧 Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, Redis |
| Frontend | Next.js 14, React, TailwindCSS |
| Database | PostgreSQL |
| Auth | JWT (Access + Refresh) |
| Deploy | Docker, Render.com |

## 📝 License

MIT