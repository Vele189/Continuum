import { Navbar, Hero, HowTo, TargetAudience, Features, Footer } from '../../components/landing';

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
