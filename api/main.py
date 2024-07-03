

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

# Assuming you've defined your SQLAlchemy models and database setup as shown earlier

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for your frontend
origins = [
    "http://localhost:3000",
    "https://fixit-git-main-harshitazzs-projects.vercel.app/",
    "https://fixit-harshitazzs-projects.vercel.app/",
    "https://fixit-kohl.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database setup and session dependency
DATABASE_URL = "postgresql+asyncpg://flask_user:your_password@localhost/flask_app_db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Predefined questions and answers (with case insensitivity)
predefined_questions = {
    "what is your name?": "I am a bot.",
    "how are you?": "I am fine, thank you.",
    "what can you do?": "I can answer your questions."
}

# Define the Question model (assuming you already have it defined)

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    return{"example":"this is an exxs"}

@app.post("/ask")
async def ask_question(question: Question):
    question_text = question.question.lower()  # Convert to lowercase for case insensitivity
    answer = predefined_questions.get(question_text)
    if not answer:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
