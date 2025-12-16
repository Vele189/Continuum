import { Code2, MonitorPlay, Rocket } from 'lucide-react';

const TargetAudience = () => {
  const audiences = [
    {
      icon: <Code2 className="w-8 h-8 text-white relative z-10" />,
      title: 'Engineering Teams',
      description: 'Who need to track sprints, manage bugs, and link code to tasks seamlessly.'
    },
    {
      icon: <Rocket className="w-8 h-8 text-white relative z-10" />,
      title: 'Product Managers',
      description: 'Who need visibility into roadmaps and progress without nagging engineers.'
    },
    {
      icon: <MonitorPlay className="w-8 h-8 text-white relative z-10" />,
      title: 'Startups',
      description: 'Who need a tool that scales from the first MVP to global enterprise deployment.'
    }
  ];

  return (
    <section id="audience" className="py-20 bg-primary-950 text-white">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Who is Continuum for?</h2>
          <p className="text-primary-200/80 max-w-2xl mx-auto text-lg">
            Built specifically for those who build the future.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {audiences.map((item, index) => (
            <div key={index} className="bg-white/5 border border-white/10 p-8 rounded-2xl backdrop-blur-sm hover:bg-white/10 transition-colors">
              <div className="w-14 h-14 rounded-xl bg-primary-600 flex items-center justify-center mb-6 shadow-lg shadow-primary-500/20">
                {item.icon}
              </div>
              <h3 className="text-xl font-bold mb-3">{item.title}</h3>
              <p className="text-primary-100/70 leading-relaxed">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TargetAudience;





