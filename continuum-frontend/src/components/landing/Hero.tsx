import { motion, useMotionValue, useSpring } from 'framer-motion';
import { useEffect, useState } from 'react';
import GravityText from '../GravityText';

const Hero = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(true);

  // Smooth spring values for slime blob
  const cursorX = useMotionValue(0);
  const cursorY = useMotionValue(0);

  const springConfig = { damping: 15, stiffness: 100 };
  const x = useSpring(cursorX, springConfig);
  const y = useSpring(cursorY, springConfig);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const xPos = e.clientX;
      const yPos = e.clientY;

      setMousePosition({ x: xPos, y: yPos });
      cursorX.set(xPos - 64); // Center the blob (half of w-32 = 64px)
      cursorY.set(yPos - 64);
    };

    const handleMouseEnter = () => setIsHovering(true);
    const handleMouseLeave = () => setIsHovering(false);

    window.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseenter', handleMouseEnter);
    document.addEventListener('mouseleave', handleMouseLeave);

    // Initialize position
    cursorX.set(window.innerWidth / 2 - 64);
    cursorY.set(window.innerHeight / 2 - 64);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseenter', handleMouseEnter);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [cursorX, cursorY]);

  // Generate particles
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 3 + 1,
    opacity: Math.random() * 0.3 + 0.1,
  }));

  return (
    <section className="min-h-screen flex items-center justify-center bg-white pt-20 pb-20 relative overflow-hidden">
      {/* Slime blob that follows cursor */}
      <motion.div
        className="fixed pointer-events-none z-0"
        style={{
          x: x,
          y: y,
        }}
        initial={{ scale: 0, opacity: 0 }}
        animate={{
          scale: isHovering ? 1 : 0.6,
          opacity: isHovering ? 0.2 : 0.05,
        }}
        transition={{ duration: 0.4 }}
      >
        {/* Main slime blob */}
        <motion.div
          className="w-32 h-32"
          style={{
            background: 'radial-gradient(circle, rgba(107, 114, 128, 0.4) 0%, rgba(156, 163, 175, 0.2) 40%, rgba(209, 213, 219, 0.1) 70%, transparent 100%)',
            filter: 'blur(50px)',
            borderRadius: '50%',
          }}
          animate={{
            scale: [1, 1.3, 0.9, 1.1, 1],
            borderRadius: ['50%', '45% 55% 50% 60%', '55% 45% 60% 50%', '50% 50% 45% 55%', '50%'],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        {/* Secondary blob for more organic feel */}
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24"
          style={{
            background: 'radial-gradient(circle, rgba(75, 85, 99, 0.3) 0%, rgba(107, 114, 128, 0.15) 50%, transparent 80%)',
            filter: 'blur(35px)',
            borderRadius: '50%',
          }}
          animate={{
            x: [0, 15, -10, 5, 0],
            y: [0, -10, 15, -5, 0],
            scale: [1, 0.8, 1.2, 0.9, 1],
            borderRadius: ['50%', '60% 40%', '40% 60%', '50% 50%', '50%'],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        {/* Tertiary small blob */}
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16"
          style={{
            background: 'radial-gradient(circle, rgba(107, 114, 128, 0.25) 0%, transparent 70%)',
            filter: 'blur(25px)',
            borderRadius: '50%',
          }}
          animate={{
            x: [0, -12, 8, -5, 0],
            y: [0, 8, -12, 5, 0],
            scale: [1, 1.3, 0.7, 1.1, 1],
          }}
          transition={{
            duration: 3.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </motion.div>

      {/* Background particles that follow cursor */}
      <div className="absolute inset-0 pointer-events-none">
        {particles.map((particle) => {
          const offsetX = (mousePosition.x / window.innerWidth - 0.5) * 30;
          const offsetY = (mousePosition.y / window.innerHeight - 0.5) * 30;

          return (
            <motion.div
              key={particle.id}
              className="absolute rounded-full bg-gray-400"
              style={{
                left: `${particle.x}%`,
                top: `${particle.y}%`,
                width: `${particle.size}px`,
                height: `${particle.size}px`,
                opacity: particle.opacity,
              }}
              animate={{
                x: offsetX * (particle.id % 3 === 0 ? 0.5 : particle.id % 3 === 1 ? 0.3 : 0.7),
                y: offsetY * (particle.id % 3 === 0 ? 0.5 : particle.id % 3 === 1 ? 0.3 : 0.7),
              }}
              transition={{
                type: "spring",
                stiffness: 50,
                damping: 20,
              }}
            />
          );
        })}
      </div>

      {/* Curved background elements */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {/* Left side curve */}
        <motion.svg
          className="absolute left-0 top-1/2 -translate-y-1/2 w-96 h-96 opacity-5"
          viewBox="0 0 400 400"
          style={{
            x: (mousePosition.x / window.innerWidth - 0.5) * 50,
            y: (mousePosition.y / window.innerHeight - 0.5) * 50,
          }}
        >
          <path
            d="M0,200 Q100,100 200,150 T400,200"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="text-gray-400"
          />
        </motion.svg>

        {/* Right side curve */}
        <motion.svg
          className="absolute right-0 top-1/2 -translate-y-1/2 w-96 h-96 opacity-5"
          viewBox="0 0 400 400"
          style={{
            x: (mousePosition.x / window.innerWidth - 0.5) * -50,
            y: (mousePosition.y / window.innerHeight - 0.5) * 50,
          }}
        >
          <path
            d="M400,200 Q300,100 200,150 T0,200"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="text-gray-400"
          />
        </motion.svg>
      </div>

      <div className="container mx-auto px-6 max-w-4xl relative z-10">
        <motion.div
          className="text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.6, -0.05, 0.01, 0.99] }}
        >
          {/* Main Heading */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-light text-gray-900 tracking-tight mb-6 leading-tight">
            <GravityText text="Project management" className="justify-center" />
            <br />
            <span className="font-normal text-gray-800">for freelancers</span>
          </h1>

          {/* Subheading */}
          <p className="text-lg md:text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed font-light">
            Track work, log hours, manage tasks, and generate invoices—all in one place.
          </p>

          {/* Trust divider */}
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="h-px w-16 bg-gray-200" />
            <span className="text-xs text-gray-400 uppercase tracking-wider font-medium">Trusted by teams worldwide</span>
            <div className="h-px w-16 bg-gray-200" />
          </div>

          {/* Feature list */}
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500">
            <span>Time Tracking</span>
            <span className="text-gray-300">•</span>
            <span>Task Management</span>
            <span className="text-gray-300">•</span>
            <span>Auto Invoicing</span>
            <span className="text-gray-300">•</span>
            <span>Client Portal</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
