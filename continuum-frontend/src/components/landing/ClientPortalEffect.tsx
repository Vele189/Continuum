import { AnimatePresence, motion } from 'framer-motion';
import { FileText, MessageSquare, CheckCircle2, CreditCard } from 'lucide-react';

interface ClientPortalEffectProps {
    isActive: boolean;
}

// Data for the left column (Invoices & Contracts)
const LEFT_ITEMS = [
    { id: 1, icon: CreditCard, label: "Invoice #1024 Paid", color: "bg-green-100 text-green-600" },
    { id: 2, icon: FileText, label: "Contract Signed", color: "bg-orange-100 text-orange-600" },
    { id: 3, icon: CreditCard, label: "Invoice #1025 Paid", color: "bg-green-100 text-green-600" },
    { id: 4, icon: FileText, label: "NDA Agreement", color: "bg-orange-100 text-orange-600" },
    { id: 5, icon: CreditCard, label: "Retainer Paid", color: "bg-green-100 text-green-600" },
    { id: 6, icon: FileText, label: "Proposal Accepted", color: "bg-orange-100 text-orange-600" },
];

// Data for the right column (Messages & Approvals)
const RIGHT_ITEMS = [
    { id: 1, icon: MessageSquare, label: "New Message", color: "bg-blue-100 text-blue-600" },
    { id: 2, icon: CheckCircle2, label: "Design Approved", color: "bg-purple-100 text-purple-600" },
    { id: 3, icon: MessageSquare, label: "Feedback Received", color: "bg-blue-100 text-blue-600" },
    { id: 4, icon: CheckCircle2, label: "Milestone Complete", color: "bg-purple-100 text-purple-600" },
    { id: 5, icon: MessageSquare, label: "Meeting Request", color: "bg-blue-100 text-blue-600" },
    { id: 6, icon: CheckCircle2, label: "Project Signed Off", color: "bg-purple-100 text-purple-600" },
];

const ScrollingColumn = ({ items, direction = "up", xPosition }: { items: typeof LEFT_ITEMS, direction?: "up" | "down", xPosition: string }) => {
    return (
        <div className={`absolute top-0 bottom-0 w-64 flex flex-col justify-center overflow-hidden pointer-events-none mask-gradient ${xPosition}`}>
            {/* Gradient masks for smooth fade in/out */}
            <div className="absolute inset-0 z-10 bg-gradient-to-b from-white via-transparent to-white pointer-events-none" />

            <motion.div
                className="flex flex-col gap-6 items-center"
                animate={{
                    y: direction === "up" ? [0, -500] : [-500, 0] // Approximate height based on items
                }}
                transition={{
                    duration: 20,
                    repeat: Infinity,
                    ease: "linear"
                }}
            >
                {/* Triple the items to ensure smooth loop without gaps */}
                {[...items, ...items, ...items].map((item, idx) => (
                    <div
                        key={`${item.id}-${idx}`}
                        className="bg-white/90 backdrop-blur-md px-4 py-3 rounded-xl shadow-lg flex items-center gap-3 border border-white/50 w-full transform transition-transform hover:scale-105"
                    >
                        <div className={`p-2 rounded-lg ${item.color}`}>
                            <item.icon size={20} />
                        </div>
                        <span className="font-medium text-gray-700 text-sm whitespace-nowrap">
                            {item.label}
                        </span>
                    </div>
                ))}
            </motion.div>
        </div>
    );
};

const ClientPortalEffect = ({ isActive }: ClientPortalEffectProps) => {
    return (
        <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
            <AnimatePresence>
                {isActive && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.5 }}
                        className="absolute inset-0"
                    >
                        {/* Left Column - Invoices & Contracts */}
                        <ScrollingColumn items={LEFT_ITEMS} direction="up" xPosition="left-[10%] md:left-[15%]" />

                        {/* Right Column - Messages & Approvals */}
                        <ScrollingColumn items={RIGHT_ITEMS} direction="down" xPosition="right-[10%] md:right-[15%]" />


                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ClientPortalEffect;
