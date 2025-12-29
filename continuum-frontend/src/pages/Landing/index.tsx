import { Navbar, Hero, FAQ, Footer } from '../../components/landing';

const Landing = () => {
  return (
    <div
      className="min-h-screen font-sans text-gray-900 overflow-x-hidden relative"
      style={{
        background: 'linear-gradient(360deg, rgba(178, 230, 247, 0.2) 0%, rgba(253, 251, 247, 0.2) 100%), #F9FAFB'
      }}
    >
      <div className="relative z-10">
        <Navbar />
        <Hero />
        <FAQ />
        <Footer />
      </div>
    </div>
  );
};

export default Landing;
