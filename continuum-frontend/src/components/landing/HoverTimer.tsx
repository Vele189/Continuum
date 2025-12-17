import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect, useRef } from 'react';

interface HoverTimerProps {
    isActive: boolean;
}

const HoverTimer = ({ isActive }: HoverTimerProps) => {
    const [time, setTime] = useState(0);
    const startTimeRef = useRef<number | null>(null);
    const requestRef = useRef<number | null>(null);

    useEffect(() => {
        if (isActive) {
            startTimeRef.current = Date.now();

            const animate = () => {
                if (startTimeRef.current) {
                    setTime(Date.now() - startTimeRef.current);
                    requestRef.current = requestAnimationFrame(animate);
                }
            };

            requestRef.current = requestAnimationFrame(animate);
        } else {
            if (requestRef.current) {
                cancelAnimationFrame(requestRef.current);
            }
            // Use setTimeout to avoid synchronous setState in effect
            const timer = setTimeout(() => {
                setTime(0);
                startTimeRef.current = null;
            }, 0);
            return () => clearTimeout(timer);
        }

        return () => {
            if (requestRef.current) {
                cancelAnimationFrame(requestRef.current);
            }
        };
    }, [isActive]);

    const formatTime = (ms: number) => {
        const hours = Math.floor(ms / 3600000);
        const minutes = Math.floor((ms % 3600000) / 60000);
        const seconds = Math.floor((ms % 60000) / 1000);
        const milliseconds = Math.floor((ms % 1000) / 10);

        const pad = (n: number) => n.toString().padStart(2, '0');

        // Matching the format in the image but ensuring all parts are used
        return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}:${pad(milliseconds)}`;
    };

    return (
        <AnimatePresence>
            {isActive && (
                <motion.div
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: 100, opacity: 0 }}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                    className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 flex items-center gap-6 px-8 py-4 bg-gray-200/80 backdrop-blur-md rounded-full shadow-lg border border-white/20"
                >
                    <span className="font-mono text-4xl font-medium tracking-wider text-[#8B0000]">
                        {formatTime(time)}
                    </span>
                    <div className="w-12 h-12 bg-[#8B0000] rounded-full flex items-center justify-center shadow-lg">
                        <div className="w-4 h-4 bg-white rounded-sm" />
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default HoverTimer;
