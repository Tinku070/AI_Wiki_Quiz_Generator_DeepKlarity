# backend/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse

# --- Components for QuizOutput ---

class QuizQuestion(BaseModel):
    """Schema for a single question item."""
    question: str
    options: List[str]
    correct_answer: str

class QuizOutput(BaseModel):
    """The full data model for a quiz returned to the frontend."""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict[str, Any]      # Corresponds to key_entities (JSON)
    sections: List[Dict[str, Any]]    # Corresponds to sections (JSON)
    quiz: List[QuizQuestion]          # Corresponds to quiz_data (JSON)
    related_topics: List[str]         # Corresponds to related_topics (JSON)
    created_at: Optional[datetime] = None # Optional as it's set by DB

    # Pydantic configuration to handle SQLAlchemy ORM objects
    class Config:
        from_attributes = True

# --- API Request Schema ---

class QuizRequest(BaseModel):
    """The expected input from the frontend when generating a quiz."""
    url: str = Field(..., description="The Wikipedia URL to scrape and generate a quiz from.")
    
    # Optional URL validation (Highly recommended to ensure it's a Wikipedia URL)
    # @classmethod
    # def validate_url(cls, v):
    #     if not v.startswith('http') and not v.startswith('https'):
    #         raise ValueError('URL must be fully qualified (start with http/https)')
    #     parsed = urlparse(v)
    #     if 'wikipedia.org' not in parsed.netloc:
    #         raise ValueError('URL must be a Wikipedia article.')
    #     return v