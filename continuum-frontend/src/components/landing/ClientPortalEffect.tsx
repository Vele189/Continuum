import { AnimatePresence, motion } from 'framer-motion';
import { FileText, MessageSquare, CheckCircle2, User, CreditCard } from 'lucide-react';
import { useEffect, useState } from 'react';

interface ClientPortalEffectProps {
    isActive: boolean;
}

interface PortalCardData {
    id: number;
    x: number;
    y: number;
    rotation: number;
    scale: number;
    icon: React.ElementType;
    label: string;
    color: string;
    delay: number;
}

const ClientPortalEffect = ({ isActive }: ClientPortalEffectProps) => {
    const [cards, setCards] = useState<PortalCardData[]>([]);

    useEffect(() => {
        if (isActive) {
            // Generate set of cards to display
            const newCards: PortalCardData[] = [
                {
                    id: 1,
                    x: 20,
                    y: 30,
                    rotation: -10,
                    scale: 1,
                    icon: CreditCard,
                    label: "Invoice Paid",
                    color: "bg-green-100 text-green-600",
                    delay: 0
                },
                {
                    id: 2,
                    x: 70,
                    y: 20,
                    rotation: 15,
                    scale: 0.9,
                    icon: MessageSquare,
                    label: "New Message",
                    color: "bg-blue-100 text-blue-600",
                    delay: 0.1
                },
                {
                    id: 3,
                    x: 15,
                    y: 60,
                    rotation: 5,
                    scale: 1.1,
                    icon: FileText,
                    label: "Contract.pdf",
                    color: "bg-orange-100 text-orange-600",
                    delay: 0.2
                },
                {
                    id: 4,
                    x: 80,
                    y: 70,
                    rotation: -8,
                    scale: 0.95,
                    icon: CheckCircle2,
                    label: "Approved",
                    color: "bg-purple-100 text-purple-600",
                    delay: 0.15
                },
                {
                    id: 5,
                    x: 45,
                    y: 85, // Bottom center
                    rotation: 0,
                    scale: 1.2,
                    icon: User,
                    label: "Client Login",
                    color: "bg-gray-100 text-gray-800",
                    delay: 0.3
                }
            ];
            setCards(newCards);
        } else {
            // Optional: clear cards or let them exit via AnimatePresence
        }
    }, [isActive]);

    return (
        <div className="fixed inset-0 pointer-events-none z-40 overflow-hidden">
            <AnimatePresence>
                {isActive && cards.map((card) => (
                    <motion.div
                        key={card.id}
                        initial={{
                            opacity: 0,
                            y: window.innerHeight, // Start from bottom
                            x: (card.x / 100) * window.innerWidth,
                            scale: 0.5,
                            rotate: 0
                        }}
                        animate={{
                            opacity: 1,
                            y: (card.y / 100) * window.innerHeight,
                            x: (card.x / 100) * window.innerWidth,
                            scale: card.scale,
                            rotate: card.rotation
                        }}
                        exit={{
                            opacity: 0,
                            scale: 0,
                            y: (card.y / 100) * window.innerHeight - 100 // Float up when disappearing
                        }}
                        transition={{
                            type: "spring",
                            damping: 12,
                            stiffness: 100,
                            delay: card.delay
                        }}
                        className="absolute"
                    >
                        <div className="bg-white/90 backdrop-blur-md px-4 py-3 rounded-xl shadow-xl flex items-center gap-3 border border-white/50">
                            <div className={`p-2 rounded-lg ${card.color}`}>
                                <card.icon size={20} />
                            </div>
                            <span className="font-medium text-gray-700 text-sm whitespace-nowrap">
                                {card.label}
                            </span>
                        </div>
                    </motion.div>
                ))}
            </AnimatePresence>
        </div>
    );
};

export default ClientPortalEffect;
