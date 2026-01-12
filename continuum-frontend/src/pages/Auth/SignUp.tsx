import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const SignUp = () => {
  const [email, setEmail] = useState('');
  const [touched, setTouched] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  // Real-time validation function
  const validateEmail = (email: string) => {
    if (!email.trim()) return 'Email is required';
    if (!/\S+@\S+\.\S+/.test(email)) return 'Please enter a valid email address';
    return '';
  };

  // Get current error
  const error = touched ? validateEmail(email) : '';

  // Mark email field as touched
  const handleBlur = () => setTouched(true);

  // Validate form before submit
  const validateForm = () => {
    setTouched(true);
    return !validateEmail(email);
  };

  // Handle form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      // Simulate network delay / signup process
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Navigate to register screen with email
      navigate('/register', { state: { email } });
    } catch (err) {
      console.error('Sign up failed:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Social login handlers
  const handleGoogleLogin = () => console.log('Google login');
  const handleAppleLogin = () => console.log('Apple login');

  return (
    // Page container - fills screen, gradient background
    <div className="flex justify-center items-center min-h-screen p-4 bg-gradient-to-b from-brand-blue to-brand-cream">

      {/* Form Container - max-width responsive, rounded, shadow */}
      <div className="w-full max-w-md rounded-2xl overflow-hidden shadow-lg">

        {/* Top Section - Continuum Header */}
        <div className="w-full bg-white border-b border-[#F5F5F5] flex flex-col items-center py-6 px-4 gap-4">
          {/* Continuum logo and subtitle group */}
          <div className="w-[219px] h-[58px] flex flex-col gap-3 items-center">
            {/* Continuum Logo */}
            <img
              src="Continuum.svg"
              alt="Continuum Logo"
              className="w-56 max-w-full h-auto"
            />
            {/* Subtitle */}
            <p className="text-xs font-sathu text-[#252014] opacity-80 text-center">
              Time track with one click.
            </p>
          </div>
        </div>

        {/* Bottom Section - Form Section */}
        <div className="w-full bg-[#F8F9F9] flex flex-col gap-4 py-6 px-4">

          {/* Social Buttons Group */}
          <div className="flex flex-col gap-2">
            {/* Google Button */}
            <button
              onClick={handleGoogleLogin}
              type="button"
              className="flex items-center justify-center relative gap-2 w-full h-10 rounded-lg border border-[#E9E9E9] bg-white"
            >
              <img src="google.svg" alt="Google" className="w-5 h-5 absolute left-3" />
              <span className="font-satoshi text-sm font-medium text-[#252014]">
                Continue with Google
              </span>
            </button>

            {/* Apple Button */}
            <button
              onClick={handleAppleLogin}
              type="button"
              className="flex items-center justify-center relative gap-2 w-full h-10 rounded-lg border border-[#E9E9E9] bg-white"
            >
              <img src="apple.svg" alt="Apple" className="w-5 h-5 absolute left-3" />
              <span className="font-satoshi text-sm font-medium text-[#252014]">
                Continue with Apple
              </span>
            </button>
          </div>

          {/* Email Section */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-1 w-full">
            {/* Email Label */}
            <label htmlFor="email" className="font-satoshi text-sm font-medium text-[#252014]">
              Email
            </label>
            {/* Email Input */}
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onBlur={handleBlur}
              placeholder="What's your email address?"
              required
              className="w-full h-10 px-4 border border-[#E9E9E9] rounded-lg text-sm font-satoshi text-[#252014] outline-none"
            />
            {/* Error Message */}
            {error && <p className="text-xs text-red-600 mt-1">{error}</p>}
          </form>

          {/* Continue with email Button and Sign In Link */}
          <div className="flex flex-col gap-2 w-full">
            {/* Continue Button */}
            <button
              onClick={handleSubmit}
              type="button"
              disabled={isSubmitting}
              className="w-full h-10 rounded-lg bg-gradient-to-r from-[#24B5F8] to-[#5521FE] text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Processing...' : 'Continue with email'}
            </button>

            {/* Sign In Link */}
            <div className="flex justify-center items-center gap-1 text-sm font-satoshi text-[#9FA5A8]">
              <span>Have an account?</span>
              <Link to="/login" className="text-[#252014] underline">
                Sign in
              </Link>
            </div>
          </div>
        </div>

        {/* Terms Text */}
        <p className="text-xs text-center text-[#252014] opacity-60 py-3 px-4">
          By clicking "Sign in" or "Continue" above, you acknowledge that you have read and
          understood, and agree to Continuum's{' '}
          <button className="underline">Terms of Service</button>.
        </p>
      </div>
    </div>
  );
};

export default SignUp;
