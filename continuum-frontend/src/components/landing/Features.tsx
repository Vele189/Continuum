import { BarChart3, Users, Zap } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: <Zap className="w-6 h-6 text-primary-500" />,
      title: 'Lightning Fast',
      description: 'Built for speed with instant updates and real-time collaboration that keeps everyone in sync.'
    },
    {
      icon: <Users className="w-6 h-6 text-primary-500" />,
      title: 'Team Alignment',
      description: 'Keep your entire organization aligned with shared goals, automated status updates, and transparent workflows.'
    },
    {
      icon: <BarChart3 className="w-6 h-6 text-primary-500" />,
      title: 'Deep Insights',
      description: 'Gain visibility into your team\'s performance with powerful analytics and customizable dashboards.'
    }
  ];

  return (
    <section id="features" className="py-24 bg-white">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Why teams choose Continuum
          </h2>
          <p className="text-lg text-gray-600">
            We solve the chaos of modern software development with a single source of truth.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="p-8 rounded-2xl bg-white border border-gray-100 hover:border-primary-100 hover:shadow-xl hover:shadow-primary-900/5 hover:-translate-y-1 transition-all duration-300 group">
              <div className="w-12 h-12 rounded-xl bg-primary-50 border border-primary-100 flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform duration-300">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 block">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;






