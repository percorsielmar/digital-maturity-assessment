from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select, text

from app.database import init_db, async_session, engine
from app.models import Question
from app.questions_data import DIGITAL_MATURITY_QUESTIONS
from app.routers import auth, questions, assessments, admin, assistant, questions_level2, questions_iso56002, questions_governance

async def run_migrations():
    from app.config import get_settings
    db_url = get_settings().DATABASE_URL
    is_sqlite = "sqlite" in db_url
    
    async with engine.begin() as conn:
        migrations = [
            ("organizations", "fiscal_code", "VARCHAR(50)"),
            ("organizations", "phone", "VARCHAR(50)"),
            ("organizations", "admin_name", "VARCHAR(255)"),
            ("questions", "hint", "TEXT"),
            ("assessments", "level", "INTEGER DEFAULT 1"),
            ("assessments", "audit_sheet", "TEXT"),
            ("organizations", "program", "VARCHAR(50) DEFAULT 'dma'"),
        ]
        for table, column, col_type in migrations:
            try:
                if is_sqlite:
                    result = await conn.execute(text(f"PRAGMA table_info({table})"))
                    columns = [row[1] for row in result.fetchall()]
                else:
                    result = await conn.execute(text(
                        f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}'"
                    ))
                    columns = [row[0] for row in result.fetchall()]
                if column not in columns:
                    await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
                    print(f"Migration: added {column} to {table}")
            except Exception as e:
                print(f"Migration {column}: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await run_migrations()
    await seed_questions()
    yield

app = FastAPI(
    title="Digital Maturity Assessment API",
    description="API per la valutazione della maturità digitale di aziende e PA",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(assessments.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")
app.include_router(questions_level2.router, prefix="/api")
app.include_router(questions_iso56002.router, prefix="/api")
app.include_router(questions_governance.router, prefix="/api")

async def seed_questions():
    async with async_session() as session:
        result = await session.execute(select(Question).limit(1))
        if result.scalar_one_or_none() is None:
            for q_data in DIGITAL_MATURITY_QUESTIONS:
                question = Question(
                    category=q_data["category"],
                    subcategory=q_data.get("subcategory"),
                    text=q_data["text"],
                    hint=q_data.get("hint"),
                    options=q_data["options"],
                    weight=q_data.get("weight", 1.0),
                    order=q_data.get("order", 0),
                    target_type=q_data.get("target_type", "both")
                )
                session.add(question)
            await session.commit()

@app.get("/")
async def root():
    return {"messaggio": "API Valutazione Maturità Digitale", "versione": "1.0.0"}

@app.get("/health")
async def health():
    return {"stato": "attivo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
