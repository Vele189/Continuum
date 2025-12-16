import { motion } from 'framer-motion';

interface GravityTextProps {
    text: string;
    className?: string;
}

const GravityText = ({ text, className = '' }: GravityTextProps) => {
    return (
        <div className={`flex flex-wrap ${className}`}>
            {text.split(" ").map((word, i) => (
                <Word key={i} word={word} />
            ))}
        </div>
    );
};

const Word = ({ word }: { word: string }) => {
    return (
        <span className="inline-block mr-2 whitespace-nowrap">
            {word.split("").map((char, i) => (
                <Char key={i} char={char} />
            ))}
        </span>
    )
}

const Char = ({ char }: { char: string }) => {
    // Random jitter on hover or distance?
    // Let's do a simple "shudder" away from cursor.

    // For now, let's keep it simple: individual characters have a springy response to hover

    return (
        <motion.span
            className="inline-block"
            whileHover={{
                y: -5,
                scale: 1.2,
                color: "#4f46e5", // Indigo-600
                transition: { type: "spring", stiffness: 300 }
            }}
            style={{ position: 'relative' }}
        >
            {char}
        </motion.span>
    )
}


export default GravityText;
