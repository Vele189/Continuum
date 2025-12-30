

const Loading = () => {
  return (
    <div className="relative flex justify-center items-center min-h-screen p-10 overflow-hidden bg-gradient-to-b from-brand-blue to-brand-cream">
      {/* Loading Content Container - 354x84px */}
      <div className="w-[354px] h-[84px] flex flex-col items-center gap-[19.38px]">
        {/* Continuum Logo with Flash Animation - 354x60px */}
        <img 
          src="Wordmark_colour.svg" 
          alt="Continuum Logo" 
          className="w-[354px] h-[60px] animate-pulse-soft"
        />
        
        {/* Subtitle with Flash Animation - 235x24px */}
        <p className="w-[235px] h-6 font-sathu font-normal text-[19.38px] leading-[100%] tracking-[-0.19px] text-center text-[#045980] opacity-80 m-0 animate-pulse-soft animation-delay-200">
          Time track with one click...
        </p>
      </div>

      <style>{`
        @keyframes pulse-soft {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.4;
          }
        }
        
        .animate-pulse-soft {
          animation: pulse-soft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        .animation-delay-200 {
          animation-delay: 0.2s;
        }
      `}</style>
    </div>
  );
};

export default Loading;