import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

interface LocationState {
  email?: string;
}

const EmailVerification = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LocationState;

  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Get email from navigation state or fallback
  const email = state?.email || 'amushiringani@gmail.com';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Reset error
    setError('');

    // Validate code
    if (!code.trim()) {
      setError('Please enter the verification code');
      return;
    }

    if (code.replace('-', '').length !== 6) {
      setError('Please enter a valid 6-digit code');
      return;
    }

    // Simulate submission
    setIsSubmitting(true);

    try {
      // Here you would typically verify the code with your backend
      // For now, we'll just navigate after a brief delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Navigate to loading screen
      navigate('/loading');
    } catch (err) {
      setError('Verification failed. Please try again.');
      console.error('Verification error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatCode = (value: string) => {
    // Remove non-numeric characters
    const numbers = value.replace(/[^0-9]/g, '');

    // Limit to 6 digits
    const limited = numbers.slice(0, 6);

    // Add hyphen after 3 digits
    if (limited.length > 3) {
      return `${limited.slice(0, 3)}-${limited.slice(3)}`;
    }

    return limited;
  };

  const handleCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatCode(e.target.value);
    setCode(formatted);

    // Clear error when user types
    if (error) {
      setError('');
    }
  };

  return (
    <div className="relative flex justify-center items-start min-h-screen p-10 overflow-hidden pt-[50px] bg-gradient-to-b from-brand-blue to-brand-cream">
      {/* Form Container - 345x303px */}
      <div className="w-[345px] h-[303px] mt-36 rounded-2xl border border-[#F5F5F5] shadow-[0px_2px_3px_0px_rgba(181,181,181,0.24),0px_6px_6px_0px_rgba(181,181,181,0.20),0px_14px_8px_0px_rgba(181,181,181,0.12),0px_25px_10px_0px_rgba(181,181,181,0.04),0px_39px_11px_0px_rgba(181,181,181,0)] overflow-hidden ">

        {/* Top Section - Header - 345x54px */}
        <div className="w-[345px] h-[54px] pt-6 pr-6 pb-4 pl-6 bg-[#F9F9F9] border-b border-[#F5F5F5] flex items-center justify-center relative">
          {/* Back Arrow - 20x20px */}
          <Link
            to="/register"
            className="w-5 h-5 absolute left-6 flex items-center justify-center"
            aria-label="Back to registration"
          >
            <img
              src="arrow.svg"
              alt=""
              className="w-5 h-5"
            />
          </Link>

          {/* Email code Text - centered - 79x22px */}
          <h2 className="w-[79px] h-[22px] font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515] m-0">
            Email code
          </h2>
        </div>

        {/* Bottom Section - Form Content - 345x249px */}
        <form
          onSubmit={handleSubmit}
          className="w-[345px] h-[249px] pt-6 pr-6 pb-9 pl-6 bg-white flex flex-col gap-6"
        >
         {/* Instruction Text - 297x38px */}
  <p className="w-[297px] h-[38px] font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#9FA5A8] m-0">
  Please enter the unique code we sent to <span className="w-[297px] h-[38px] font-satoshi font-medium text-[#151515]">{email}</span>
</p>

          {/* Code Input Group - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-2">
            {/* Code Label - 35x19px */}
            <label
              htmlFor="verification-code"
              className="w-[35px] h-[19px] font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              Code
            </label>

            {/* Input Box - 297x40px */}
            <input
              id="verification-code"
              type="text"
              value={code}
              onChange={handleCodeChange}
              placeholder="000-000"
              maxLength={7}
              inputMode="numeric"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border tracking-[2px]"
            />

            {/* Error Message */}
            {error && (
              <p className="text-xs text-red-600 mt-1">
                {error}
              </p>
            )}
          </div>

          {/* Sign Up Button - 297x40px */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-[297px] h-10 rounded-lg bg-[#24B5F8] pt-2 pr-4 pb-2 pl-4 flex items-center justify-center cursor-pointer border-none shadow-[0px_3px_9.3px_0px_rgba(44,158,249,0.1)] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="font-satoshi text-sm font-semibold text-white">
              {isSubmitting ? 'Verifying...' : 'Sign Up'}
            </span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default EmailVerification;
