import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import backArrowIcon from "../../assets/back-arrow.png";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    // Validate email field
    if (!email) {
      setLocalError("Email is required");
      return;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setLocalError("Invalid email address");
      return;
    }

    // Navigate to reset password page (static flow)
    navigate("/reset-password");
  };

  const displayError = localError;

  return (
    // Page Container - full screen with gradient background
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-start justify-center pt-[160px] relative overflow-hidden">

      {/* Card Container - 345x303px, white background, rounded, shadow */}
      <div className="bg-white w-[345px] h-[303px] border-2 border-gray-100 rounded-2xl shadow-lg flex flex-col justify-center items-center">

      {/* Top Bar - 345x54px, gray background, contains back arrow and title */}
        <div className="relative h-[54px] rounded-t-lg bg-[#F5F5F5] flex items-center justify-between w-full font-medium text-[#595959]">
          
      {/* Back Arrow - navigates to login */}
        <Link to="/login">
        <img src={backArrowIcon} alt="Back Arrow" className="absolute top-3 left-4 h-4" />
        </Link>

      {/* Page Title - centered */}
        <h2 className="text-[16px] mx-auto">Forgot Password</h2>
        </div>

      {/* Content Area - 345x249px, vertical layout */}
        <div className="w-[345px] h-[249px] flex flex-col justify-center items-center gap-[24px]">
          
      {/* Instruction Text - 297x38px */}
        <p className="w-[297px] h-[38px] text-gray-400 font-medium text-[14px] leading-[100%] tracking-[0] text-center">
          We will email a reset link to your email address you used.
        </p>

      {/* Form Container - 297x107px, email input + submit button */}
        <form onSubmit={handleSubmit} className="w-full flex flex-col items-center gap-[24px]">

      {/* Email Input Field - 297x63px container */}
        <div className="w-[297px] h-[63px] flex flex-col gap-1 font-medium relative">

      {/* Email Label */}
        <label htmlFor="email" className="block text-gray-900 text-[14px]">
                Email
        </label>

      {/* Email Input - 297x40px */}
        <input
        type="email"
        id="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className={`w-full h-[40px] px-4 py-2 border text-[14px] rounded-lg focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
      }`}
        placeholder="Enter your email"
        />
      {/* Error Message */}
        {displayError && (
                <span className="absolute -bottom-5 left-0 text-red-500 text-[11px] font-normal">
                  {displayError}
                </span>
         )}
        </div>

    {/* Submit Button - 297x40px */}
      <button
      type="submit"
      className="w-[297px] h-[40px] bg-[#2299fa] text-white text-[14px] font-bold py-2 px-4 rounded-lg transition-all hover:bg-[#1a8ae5]"
          >
      Send reset link
      </button>
      </form>
      </div>

      </div>
    </div>
  );
};

export default ForgotPassword;
