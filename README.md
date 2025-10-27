# DeepKlarity AI Wiki Quiz Generator

## Overview
The DeepKlarity AI Wiki Quiz Generator is a web application that automatically generates quizzes from Wikipedia articles. Users can input a Wikipedia URL, and the system scrapes the article, extracts key information, and generates a structured multiple-choice quiz using a Large Language Model (LLM). Previously generated quizzes are stored and accessible through the History tab.

---

## Features

### Tab 1 – Generate Quiz
- Enter a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Alan_Turing`)  
- Scrapes title, summary, and sections from the article  
- Generates 5-10 quiz questions with:
  - Question text
  - Four options (A-D)
  - Correct answer
  - Short explanation
  - Difficulty level (easy, medium, hard)
  - Suggested related topics  
- Displays quiz in a clean, card-based layout

### Tab 2 – Past Quizzes (History)
- Table listing previously processed Wikipedia URLs  
- Clicking **Details** opens a modal with full quiz information  

### Backend
- Python + FastAPI  
- SQLite database storing URL, title, summary, quiz, and related topics  
- BeautifulSoup for Wikipedia scraping  
- LangChain + OpenAI API for quiz generation  

### Frontend
- React-based UI with tabs, cards, and modals  
- Clean, minimal design  

---

## Setup Instructions

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt


Set OpenAI API key (required for LLM):

setx OPENAI_API_KEY "your_api_key_here"   # Windows
export OPENAI_API_KEY="your_api_key_here" # Linux/Mac


Run backend server:

uvicorn main:app --reload


Backend runs at http://localhost:8000

2. Frontend
cd frontend
npm install
npm start


Frontend runs at http://localhost:3000

Usage

Tab 1 – Generate Quiz

Enter Wikipedia URL

Click Generate Quiz

Quiz appears in structured card layout

Tab 2 – Past Quizzes

View table of previously processed URLs

Click Details to see full quiz modal

Sample Data

sample_data/ folder contains:

urls.txt → Example Wikipedia URLs tested

quiz_alan_turing.json → Sample quiz JSON for Alan Turing article

quiz_artificial_intelligence.json → Sample quiz JSON for AI article

quiz_computer_science.json → Sample quiz JSON for Computer Science article

Screenshots

Evaluation Criteria Mapping
| **Category**                 | **How It Is Met**                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| Prompt Design & Optimization | Clear prompts for quiz generation, grounded in article summary to minimize hallucination |
| Quiz Quality                 | Relevant, diverse questions with correct difficulty levels and explanations              |
| Extraction Quality           | Clean scraping of title, summary, sections, and placeholder key entities                 |
| Functionality                | End-to-end flow: URL → scrape → generate quiz → store in database → display on frontend  |
| Code Quality                 | Modular, readable code with meaningful comments and logical structure                    |
| Error Handling               | Invalid URLs or failed LLM calls handled gracefully with fallback quiz                   |
| UI Design                    | Minimal, clear UI with tabs, card-based quiz display, and modal for details              |
| Database Accuracy            | SQLite stores all quiz data; History tab retrieves entries correctly                     |
| Testing Evidence             | `sample_data/` and screenshots demonstrate functionality and robustness                  |


Notes

Backend uses SQLite (can be switched to MySQL/PostgreSQL easily)

LangChain + OpenAI integration requires API key

If LLM fails, fallback sample quiz is generated to ensure system works

AI_Wiki_Quiz_Generator_DeepKlarity/
├─ backend/
│  ├─ main.py
│  ├─ db.py
│  └─ models.py
├─ frontend/
│  ├─ App.jsx
│  ├─ pages/
│  │  ├─ GenerateQuizPage.jsx
│  │  └─ HistoryPage.jsx
│  └─ index.css
├─ sample_data/
│  ├─ urls.txt
│  ├─ quiz_alan_turing.json
│  ├─ quiz_artificial_intelligence.json
│  └─ quiz_computer_science.json
├─ screenshots/
│  ├─ tab1_generate_quiz.png
│  ├─ tab2_history.png
│  └─ modal_details.png
└─ README.md
