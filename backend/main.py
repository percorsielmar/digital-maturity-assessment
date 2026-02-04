from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select, text

from app.database import init_db, async_session, engine
from app.models import Question
from app.questions_data import DIGITAL_MATURITY_QUESTIONS
from app.routers import auth, questions, assessments, admin

async def run_migrations():
    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE organizations ADD COLUMN IF NOT EXISTS fiscal_code VARCHAR(50)"))
        await conn.execute(text("ALTER TABLE organizations ADD COLUMN IF NOT EXISTS phone VARCHAR(50)"))
        await conn.execute(text("ALTER TABLE organizations ADD COLUMN IF NOT EXISTS admin_name VARCHAR(255)"))
        await conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS hint TEXT"))

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
