from pydantic import BaseModel, Field
from typing import List, Literal

# --- Sub-models defining the quiz structure ---

class Answer(BaseModel):
    """A single answer choice for a multiple-choice question (MCQ)."""
    text: str = Field(description="The text of the answer choice.")
    is_correct: bool = Field(description="True if this answer is the correct choice for the question.")

class Question(BaseModel):
    """A single multiple-choice question object."""
    question_text: str = Field(description="The question based on the Wikipedia text.")
    
    # Enforce exactly 4 answers and restrict the difficulty string
    answers: List[Answer] = Field(
        description="A list of 4 answer choices, exactly one of which must be correct.",
        min_items=4,
        max_items=4
    )
    
    difficulty: Literal['Easy', 'Medium', 'Hard'] = Field(
        description="The difficulty level of the question, must be 'Easy', 'Medium', or 'Hard'."
    )

# --- Main output model ---

class QuizOutput(BaseModel):
    """The complete structured output for a generated quiz."""
    quiz_title: str = Field(description="A concise, descriptive title for the quiz based on the article.")
    
    # Enforce exactly 5 questions
    questions: List[Question] = Field(
        description="A list of 5 generated multiple-choice questions.",
        min_items=5,
        max_items=5
    )