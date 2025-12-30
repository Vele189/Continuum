

const Footer = () => {
  const footerLinks = {
    Product: [
      { label: 'Features', href: '#features' },
      { label: 'User Manual', href: '#' },
    ],
    Company: [
      { label: 'About', href: '#audience' },
      { label: 'Contact', href: '#' },
    ],
    Legal: [
      { label: 'Privacy', href: '#' },
      { label: 'Terms', href: '#' },
      { label: 'Security', href: '#' },
    ],
  };

  return (
    <footer className="bg-white border-t border-gray-200 pt-16 pb-8">
      <div className="container mx-auto px-6 max-w-7xl">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-12 mb-12">
          {/* Brand Section */}
          <div className="col-span-2 lg:col-span-2">
            <span style={{
              fontFamily: 'Sarina',
              fontWeight: 400,
              fontSize: '24px',
              background: 'linear-gradient(99.31deg, #24B5F8 4.62%, #5521FE 148.53%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              color: 'transparent',
              display: 'inline-block',
              marginBottom: '1rem'
            }}>
              Continuum
            </span>
            <p className="text-gray-600 text-sm leading-relaxed max-w-sm font-light" style={{ fontFamily: 'Satoshi' }}>
              The project management platform for teams that want to ship software faster and with fewer meetings.
            </p>
          </div>

          {/* Links Sections */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="text-sm font-medium text-gray-900 mb-4" style={{ fontFamily: 'Satoshi' }}>{category}</h4>
              <ul className="space-y-3 text-sm">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      onClick={(e) => {
                        if (link.href.startsWith('#')) {
                          e.preventDefault();
                          const element = document.querySelector(link.href);
                          if (element) {
                            element.scrollIntoView({ behavior: 'smooth' });
                          }
                        }
                      }}
                      className="text-gray-600 hover:text-gray-900 transition-colors font-light"
                      style={{ fontFamily: 'Satoshi' }}
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-200 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <p className="font-light" style={{ fontFamily: 'Satoshi' }}>&copy; {new Date().getFullYear()} Continuum Inc. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <a href="#" className="hover:text-gray-900 transition-colors font-light" style={{ fontFamily: 'Satoshi' }}>
              GitHub
            </a>
            <a href="#" className="hover:text-gray-900 transition-colors font-light" style={{ fontFamily: 'Satoshi' }}>
              LinkedIn
            </a>
          </div>
        </div>
      </div>


    </footer>
  );
};

export default Footer;
