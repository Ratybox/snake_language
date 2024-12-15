// frontend/src/components/LexicalAnalysis.js
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const LexicalAnalysis = ({ tokens }) => {
    if (!tokens) return null;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="lexical-analysis"
        >
            <h2>Lexical Analysis Results</h2>
            <div className="tokens-container">
                <AnimatePresence>
                    {tokens.map((token, index) => (
                        <motion.div
                            key={index}
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            exit={{ x: 20, opacity: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className={`token-item ${token.type.toLowerCase()}`}
                        >
                            <span className="token-type">{token.type}</span>
                            <span className="token-value">{token.value}</span>
                            <span className="token-line">Line: {token.line}</span>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </motion.div>
    );
};

export default LexicalAnalysis;