# C:\Users\bonab\OneDrive\Desktop\AI_Wiki_Quiz_Generator_DeepKlarity\backend\app\api\quiz_router.py

import json
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field # REQUIRED
from sqlalchemy.orm import Session
from typing import List

# Import services and models
from app.db import get_db, Quiz
from app.services.scraping_service import scrape_wikipedia_article
from app.services.llm_service import generate_quiz_content
from app.schemas.quiz import QuizOutput

# Define the input schema directly here for simplicity (or ensure it's in a common file)
class URLInput(BaseModel):
    url: str = Field(..., description="The Wikipedia URL to scrape.")

router = APIRouter(prefix="/api/v1")

# --- Endpoint 1: Generate Quiz (Handles Scraping and LLM errors) ---
@router.post("/generate_quiz", response_model=QuizOutput)
def generate_quiz(url_data: URLInput, db: Session = Depends(get_db)):
    url = url_data.url
    
    # 1. Scraping 
    try:
        article_text = scrape_wikipedia_article(url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Scraping failed for URL: {e}"
        )

    # 2. LLM Generation
    try:
        quiz_output_pydantic = generate_quiz_content(article_text)
    except Exception as e:
        error_detail = str(e)
        
        # Check for authentication/rate limit issues
        if "API Key" in error_detail or "Quota" in error_detail:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"LLM Service Authentication/Limit Error: {error_detail}"
            )
        
        # Generic internal server error for other LLM/Parsing issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quiz generation failed: {error_detail}"
        )

    # 3. Save to Database
    try:
        quiz_json_string = quiz_output_pydantic.model_dump_json()
        
        db_quiz = Quiz(
            title=quiz_output_pydantic.quiz_title,
            source_url=url,
            quiz_data=quiz_json_string
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
    except Exception as e:
        print(f"Warning: Failed to save quiz to database: {e}")
    
    # 4. Return the generated quiz
    return quiz_output_pydantic

# --- Endpoint 2: Load History (Fixes Tab 2: History Error) ---
@router.get("/past_quizzes", response_model=List[QuizOutput])
def get_past_quizzes(db: Session = Depends(get_db)):
    try:
        db_quizzes = db.query(Quiz).order_by(Quiz.id.desc()).limit(10).all()
        
        past_quizzes = []
        for db_quiz in db_quizzes:
            try:
                # Re-validate and parse the stored JSON string
                quiz_data = QuizOutput.model_validate_json(db_quiz.quiz_data)
                past_quizzes.append(quiz_data)
            except Exception as e:
                print(f"Error parsing stored quiz ID {db_quiz.id}: {e}")
                continue

        return past_quizzes
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load quiz history: Database access error: {e}"
        )