import { useState } from 'react';
import { Navbar, Hero } from '../../components/landing';
import CursorGravity from '../../components/CursorGravity';
import CustomCursor from '../../components/CustomCursor';

const Landing = () => {
  const [isVacuumActive, setIsVacuumActive] = useState(false);

  return (
    <div className="min-h-screen bg-white font-sans text-gray-900 overflow-x-hidden relative">
      <CursorGravity isVacuumActive={isVacuumActive} />
      <CustomCursor isVacuumActive={isVacuumActive} />
      <div className="relative z-10">
        <Navbar />
        <Hero onVacuumStateChange={setIsVacuumActive} />
      </div>
    </div>
  );
};

export default Landing;
