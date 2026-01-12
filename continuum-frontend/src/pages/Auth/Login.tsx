import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {

      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

    return (
    <div className="relative flex justify-center items-center min-h-screen p-10 overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-200 via-purple-100 to-pink-200">
        {/* Large decorative circles */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-blue-200/40 to-purple-200/40 rounded-full blur-3xl transform translate-x-1/3 -translate-y-1/3"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-tr from-purple-200/40 to-pink-200/40 rounded-full blur-3xl transform -translate-x-1/3 translate-y-1/3"></div>

        {/* Medium circles */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-br from-indigo-200/30 to-blue-200/30 rounded-full blur-2xl"></div>
        <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-gradient-to-tl from-pink-200/30 to-purple-200/30 rounded-full blur-2xl"></div>

        {/* Small accent circles */}
        <div className="absolute top-1/2 right-1/3 w-32 h-32 bg-blue-300/20 rounded-full blur-xl"></div>
        <div className="absolute top-1/3 right-1/2 w-24 h-24 bg-purple-300/20 rounded-full blur-lg"></div>
      </div>

      <div className="relative bg-white p-10 rounded-lg shadow-sm w-full max-w-lg text-center">
        <div className="mb-8 flex justify-center items-center">
          <img src="/logo.png" alt="Continuum Logo" className="h-16 -mr-5" />
          <span className="text-3xl font-bold text-slate-900 tracking-tight">Continuum</span>
        </div>

        <h1 className="text-gray-900 text-2xl font-semibold mb-8">Login</h1>

        <div className="text-left">
          <div className="mb-5">
            <label htmlFor="email" className="block text-sm text-gray-700 mb-2 font-medium">
              Email
            </label>
            <div className="relative flex items-center">
              <span className="absolute left-3 text-gray-400 pointer-events-none">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </span>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="e.g. LethaboExample@gmail.com"
                required
                className="w-full py-3 px-11 border border-gray-300 rounded-md text-base text-gray-900 focus:outline-none focus:border-blue-500 transition-colors placeholder:text-gray-500"
              />
            </div>
          </div>

          <div className="mb-5">
            <label htmlFor="password" className="block text-sm text-gray-700 mb-2 font-medium">
              Password
            </label>

            <div className="relative flex items-center">
              <span className="absolute left-3 text-gray-400 pointer-events-none">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </span>
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full py-3 px-11 border border-gray-300 rounded-md text-base text-gray-900 focus:outline-none focus:border-blue-500 transition-colors placeholder:text-gray-500"
              />
              <button
                type="button"
                className="absolute right-3 bg-transparent border-0 cursor-pointer text-gray-400 hover:text-gray-700 p-0"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}
<Link to="/forgot-password" className="text-sm text-blue-600 no-underline hover:underline">
                Forgot Password?
              </Link>


          <button
            type="submit"
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-blue-600 text-white font-semibold py-3 border-0 rounded-md text-base cursor-pointer mt-4 mb-6 hover:bg-blue-700 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </div>

        <p className="text-sm text-gray-600 text-center leading-relaxed mb-6">
          By logging in, you agree to our <a href="#" className="text-blue-600 no-underline hover:underline">Terms of Service</a><br />
          and <a href="#" className="text-blue-600 no-underline hover:underline">Privacy Policy</a>.
        </p>

        <div className="text-sm text-gray-600 text-center">
          Don't have an account? <Link to="/register" className="text-blue-600 font-medium no-underline hover:underline">Sign up</Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
