import React, { useState } from 'react';
// Assuming you have some basic styling for .correct, .selected, etc.

function QuizCard({ quizData }) {
  // State to toggle between Quiz Mode (answers hidden) and Review Mode (answers shown)
  const [showAnswers, setShowAnswers] = useState(false);
  
  // State to store the user's selection for each question (e.g., { 0: "Option A", 1: "Option C" })
  const [userAnswers, setUserAnswers] = useState({});

  if (!quizData || !quizData.quiz || quizData.quiz.length === 0) {
    return <p>No quiz data available to display.</p>;
  }

  const handleOptionSelect = (qIndex, selectedOption) => {
    // Only allow selection if answers are hidden (Take Quiz Mode)
    if (!showAnswers) {
      setUserAnswers(prev => ({
        ...prev,
        [qIndex]: selectedOption
      }));
    }
  };
  
  const calculateScore = () => {
    let correctCount = 0;
    quizData.quiz.forEach((q, index) => {
      if (userAnswers[index] === q.answer) {
        correctCount++;
      }
    });
    return correctCount;
  };

  const score = showAnswers ? calculateScore() : 0;
  
  return (
    <div className="quiz-card-container">
      <h2>{quizData.title}</h2>
      <p className="summary">**URL:** <a href={quizData.url} target="_blank" rel="noopener noreferrer">{quizData.url}</a></p>
      <p className="summary">**Summary:** {quizData.summary}</p>
      
      {/* Quiz Mode Toggle and Score Display */}
      <div className="quiz-controls">
        <button onClick={() => setShowAnswers(!showAnswers)}>
          {showAnswers ? 'Hide Answers & Reset Selections' : 'Show Answers / Review Mode'}
        </button>
        {showAnswers && (
          <p className="score-display">
            **Your Score:** {score} / {quizData.quiz.length} Correct
          </p>
        )}
      </div>

      {/* 1. Related Topics */}
      <div className="section related-topics">
        <h3>Suggested Topics</h3>
        <p>{(quizData.related_topics || []).join(' | ')}</p>
      </div>

      {/* 2. Questions */}
      <div className="section questions">
        <h3>Quiz Questions ({quizData.quiz.length})</h3>
        
        {quizData.quiz.map((q, qIndex) => (
          <div key={qIndex} className="question-item card">
            <h4>{qIndex + 1}. {q.question}</h4>
            <p>Difficulty: <span className={`diff-${q.difficulty}`}>{q.difficulty}</span></p>
            
            <ul className="options-list">
              {q.options.map((option, oIndex) => {
                const isSelected = userAnswers[qIndex] === option;
                const isCorrect = option === q.answer;
                
                let optionClass = '';
                if (isSelected) {
                    // Mark user selection
                    optionClass = 'selected';
                    // If in review mode, mark if user selection is wrong
                    if (showAnswers && !isCorrect) {
                        optionClass += ' incorrect-selection';
                    }
                }
                
                // Mark correct answer only in review mode
                if (showAnswers && isCorrect) {
                    optionClass = 'correct';
                }

                return (
                  <li 
                    key={oIndex} 
                    className={optionClass}
                    onClick={() => handleOptionSelect(qIndex, option)}
                  >
                    {String.fromCharCode(65 + oIndex)}: {option}
                  </li>
                );
              })}
            </ul>
            
            {showAnswers && (
              <p className="explanation">**Explanation:** {q.explanation}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default QuizCard;