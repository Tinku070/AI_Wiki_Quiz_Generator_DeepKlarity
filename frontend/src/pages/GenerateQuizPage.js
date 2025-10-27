import React, { useState } from 'react';
import axios from 'axios';

export default function GenerateQuizPage() {
  const [url, setUrl] = useState('');
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateQuiz = async () => {
    if (!url) return alert("Enter a Wikipedia URL");
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/generate_quiz/', { url });
      setQuizData(res.data);
    } catch (err) {
      alert("Failed to generate quiz");
    }
    setLoading(false);
  };

  return (
    <div>
      <input type="text" value={url} placeholder="Enter Wikipedia URL" onChange={e=>setUrl(e.target.value)} style={{width:'60%',padding:'10px',marginRight:'10px'}}/>
      <button onClick={handleGenerateQuiz} disabled={loading}>{loading?'Generating...':'Generate Quiz'}</button>

      {quizData && (
        <div style={{marginTop:'20px'}}>
          <h2>{quizData.title}</h2>
          {quizData.quiz.map((q,idx)=>(
            <div key={idx} style={{border:'1px solid #ddd',padding:'10px',margin:'10px 0'}}>
              <p><b>Q{idx+1}:</b> {q.question}</p>
              <ul>{q.options.map((o,i)=><li key={i}>{o}</li>)}</ul>
              <p><b>Answer:</b> {q.answer}</p>
              <p><b>Explanation:</b> {q.explanation}</p>
              <p><b>Difficulty:</b> {q.difficulty}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
