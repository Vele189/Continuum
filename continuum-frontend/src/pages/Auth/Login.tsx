import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [touched, setTouched] = useState({
    email: false,
    password: false
  });

  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  // Real-time validation functions
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

  // Get current errors
  const errors = {
    email: touched.email ? validateEmail(email) : '',
    password: touched.password ? validatePassword(password) : ''
  };

  const handleBlur = (field: keyof typeof touched) => {
    setTouched({
      ...touched,
      [field]: true
    });
  };

  const validateForm = () => {
    // Mark all fields as touched
    setTouched({
      email: true,
      password: true
    });

    // Check if there are any errors
    return !validateEmail(email) && !validatePassword(password);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
    }

  const handleGoogleLogin = () => {
    console.log('Google login');
  };

  const handleAppleLogin = () => {
    console.log('Apple login');
  };

  return (
    <div className="relative flex justify-center items-center min-h-screen p-10 overflow-hidden bg-gradient-to-b from-brand-blue to-brand-cream">
      {/* Form Container - 345x550px */}
      <div className="w-[345px] h-[550px] rounded-2xl overflow-hidden shadow-[0px_4px_24px_rgba(0,0,0,0.1)]">

        {/* Top Section - Continuum Header - 345x118px */}
        <div className="w-[345px] h-[118px] pt-9 px-6 pb-6 bg-white border-b border-[#F5F5F5] flex flex-col items-center gap-4">
          {/* Continuum logo and subtitle group - 219x58px */}
          <div className="w-[219px] h-[58px] flex flex-col gap-3 items-center">
            {/* Continuum Logo - 219x37px */}
            <img
              src="Continuum.svg"
              alt="Continuum Logo"
              className="w-[219px] h-[37px]"
            />

            {/* Subtitle - 139x15px */}
            <p className="w-[139px] h-[15px] font-sathu font-normal text-xs leading-[100%] tracking-[-0.12px] text-center text-[#252014] opacity-80">
              Time track with one click.
            </p>
          </div>
        </div>

        {/* Bottom Section - Form - 345x432px */}
        <div className="w-[345px] h-[432px] pt-6 px-6 pb-9 bg-[#F8F9F9] flex flex-col gap-6">

          {/* Social Buttons Group - 297x88px */}
          <div className="w-[297px] h-[88px] flex flex-col gap-2">
            {/* Google Button - 297x40px */}
            <button
              onClick={handleGoogleLogin}
              type="button"
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white py-2 px-4 flex items-center justify-center cursor-pointer relative"
            >
              <img
                src="google.svg"
                alt="Google Logo"
                className="w-5 h-5 absolute left-4"
              />
              <span className="font-satoshi text-sm font-medium text-[#252014] tracking-[0px] leading-[100%]">
                Continue with Google
              </span>
            </button>

            {/* Apple Button - 297x40px */}
           <button
              onClick={handleAppleLogin}
              type="button"
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white py-2 px-4 flex items-center justify-center cursor-pointer relative">
              <img
                src="apple.svg"
                alt="Apple Logo"
                className="w-5 h-5 absolute left-4"
              />
              <span className="font-satoshi text-sm font-medium text-[#252014] tracking-[0px] leading-[100%]">
                Continue with Apple
              </span>
            </button>
          </div>

          {/* Form Fields Group - 297x281px */}
          <form onSubmit={handleSubmit} className="w-[297px] h-[281px] flex flex-col gap-2">
            {/* Email Section - 297x63px */}
            <div className="w-[297px] flex flex-col gap-1">
              <label
                htmlFor="email"
                className="font-satoshi text-sm font-medium text-[#252014]"
              >
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
                className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white py-2 px-4 font-satoshi text-sm text-[#252014] outline-none"
              />
              {errors.email && (
                <p className="text-xs text-red-600 mt-1">{errors.email}</p>
              )}
            </div>

            {/* Password Section - 297x63px */}
            <div className="w-[297px] flex flex-col gap-1">
              <label
                htmlFor="password"
                className="font-satoshi text-sm font-medium text-[#252014]"
              >
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
                className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white py-2 px-4 font-satoshi text-sm text-[#252014] outline-none"
              />
              {errors.password && (
                <p className="text-xs text-red-600 mt-1">{errors.password}</p>
              )}
            </div>

            {/* Forgot Password */}
            <Link
              to="/forgot-password"
              className="self-end font-satoshi text-xs text-[#252014] no-underline"
            >
              Forgot password
            </Link>

            {/* Sign In Button + Sign Up Link Group - 297x67px */}
            <div className="w-[297px] h-[67px] flex flex-col gap-2">
              {/* Sign In Button - 297x40px */}
              <button
                type="submit"
                disabled={loading}
                className="w-[297px] h-10 rounded-lg bg-[#24B5F8] border-t border-white shadow-[0px_3px_9.3px_0px_rgba(44,158,249,0.1)] py-2 px-4 flex items-center justify-center cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="font-satoshi text-sm font-semibold text-white">
                  {loading ? 'Signing in...' : 'Sign in'}
                </span>
              </button>

              {/* Error Message */}
              {error && (
                <p className="text-xs text-red-600 text-center">
                  {error}
                </p>
              )}

                {/* Sign Up Link */}
          <div className="flex items-center justify-center gap-1">
            <p className="font-satoshi text-sm text-[#9FA5A8]">
              Don't have an account?
            </p>
            <Link
              to="/sign-up"
              className="font-satoshi text-sm text-[#252014] no-underline"
            >
              Sign up
            </Link>
          </div>
            </div>
          </form>
        </div>
      </div>

      {/* Terms Text - Outside the form, below it - 345x48px */}
      <div className="absolute w-[345px] h-12 mt-[630px] px-4 flex items-center justify-center">
        <p className="font-satoshi text-[11px] leading-[1.4] text-center text-[#252014] opacity-60">
          By clicking "Sign in" or "Continue" above, you acknowledge that you have read and understood, and agree to Continuum's{' '}
          <button
            type="button"
            className="bg-transparent border-none text-[11px] text-[#252014] cursor-pointer underline opacity-80"
          >
            Terms of Service
          </button>
          .
        </p>
      </div>
    </div>
  );
};

export default Login;
    } catch (err) {
      console.error('Login failed:', err);
    }
