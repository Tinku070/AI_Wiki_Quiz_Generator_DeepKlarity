import React, { useState } from 'react';
import GenerateQuizPage from './pages/GenerateQuizPage';
import HistoryPage from './pages/HistoryPage';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="app-container">
      <header className="header">
        <h1>DeepKlarity AI Wiki Quiz Generator</h1>
      </header>

      <div className="tabs">
        <button className={activeTab==='generate'?'tab-button active':'tab-button'} onClick={()=>setActiveTab('generate')}>TAB 1 - GENERATE QUIZ</button>
        <button className={activeTab==='history'?'tab-button active':'tab-button'} onClick={()=>setActiveTab('history')}>TAB 2 - HISTORY</button>
      </div>

      <div className="tab-content">
        {activeTab==='generate'?<GenerateQuizPage/>:<HistoryPage/>}
      </div>
    </div>
  );
}

export default App;
