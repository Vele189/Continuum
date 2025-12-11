import { useState, useEffect } from 'react';
import logo from '../assets/logo.png';

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? 'bg-white/90 backdrop-blur-md shadow-sm py-4' 
          : 'bg-white/50 backdrop-blur-sm py-6'
      }`}
    >
      <div className="container mx-auto px-6 flex items-center justify-between relative">
        {/* Hidden spacer to balance the flex layout if needed, or we use absolute centering */}
        <div className="hidden md:flex items-center gap-8 w-1/3">
          {['Features', 'About'].map((item) => (
            <a 
              key={item} 
              href={`#${item.toLowerCase()}`}
              className="text-sm font-medium transition-colors hover:text-primary-600 text-gray-600"
            >
              {item}
            </a>
          ))}
        </div>

        {/* Centralized Branding */}
        <div className="flex items-center gap-4 justify-center absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 md:static md:translate-x-0 md:translate-y-0 md:w-1/3 md:justify-center">
          <img src={logo} alt="Continuum Logo" className="h-16 md:h-20 w-auto drop-shadow-sm transition-all" />
          <span className="text-3xl md:text-5xl font-bold tracking-tighter text-gray-900 transition-all">
            Continuum
          </span>
        </div>

        <div className="flex items-center gap-4 w-1/3 justify-end">
          <a 
            href="#login" 
            className="hidden md:block text-sm font-medium transition-colors hover:text-primary-600 text-gray-900"
          >
            Log in
          </a>
          <button className="bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-full text-sm font-semibold transition-all shadow-lg hover:shadow-primary-500/25 cursor-pointer">
            Get Started
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
