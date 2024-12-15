import React from 'react';
import { motion } from 'framer-motion';

const SyntaxAnalysis = ({ analysis }) => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="syntax-analysis"
        >
            <h2>Syntax Analysis</h2>
            <div className="ast-container">
                <h3>Abstract Syntax Tree:</h3>
                <pre>{JSON.stringify(analysis.ast, null, 2)}</pre>
                <h3>Structure:</h3>
                <ul>
                    {analysis.structure.map((item, index) => (
                        <li key={index}>{item}</li>
                    ))}
                </ul>
            </div>
        </motion.div>
    );
};

export default SyntaxAnalysis;
