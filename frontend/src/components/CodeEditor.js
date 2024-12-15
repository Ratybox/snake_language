// frontend/src/components/CodeEditor.js
import React, { useState } from 'react';
import LexicalAnalysis from './LexicalAnalysis';
import SyntaxAnalysis from './SyntaxAnalysis';
import SemanticAnalysis from './SemanticAnalysis';
import { motion } from 'framer-motion';

const CodeEditor = () => {
    const [code, setCode] = useState('');
    const [result, setResult] = useState(null);

    const analyzeCode = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/compile/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            });
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Error:', error);
            setResult({
                success: false,
                errors: [error.message]
            });
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="code-editor-container"
        >
            <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter your SNAKE code here..."
                rows={10}
                cols={50}
            />
            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={analyzeCode}
            >
                Analyze Code
            </motion.button>

            {result && (
                <div className="analysis-results">
                    {result.errors && result.errors.length > 0 && (
                        <div className="errors">
                            <h3>Errors:</h3>
                            {result.errors.map((error, index) => (
                                <div key={index} className="error-message">
                                    {error}
                                </div>
                            ))}
                        </div>
                    )}
                    
                    {result.lexical_analysis && (
                        <LexicalAnalysis tokens={result.lexical_analysis} />
                    )}
                    
                    {result.syntax_analysis && (
                        <SyntaxAnalysis analysis={result.syntax_analysis} />
                    )}
                    
                    {result.semantic_analysis && (
                        <SemanticAnalysis analysis={result.semantic_analysis} />
                    )}
                </div>
            )}
        </motion.div>
    );
};

export default CodeEditor;