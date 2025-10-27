# C:\Users\bonab\OneDrive\Desktop\AI_Wiki_Quiz_Generator_DeepKlarity\backend\app\services\llm_service.py

import os
import logging
from google import genai
from google.genai import types
from google.genai.errors import APIError
from app.api.schemas.quiz import QuizOutput

logger = logging.getLogger(__name__)

# ============================================================
#  GEMINI CLIENT INITIALIZATION
# ============================================================
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is NOT SET.")

    client = genai.Client(api_key=GEMINI_API_KEY)

except ValueError as e:
    logger.critical(f"Configuration Error: {e}")
    raise Exception(
        f"FATAL: Failed to initialize Gemini client. Please set GEMINI_API_KEY. Details: {e}"
    )
except Exception as e:
    logger.critical(f"Unexpected error during Gemini client setup: {e}")
    raise Exception(
        f"FATAL: Unexpected error during LLM client setup. Details: {e}"
    )

# ============================================================
#  SYSTEM PROMPT (LLM CONTEXT)
# ============================================================
SYSTEM_PROMPT = """
You are an expert quiz generator. Your task is to analyze the provided Wikipedia article text and generate a quiz. 
The output MUST be a valid JSON object that strictly follows the provided schema. 
Rules:
- Generate exactly 5 multiple-choice questions.
- Each question must have exactly 4 answer choices.
- Exactly one answer choice per question must have "is_correct": true.
- Use the difficulty levels 'Easy', 'Medium', or 'Hard' accurately.
"""

# ============================================================
#  MAIN FUNCTION: generate_quiz_content
# ============================================================
def generate_quiz_content(article_text: str) -> QuizOutput:
    """
    Generates a structured quiz using the Gemini LLM.
    
    Args:
        article_text (str): The Wikipedia article content.

    Returns:
        QuizOutput: A validated quiz structure as per the defined schema.

    Raises:
        Exception: If API fails, quota exceeded, or output is invalid.
    """
    contents = [SYSTEM_PROMPT, f"ARTICLE TEXT:\n\n{article_text}"]

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=QuizOutput,
    )

    try:
        logger.info("Sending request to Gemini model for quiz generation...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
            request_options={"timeout": 60},
        )

        quiz_data = QuizOutput.model_validate_json(response.text)
        logger.info("Quiz successfully generated and validated.")
        return quiz_data

    except QuotaError as e:
        logger.error(f"Gemini API Quota/Rate Limit Error: {e}", exc_info=True)
        raise Exception(
            "LLM API Quota exceeded. Please wait a minute or check usage limits."
        ) from e

    except APIError as e:
        logger.error(f"Gemini API Error: {e}", exc_info=True)
        raise Exception(
            "LLM API request failed. Check API key validity or model configuration."
        ) from e

    except Exception as e:
        logger.error(f"Error processing LLM output: {e}", exc_info=True)
        raise Exception(
            "Failed to process LLM output into a valid quiz structure. The model likely returned invalid JSON."
        ) from e
