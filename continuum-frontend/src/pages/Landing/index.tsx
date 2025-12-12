import Navbar from '../../components/Navbar';
import Hero from '../../components/Hero';
import TargetAudience from '../../components/TargetAudience';
import Features from '../../components/Features';
import HowTo from '../../components/HowTo';
import Footer from '../../components/Footer';

const Landing = () => {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900">
      <Navbar />
      <main className="pt-28">
        <Hero />
        <HowTo />
        <TargetAudience />
        <Features />
      </main>
      <Footer />
    </div>
  );
};

export default Landing;

