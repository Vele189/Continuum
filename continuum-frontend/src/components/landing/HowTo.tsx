import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import signupImg from '../../assets/signup.png';
import loginImg from '../../assets/login.png';

const HowTo = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  const steps = [
    {
      image: signupImg,
      title: 'Create your account',
      description: 'Get started for free in seconds. No credit card required. Set up your profile and you\'re ready to go.',
      cta: 'Sign Up',
      link: '/register',
    },
    {
      image: loginImg,
      title: 'Start tracking work',
      description: 'Sign in to access your dashboard, create projects, and start logging your first work session.',
      cta: 'Log In',
      link: '/login',
    }
  ];

  return (
    <section id="get-started" className="py-24 bg-gray-50">
      <div className="container mx-auto px-6 max-w-5xl" ref={ref}>
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-light text-gray-900 mb-4 tracking-tight">
            Get started in minutes
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto font-light">
            No setup complexity, no learning curve. Start tracking your work immediately.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-16">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
              transition={{ delay: index * 0.2, duration: 0.6 }}
              className="bg-white border border-gray-200 p-8"
            >
              {/* Step Number */}
              <div className="text-sm text-gray-400 mb-6 font-medium tracking-wider">
                Step {index + 1}
              </div>

              {/* Image */}
              <div className="mb-8 bg-gray-50 flex items-center justify-center p-8 h-48">
                <img
                  src={step.image}
                  alt={step.title}
                  className="h-full w-auto object-contain opacity-80"
                />
              </div>

              {/* Content */}
              <h3 className="text-xl font-medium text-gray-900 mb-4">
                {step.title}
              </h3>
              <p className="text-gray-600 mb-8 leading-relaxed font-light">
                {step.description}
              </p>

              {/* CTA */}
              <Link
                to={step.link}
                className="group inline-flex items-center gap-2 text-gray-900 font-medium hover:text-gray-700 transition-colors"
              >
                {step.cta}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowTo;
