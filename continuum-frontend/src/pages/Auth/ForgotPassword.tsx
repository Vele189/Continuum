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
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-start justify-center pt-[137px] relative overflow-hidden">

      <div className="bg-white w-full max-w-[345px] h-[303px] border border-[#F0F0F0] rounded-2xl shadow-lg overflow-hidden flex flex-col">
        <div className="relative h-[54px] w-full flex items-center justify-center gap-4 px-6 py-4 bg-[#F9F9F9] border-b border-[#F5F5F5] font-medium text-[#595959]">
          <Link to="/login">
            <img src={backArrowIcon} alt="Back Arrow" 
            className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5" />
          </Link>
          <h2 className="text-[16px]">Forgot password</h2>
        </div>

        <div className="w-full h-[249px] flex flex-col gap-6 pt-6 px-6 pb-9 bg-white">
          <p className="w-[297px] text-[#9FA5A8] text-[14px] font-medium leading-[100%]">
           We will email a reset link to your email address you used.
         </p>


          <form onSubmit={handleSubmit} className="w-full flex flex-col items-center gap-[16px]">
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
              className="w-full h-[40px] px-4 py-2 rounded-lg bg-gradient-to-r from-[#24B5F8] to-[#5521FE] text-white text-[14px] font-semibold leading-[100%] flex items-center justify-center gap-2"
             >Send reset link
            </button>
          </form>
        </div>

      </div>
    </div>
  );
};

export default ForgotPassword;
