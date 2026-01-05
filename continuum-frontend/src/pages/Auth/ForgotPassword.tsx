import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import backArrowIcon from "../../assets/back-arrow.png"

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (!email) {
      setLocalError("Email is required");
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      setLocalError("Invalid email address");
      return;
    }

    // Navigate to reset password page (static flow, no backend)
    navigate("/reset-password");
  };

  const displayError = localError;

  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-start justify-center pt-[160px] relative overflow-hidden">

      <div className="bg-white w-[345px] h-[303px] border-2 border-gray-100 rounded-2xl shadow-lg flex flex-col justify-center items-center">

        <div className="relative h-[54px] rounded-t-lg bg-[#F5F5F5] flex items-center justify-between w-full font-medium text-[#595959]">
          <Link to="/login">
            <img src={backArrowIcon} alt="Back Arrow" className="absolute top-3 left-4 h-4" />
          </Link>
          <h2 className="text-[16px] mx-auto">Forgot Password</h2>
        </div>

        <div className="w-[345px] h-[249px] flex flex-col justify-center items-center gap-[24px]">
          <p className="w-[297px] h-[38px] text-gray-400 font-medium text-[14px] leading-[100%] tracking-[0]">
            We will email a reset link to your email address you used.
          </p>

          <form onSubmit={handleSubmit} className="w-full flex flex-col items-center gap-[24px]">
            <div className="w-[297px] h-[63px] flex flex-col gap-1 font-medium relative">
              <label htmlFor="email" className="block text-gray-900 text-[14px]">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`w-full h-[40px] px-4 py-2 border text-[14px] rounded-lg focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
                  }`}
                placeholder="Enter your email"
              />
              {displayError && (
                <span className="absolute -bottom-5 left-0 text-red-500 text-[11px] font-normal">
                  {displayError}
                </span>
              )}
            </div>

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
