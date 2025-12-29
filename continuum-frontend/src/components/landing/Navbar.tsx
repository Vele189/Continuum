import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';


const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { label: 'Focus', href: '#deep-work' },
    { label: 'Method', href: '#methodology' },
    { label: 'Invoice', href: '#invoicing' },
    { label: 'Clients', href: '#clients' },
    { label: 'FAQ', href: '#faq' },
  ];

  const handleNavClick = (href: string) => {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.4 }}
      className="absolute top-0 left-0 right-0 z-50 transition-all duration-200 bg-transparent py-6"
    >
      <div className="container mx-auto px-6 flex items-center justify-between max-w-7xl">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3">
          <span style={{
            fontFamily: 'Sarina',
            fontWeight: 400,
            fontSize: '21.41px',
            lineHeight: '24px',
            letterSpacing: '-0.02em',
            color: '#0B191F'
          }}>
            Continuum
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <a
              key={item.label}
              href={item.href}
              onClick={(e) => {
                e.preventDefault();
                handleNavClick(item.href);
              }}
              className="transition-colors"
              style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontSize: '16px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#606D76'
              }}
            >
              {item.label}
            </a>
          ))}
        </div>

        {/* Right Side */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Link
              to="/login"
              className="flex items-center justify-center transition-all duration-200 hover:scale-105"
              style={{
                width: '67px',
                height: '32px',
                background: '#FFFFFF',
                border: '1px solid #EDEDED',
                borderRadius: '8px',
                padding: '8px 16px',
                boxShadow: `
                  0px 1px 1px 0px #0E0E2208,
                  0px 2px 1px 0px #0E0E2205,
                  0px 3px 1px 0px #0E0E2203,
                  0px 5px 1px 0px #0E0E2200
                `
              }}
            >
              <span style={{
                fontFamily: 'Satoshi',
                fontWeight: 500,
                fontSize: '14px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#0B191F'
              }}>
                Login
              </span>
            </Link>

            <Link
              to="/register"
              className="flex items-center justify-center transition-all duration-200"
              style={{
                minWidth: '84px',
                height: '32px',
                background: 'linear-gradient(141.68deg, #24B5F8 -123.02%, #5521FE 802.55%)',
                border: '1px solid #FFFFFF1A',
                borderRadius: '8px',
                padding: '8px 16px',
                whiteSpace: 'nowrap',
                boxShadow: `
                  0px 0px 1px 0px #2D9AF936,
                  0px 2px 2px 0px #2D9AF930,
                  0px 4px 3px 0px #2D9AF91C,
                  0px 8px 3px 0px #2D9AF908,
                  0px 12px 3px 0px #2D9AF900
                `
              }}
            >
              <span style={{
                fontFamily: 'Satoshi',
                fontWeight: 700,
                fontSize: '14px',
                lineHeight: '100%',
                letterSpacing: '0%',
                color: '#FFFFFF'
              }}>
                Sign Up
              </span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 text-gray-600 hover:text-gray-900 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden bg-white border-t border-gray-200"
        >
          <div className="container mx-auto px-6 py-6 space-y-4">
            {navItems.map((item) => (
              <a
                key={item.label}
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick(item.href);
                }}
                className="block text-base text-gray-600 hover:text-gray-900 transition-colors py-2"
              >
                {item.label}
              </a>
            ))}
            <div className="pt-4 border-t border-gray-200 space-y-3">
              <Link
                to="/login"
                className="block text-center py-2 text-gray-600 hover:text-gray-900 transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Log in
              </Link>
              <Link
                to="/register"
                className="block text-center py-2 bg-gray-900 text-white transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Get Started
              </Link>
            </div>
          </div>
        </motion.div>
      )}
    </motion.nav>
  );
};

export default Navbar;
