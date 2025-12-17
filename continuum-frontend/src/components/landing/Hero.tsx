import { motion, useMotionValue, useSpring } from 'framer-motion';
import { useEffect, useState } from 'react';
import GravityText from '../GravityText';
import FlexibleText from './FlexibleText';
import HoverTimer from './HoverTimer';
import MoneyRain from './MoneyRain';
import ClientPortalEffect from './ClientPortalEffect';

// Generate particles outside the component to avoid impure function calls during render
const generateParticles = () =>
  Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 6 + 2, // Increased size: 2 to 8px
    opacity: Math.random() * 0.3 + 0.1,
    splashX: (Math.random() - 0.5) * 300, // Random splash direction X
    splashY: (Math.random() - 0.5) * 300, // Random splash direction Y
    vacuumOffsetX: (Math.random() - 0.5) * 30, // Random offset when vacuumed
    vacuumOffsetY: (Math.random() - 0.5) * 30, // Random offset when vacuumed
  }));

interface HeroProps {
  onVacuumStateChange?: (isActive: boolean) => void;
}

const Hero = ({ onVacuumStateChange }: HeroProps) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(true);
  const [isTimeTrackingHovered, setIsTimeTrackingHovered] = useState(false);
  const [isTaskManagementHovered, setIsTaskManagementHovered] = useState(false);
  const [isAutoInvoicingHovered, setIsAutoInvoicingHovered] = useState(false);
  const [isClientPortalHovered, setIsClientPortalHovered] = useState(false);

  // Update global vacuum state when local hover state changes
  useEffect(() => {
    onVacuumStateChange?.(isTaskManagementHovered);
  }, [isTaskManagementHovered, onVacuumStateChange]);

  const [isSplashing, setIsSplashing] = useState(false);
  // Track previous hover state to detect release
  const [wasTaskManagementHovered, setWasTaskManagementHovered] = useState(false);

  useEffect(() => {
    if (!isTaskManagementHovered && wasTaskManagementHovered) {
      setIsSplashing(true);
      const timer = setTimeout(() => setIsSplashing(false), 500); // Splash duration
      return () => clearTimeout(timer);
    }
    setWasTaskManagementHovered(isTaskManagementHovered);
  }, [isTaskManagementHovered]);

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

  // Use lazy state initialization to generate particles only once
  const [particles] = useState(generateParticles);

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
          scale: isTaskManagementHovered ? 2.5 : isHovering ? 1 : 0.6,
          opacity: isTaskManagementHovered ? 0.4 : isHovering ? 0.2 : 0.05,
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
          // Standard parallax offset
          const parallaxX = (mousePosition.x / window.innerWidth - 0.5) * 30;
          const parallaxY = (mousePosition.y / window.innerHeight - 0.5) * 30;

          // Vacuum offset: Calculate difference between mouse position and particle origin
          // Particle origin in pixels approx:
          const originX = (particle.x / 100) * window.innerWidth;
          const originY = (particle.y / 100) * window.innerHeight;

          const vacuumDeltaX = mousePosition.x - originX;
          const vacuumDeltaY = mousePosition.y - originY;

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
                x: isTaskManagementHovered ? vacuumDeltaX + (particle as any).vacuumOffsetX
                  : isSplashing ? vacuumDeltaX + (particle as any).splashX
                    : parallaxX * (particle.id % 3 === 0 ? 0.5 : particle.id % 3 === 1 ? 0.3 : 0.7),
                y: isTaskManagementHovered ? vacuumDeltaY + (particle as any).vacuumOffsetY
                  : isSplashing ? vacuumDeltaY + (particle as any).splashY
                    : parallaxY * (particle.id % 3 === 0 ? 0.5 : particle.id % 3 === 1 ? 0.3 : 0.7),
                scale: isTaskManagementHovered ? 0.6 : 1, // Stay visible but smaller
              }}
              transition={{
                type: isSplashing ? "tween" : "spring",
                ease: isSplashing ? "easeOut" : undefined,
                duration: isSplashing ? 0.4 : undefined,
                stiffness: isTaskManagementHovered ? 20 : 50, // Much lower stiffness for slower movement
                damping: isTaskManagementHovered ? 15 : 20, // Lower damping
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

      <MoneyRain isActive={isAutoInvoicingHovered} />
      <ClientPortalEffect isActive={isClientPortalHovered} />
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
            <span className="font-normal text-gray-800">
              for&nbsp;<FlexibleText>freelancers</FlexibleText>
            </span>
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
            <span
              className="cursor-default transition-colors hover:text-gray-900"
              onMouseEnter={() => setIsTimeTrackingHovered(true)}
              onMouseLeave={() => setIsTimeTrackingHovered(false)}
            >
              Time Tracking
            </span>
            <span className="text-gray-300">•</span>
            <span
              className="cursor-none transition-colors hover:text-gray-900"
              onMouseEnter={() => setIsTaskManagementHovered(true)}
              onMouseLeave={() => setIsTaskManagementHovered(false)}
            >
              Task Management
            </span>
            <span className="text-gray-300">•</span>
            <span
              className="relative inline-block cursor-default transition-colors hover:text-gray-900"
              onMouseEnter={() => setIsAutoInvoicingHovered(true)}
              onMouseLeave={() => setIsAutoInvoicingHovered(false)}
            >
              Auto Invoicing
            </span>
            <span className="text-gray-300">•</span>
            <span
              className="cursor-default transition-colors hover:text-gray-900"
              onMouseEnter={() => setIsClientPortalHovered(true)}
              onMouseLeave={() => setIsClientPortalHovered(false)}
            >
              Client Portal
            </span>
          </div>
        </motion.div>
      </div>

      <HoverTimer isActive={isTimeTrackingHovered || isAutoInvoicingHovered} />
    </section>
  );
};

export default Hero;
