import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import TiltCard from '../TiltCard';

const Features = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  const features = [
    {
      title: 'Automatic Time Tracking',
      description: 'Start and stop work sessions directly in tasks. Hours are captured automatically and tied to the correct project.',
    },
    {
      title: 'Smart Invoice Generation',
      description: 'One-click PDF invoices showing hours worked, tasks completed, commits linked, and milestones reached.',
    },
    {
      title: 'Git Integration',
      description: 'Automatically link commits to tasks. Track contributions per team member and maintain a clean record of what was shipped.',
    },
    {
      title: 'Client Portal',
      description: 'Give clients transparent access to project progress, completed tasks, hours logged, and milestone updates.',
    },
    {
      title: 'Project Health Indicators',
      description: 'Clear signals when tasks fall behind, alerts for inactive projects, and visual summaries showing overall progress.',
    },
    {
      title: 'AI-Powered Summaries',
      description: 'Automatic weekly summaries using actual data from tasks, commits, and hours. Clean, factual summaries for client updates.',
    }
  ];

  return (
    <section id="features" className="py-24 bg-white">
      <div className="container mx-auto px-6 max-w-6xl" ref={ref}>
        {/* Section Header */}
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-light text-gray-900 mb-4 tracking-tight">
            Everything you need
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto font-light">
            One platform that combines project management, time tracking, invoicing, and client communication.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
          {features.map((feature, index) => (
            <TiltCard key={index} className="h-full">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                className="border-t border-gray-200 pt-6 h-full p-4 hover:bg-gray-50/50 rounded-xl transition-colors" // Added padding and hover bg
              >
                <h3 className="text-lg font-medium text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed font-light">
                  {feature.description}
                </p>
              </motion.div>
            </TiltCard>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
