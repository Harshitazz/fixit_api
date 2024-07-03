from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy import Column, Integer, String

# Database setup
DATABASE_URL = "postgresql+asyncpg://flask_user:your_password@localhost/flask_app_db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Define the Question model
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, unique=True, index=True)
    answer_text = Column(String)

    @staticmethod
    async def initialize_data():
        async with SessionLocal() as session:
            async with session.begin():
                questions = [
                    {"question_text": "What is your name?", "answer_text": "I am a bot."},
                    {"question_text": "How are you?", "answer_text": "I am fine, thank you."},
                    {"question_text": "What can you do?", "answer_text": "I can answer your questions."}
                ]
                for q in questions:
                    existing_question = await session.execute(select(Question).filter(Question.question_text == q["question_text"]))
                    if not existing_question.scalars().first():
                        question = Question(question_text=q["question_text"], answer_text=q["answer_text"])
                        session.add(question)
                await session.commit()
