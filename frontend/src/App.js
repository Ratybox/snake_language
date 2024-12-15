// src/App.js
import React from 'react';
import CodeEditor from './components/CodeEditor';
import './styles/LexicalAnalysis.css';

function App() {
    return (
        <div className="App">
            <h1>SNAKE Language Compiler</h1>
            <CodeEditor />
        </div>
    );
}

export default App;