import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

const TargetAudience = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  const audiences = [
    {
      title: 'Engineering Teams',
      description: 'Track sprints, manage bugs, and link code to tasks seamlessly. See exactly what your team is working on and when it ships.',
    },
    {
      title: 'Product Managers',
      description: 'Get visibility into roadmaps and progress without nagging engineers. Real-time updates and automated status reports.',
    },
    {
      title: 'Freelancers & Startups',
      description: 'Scale from your first MVP to global enterprise. One tool that grows with you, from solo freelancer to full team.',
    }
  ];

  return (
    <section id="audience" className="py-24 bg-white">
      <div className="container mx-auto px-6 max-w-5xl" ref={ref}>
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-light text-gray-900 mb-4 tracking-tight">
            Built for modern teams
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto font-light">
            Whether you're a solo freelancer or a growing team, Continuum adapts to your workflow.
          </p>
        </motion.div>

        {/* Audience Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {audiences.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              className="border-t border-gray-200 pt-6"
            >
              <h3 className="text-lg font-medium text-gray-900 mb-3">
                {item.title}
              </h3>
              <p className="text-gray-600 leading-relaxed font-light">
                {item.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TargetAudience;
