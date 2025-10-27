import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Modal from 'react-modal';

Modal.setAppElement('#root');

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const fetchHistory = async ()=>{
      const res = await axios.get('http://localhost:8000/history/');
      setHistory(res.data);
    }
    fetchHistory();
  }, []);

  const openModal = (quiz) => { setSelectedQuiz(quiz); setModalOpen(true); }
  const closeModal = () => { setSelectedQuiz(null); setModalOpen(false); }

  return (
    <div>
      <table border="1" cellPadding="10" style={{width:'100%',borderCollapse:'collapse'}}>
        <thead><tr><th>ID</th><th>Title</th><th>URL</th><th>Actions</th></tr></thead>
        <tbody>
          {history.map(item=>(
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.title}</td>
              <td>{item.url}</td>
              <td><button onClick={()=>openModal(item)}>Details</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      <Modal isOpen={modalOpen} onRequestClose={closeModal} contentLabel="Quiz Details"
        style={{content:{top:'50%',left:'50%',right:'auto',bottom:'auto',transform:'translate(-50%,-50%)',width:'80%',maxHeight:'80%',overflowY:'auto',padding:'20px',borderRadius:'10px'}}}>
        <button onClick={closeModal} style={{float:'right'}}>Close</button>
        {selectedQuiz && (
          <div>
            <h2>{selectedQuiz.title}</h2>
            {selectedQuiz.quiz.map((q,idx)=>(
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
      </Modal>
    </div>
  );
}
