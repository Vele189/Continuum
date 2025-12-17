import { Navbar, Hero } from '../../components/landing';
import CursorGravity from '../../components/CursorGravity';

const Landing = () => {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900 overflow-x-hidden relative">
      <CursorGravity />
      <div className="relative z-10">
        <Navbar />
        <Hero />
      </div>
    </div>
  );
};

export default Landing;
