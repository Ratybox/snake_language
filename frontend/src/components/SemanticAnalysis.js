import React from 'react';
import { motion } from 'framer-motion';

const SemanticAnalysis = ({ analysis }) => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="semantic-analysis"
        >
            <h2>Semantic Analysis</h2>
            <div className="semantic-container">
                <h3>Symbol Table:</h3>
                <pre>{JSON.stringify(analysis.symbol_table, null, 2)}</pre>
                <h3>Type Checking:</h3>
                <p>{analysis.type_checking}</p>
                <h3>Scope Analysis:</h3>
                <p>{analysis.scope_analysis}</p>
            </div>
        </motion.div>
    );
};

export default SemanticAnalysis;
