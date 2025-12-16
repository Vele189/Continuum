import { Link } from 'react-router-dom';
import signupImg from '../../assets/signup.png';
import loginImg from '../../assets/login.png';

const HowTo = () => {
  return (
    <section id="get-started" className="py-24 bg-primary-50">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Getting Started is Easy
          </h2>
          <p className="text-lg text-gray-600">
            Join thousands of teams already shipping faster with Continuum.
          </p>
        </div>

        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Sign Up Section */}
          <div className="bg-white p-8 rounded-2xl shadow-xl shadow-primary-900/5 hover:-translate-y-1 transition-transform duration-300">
            <div className="mb-6 rounded-xl overflow-hidden bg-primary-100/50 flex items-center justify-center p-6 h-48">
              <img src={signupImg} alt="Sign Up Illustration" className="h-full w-auto object-contain mix-blend-multiply" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">1. Create your account</h3>
            <p className="text-gray-600 mb-6">
              Get started for free in seconds. No credit card required. seamless collaboration awaits.
            </p>
            <Link to="/register" className="inline-block w-full py-3 px-6 bg-primary-600 text-white rounded-lg font-semibold text-center hover:bg-primary-700 transition-colors">
              Sign Up Now
            </Link>
          </div>

          {/* Log In Section */}
          <div className="bg-white p-8 rounded-2xl shadow-xl shadow-primary-900/5 hover:-translate-y-1 transition-transform duration-300">
             <div className="mb-6 rounded-xl overflow-hidden bg-primary-100/50 flex items-center justify-center p-6 h-48">
              <img src={loginImg} alt="Log In Illustration" className="h-full w-auto object-contain mix-blend-multiply" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">2. Return to work</h3>
            <p className="text-gray-600 mb-6">
              Already have an account? Sign securely to access your dashboard and pick up where you left off.
            </p>
            <Link to="/login" className="inline-block w-full py-3 px-6 bg-white text-primary-700 border border-primary-200 rounded-lg font-semibold text-center hover:bg-primary-50 transition-colors">
              Log In
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowTo;





