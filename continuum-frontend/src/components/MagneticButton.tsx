import { useRef, useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface MagneticButtonProps {
    children: React.ReactNode;
    className?: string;
    onClick?: () => void;
    range?: number;
    strength?: number;
    disabled?: boolean;
}

const MagneticButton = ({
    children,
    className = '',
    onClick,
    range = 100, // Default range in pixels
    strength = 0.5, // Default strength multiplier
    disabled = false
}: MagneticButtonProps) => {
    const ref = useRef<HTMLDivElement>(null);
    const [position, setPosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        if (disabled) {
            setPosition({ x: 0, y: 0 });
            return;
        }

        const handleMouseMove = (e: MouseEvent) => {
            if (!ref.current) return;

            const { clientX, clientY } = e;
            const { height, width, left, top } = ref.current.getBoundingClientRect();

            const centerX = left + width / 2;
            const centerY = top + height / 2;

            const distance = Math.sqrt(
                Math.pow(clientX - centerX, 2) + Math.pow(clientY - centerY, 2)
            );

            if (distance < range) {
                // Determine how much to move based on distance relative to range
                // Optional: add ease-in/out based on distance? 
                // For now, keep it simple as proportional to offset like before, 
                // but limited by the range check.

                const x = (clientX - centerX) * strength;
                const y = (clientY - centerY) * strength;
                setPosition({ x, y });
            } else {
                setPosition({ x: 0, y: 0 });
            }
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, [range, strength, disabled]);

    const { x, y } = position;

    return (
        <motion.div
            ref={ref}
            animate={{ x, y }}
            transition={{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }}
            className={`inline-block ${className}`}
            onClick={onClick}
        >
            {children}
        </motion.div>
    );
};

export default MagneticButton;
