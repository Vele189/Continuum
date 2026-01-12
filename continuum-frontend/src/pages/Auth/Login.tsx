import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [touched, setTouched] = useState({ email: false, password: false });
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const validateEmail = (email: string) => {
    if (!email.trim()) return 'Email is required';
    if (!/\S+@\S+\.\S+/.test(email)) return 'Please enter a valid email address';
    return '';
  };

  const validatePassword = (password: string) => {
    if (!password) return 'Password is required';
    if (password.length < 8) return 'Password must be at least 8 characters';
    return '';
  };

  const errors = {
    email: touched.email ? validateEmail(email) : '',
    password: touched.password ? validatePassword(password) : ''
  };

  const handleBlur = (field: keyof typeof touched) => {
    setTouched({ ...touched, [field]: true });
  };

  const validateForm = () => {
    setTouched({ email: true, password: true });
    return !validateEmail(email) && !validatePassword(password);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  const handleGoogleLogin = () => console.log('Google login');
  const handleAppleLogin = () => console.log('Apple login');

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 sm:p-10 bg-gradient-to-b from-brand-blue to-brand-cream">
      {/* Card Container */}
      <div className="w-full max-w-[400px] sm:max-w-[360px] rounded-2xl overflow-hidden shadow-[0px_4px_24px_rgba(0,0,0,0.1)] bg-white">
        {/* Top Header */}
        <div className="w-full py-6 px-6 flex flex-col items-center gap-3 border-b border-[#F5F5F5]">
          <img src="Continuum.svg" alt="Continuum Logo" className="w-44 sm:w-56 h-auto" />
          <p className="text-xs sm:text-sm text-center text-[#252014] opacity-80">
            Time track with one click.
          </p>
        </div>

        {/* Form Section */}
        <div className="w-full py-6 px-6 flex flex-col gap-6 bg-[#F8F9F9]">
          {/* Social Buttons */}
          <div className="flex flex-col gap-2 w-full">
            <button
              onClick={handleGoogleLogin}
              type="button"
              className="w-full sm:w-[297px] py-2 px-4 rounded-lg border border-[#E9E9E9] bg-white flex items-center justify-center"
            >
              <img src="google.svg" alt="Google Logo" className="w-5 h-5 mr-2" />
              Continue with Google
            </button>
            <button
              onClick={handleAppleLogin}
              type="button"
              className="w-full sm:w-[297px] py-2 px-4 rounded-lg border border-[#E9E9E9] bg-white flex items-center justify-center"
            >
              <img src="apple.svg" alt="Apple Logo" className="w-5 h-5 mr-2" />
              Continue with Apple
            </button>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full sm:w-[297px]">
            {/* Email Input */}
            <div className="flex flex-col gap-1 w-full">
              <label htmlFor="email" className="text-sm sm:text-base font-medium text-[#252014]">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onBlur={() => handleBlur('email')}
                placeholder="What's your email address?"
                required
                className="w-full h-10 rounded-lg border border-[#E9E9E9] px-4"
              />
              {errors.email && <p className="text-xs text-red-600">{errors.email}</p>}
            </div>

            {/* Password Input */}
            <div className="flex flex-col gap-1 w-full">
              <label htmlFor="password" className="text-sm sm:text-base font-medium text-[#252014]">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onBlur={() => handleBlur('password')}
                placeholder="What's your password?"
                required
                className="w-full h-10 rounded-lg border border-[#E9E9E9] px-4"
              />
              {errors.password && <p className="text-xs text-red-600">{errors.password}</p>}
            </div>

            <Link to="/forgot-password" className="self-end text-xs sm:text-sm text-[#252014]">
              Forgot password
            </Link>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 rounded-lg bg-[#24B5F8] text-white disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>

            {/* Sign Up Link */}
            <div className="flex justify-center gap-1 text-xs sm:text-sm text-[#9FA5A8]">
              <p>Don't have an account?</p>
              <Link to="/sign-up" className="text-[#252014]">Sign up</Link>
            </div>

            {error && <p className="text-xs text-red-600 text-center">{error}</p>}
          </form>
        </div>
      </div>

      {/* Terms Text */}
      <p className="text-[11px] sm:text-xs text-center text-[#252014] opacity-60 mt-4 px-4">
        By clicking "Sign in" or "Continue" above, you acknowledge that you have read and understood, and agree to Continuum's{' '}
        <button className="underline text-[11px] sm:text-xs">Terms of Service</button>.
      </p>
    </div>
  );
};

export default Login;
