import logo from '../../assets/logo.png';

const Hero = () => {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-white pt-20">
      {/* Background gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary-100/40 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-primary-50/40 blur-[120px] rounded-full" />
      </div>

      <div className="container mx-auto px-6 relative z-10 text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-gray-900 tracking-tight mb-8 leading-tight max-w-4xl mx-auto">
          The project management platform for <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-400">
             modern software teams
          </span>
        </h1>

        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
          Continuum is the all-in-one workspace where planning, execution, and collaboration meet. Stop toggling between apps and start shipping.
        </p>

        <div className="flex justify-center mb-12">
           <img src={logo} alt="Continuum Logo" className="h-24 w-auto drop-shadow-lg" />
        </div>
      </div>
    </section>
  );
};

export default Hero;

