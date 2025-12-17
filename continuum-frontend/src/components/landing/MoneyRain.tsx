import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState, useRef } from 'react';

interface MoneyRainProps {
    isActive: boolean;
}

interface MoneyParticle {
    id: number;
    x: number;
    rotation: number;
    duration: number;
    delay: number;
}

const MoneyRain = ({ isActive }: MoneyRainProps) => {
    const [items, setItems] = useState<MoneyParticle[]>([]);
    const idCounter = useRef(0);

    useEffect(() => {
        let interval: NodeJS.Timeout;

        if (isActive) {
            // Spawn a new particle every 100ms
            interval = setInterval(() => {
                const id = idCounter.current++;
                const newItem: MoneyParticle = {
                    id,
                    x: Math.random() * window.innerWidth, // Random horizontal start
                    rotation: Math.random() * 360, // Random initial rotation
                    duration: Math.random() * 2 + 1.5, // Fall duration between 1.5s and 3.5s
                    delay: 0,
                };

                setItems((prev) => [...prev, newItem]);

                // Cleanup this specific item after it falls to prevent memory leak
                // (Though AnimatePresence handles exit, we need to remove from state loop)
                setTimeout(() => {
                    setItems((prev) => prev.filter((item) => item.id !== id));
                }, newItem.duration * 1000 + 100);

            }, 100);
        } else {
            // If inactive, let existing ones fall but stop spawning
            // Optional: Clear immediately if we want instant stop? 
            // User said "rain from top", implies nice transition. 
            // Let's stop spawning.
        }

        return () => clearInterval(interval);
    }, [isActive]);

    return (
        <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
            <AnimatePresence>
                {items.map((item) => (
                    <motion.img
                        key={item.id}
                        src="/dollar_4286172.png"
                        alt="Money"
                        className="absolute w-8 h-8 object-contain opacity-80"
                        initial={{
                            y: -50,
                            x: item.x,
                            rotate: item.rotation,
                            opacity: 0,
                        }}
                        animate={{
                            y: window.innerHeight + 50,
                            rotate: item.rotation + 360, // Spin as it falls
                            opacity: 1,
                        }}
                        exit={{ opacity: 0 }}
                        transition={{
                            duration: item.duration,
                            ease: "linear",
                        }}
                    />
                ))}
            </AnimatePresence>
        </div>
    );
};

export default MoneyRain;
