import { motion } from 'framer-motion';
import React from 'react';

interface FlexibleTextProps {
    children: React.ReactNode;
    className?: string;
}

const FlexibleText: React.FC<FlexibleTextProps> = ({ children, className = '' }) => {
    return (
        <motion.span
            className={`inline-block cursor-default ${className}`}
            whileHover={{
                scaleX: 1.15,
                scaleY: 0.85,
                rotate: -2,
            }}
            transition={{
                type: 'spring',
                stiffness: 400,
                damping: 10,
                mass: 0.8,
            }}
        >
            {children}
        </motion.span>
    );
};

export default FlexibleText;
