
import { motion, AnimatePresence } from 'framer-motion';
import { Check } from 'lucide-react';

interface TaskCompletedCardProps {
    isVisible: boolean;
}

const TaskCompletedCard = ({ isVisible }: TaskCompletedCardProps) => {
    return (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.5, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.8, y: -20 }}
                    transition={{ type: "spring", stiffness: 400, damping: 25 }}
                    style={{
                        pointerEvents: 'none',
                        zIndex: 50,
                    }}
                    className="fixed top-32 left-1/2 -translate-x-1/2 flex items-center gap-3 px-5 py-3 bg-white/90 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/40"
                >
                    <div className="flex items-center justify-center w-8 h-8 bg-green-500 rounded-full shadow-lg shadow-green-500/30">
                        <motion.div
                            initial={{ pathLength: 0, opacity: 0 }}
                            animate={{ pathLength: 1, opacity: 1 }}
                            transition={{ duration: 0.3, delay: 0.2 }}
                        >
                            <Check className="w-5 h-5 text-white stroke-[3]" />
                        </motion.div>
                    </div>
                    <div>
                        <h3 className="text-sm font-bold text-gray-800 leading-tight">Task Completed</h3>
                        <p className="text-[10px] font-medium text-gray-500 uppercase tracking-wider">Vacuum Cleaned</p>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default TaskCompletedCard;
