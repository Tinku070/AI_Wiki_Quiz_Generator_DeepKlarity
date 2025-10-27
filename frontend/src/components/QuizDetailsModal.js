import React from 'react';
import QuizCard from './QuizCard';

// A simple modal implementation (requires basic CSS for overlay and box)
function QuizDetailsModal({ isOpen, onClose, quizData }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Quiz Details</h3>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <QuizCard quizData={quizData} />
        </div>
      </div>
    </div>
  );
}

export default QuizDetailsModal;