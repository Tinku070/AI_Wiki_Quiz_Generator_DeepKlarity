from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Quiz
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class QuizRequest(BaseModel):
    url: str

def scrape_wikipedia(url: str):
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch URL")
    soup = BeautifulSoup(res.text, "html.parser")
    
    title = soup.find("h1").text
    paragraphs = soup.find_all("p")
    summary = " ".join([p.text for p in paragraphs[:5]])
    sections = [h2.text for h2 in soup.find_all("h2")]
    
    return {"title": title, "summary": summary, "sections": sections}

def generate_quiz(text: str):
    llm = OpenAI(temperature=0)
    prompt = f"""
    Generate 5 quiz questions from the following text. 
    Each question must have 4 options (A-D), one correct answer, 
    a short explanation, difficulty level (easy, medium, hard), 
    and suggested related topics. Return JSON.
    Text: {text}
    """
    response = llm(prompt)
    # If the LLM returns stringified JSON
    try:
        return json.loads(response)
    except:
        # Fallback: simple example quiz
        return {
            "quiz": [
                {
                    "question": "Sample Q?",
                    "options": ["A","B","C","D"],
                    "answer": "A",
                    "explanation": "Sample",
                    "difficulty": "easy"
                }
            ],
            "related_topics": ["Wikipedia"]
        }

@app.post("/generate_quiz/")
def create_quiz(request: QuizRequest):
    db: Session = SessionLocal()
    existing = db.query(Quiz).filter(Quiz.url == request.url).first()
    if existing:
        return existing
    
    data = scrape_wikipedia(request.url)
    quiz_data = generate_quiz(data["summary"])
    
    new_quiz = Quiz(
        url=request.url,
        title=data["title"],
        summary=data["summary"],
        sections=data["sections"],
        key_entities={"people": [], "organizations": [], "locations": []},
        quiz=quiz_data["quiz"],
        related_topics=quiz_data.get("related_topics", [])
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

@app.get("/history/")
def get_history():
    db: Session = SessionLocal()
    return db.query(Quiz).all()

@app.get("/history/{quiz_id}")
def get_quiz_details(quiz_id: int):
    db: Session = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

def generate_quiz(text: str):
    try:
        from langchain.llms import OpenAI
        llm = OpenAI(temperature=0)
        prompt = f"""
        Generate 5 quiz questions from the following text. 
        Each question must have 4 options (A-D), one correct answer, 
        a short explanation, difficulty level (easy, medium, hard), 
        and suggested related topics. Return JSON.
        Text: {text}
        """
        response = llm(prompt)
        return json.loads(response)
    except Exception as e:
        print("LLM error:", e)
        # Fallback quiz
        return {
            "quiz": [
                {
                    "question": "Sample Question?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "This is a sample explanation.",
                    "difficulty": "easy"
                }
            ],
            "related_topics": ["Wikipedia"]
        }
