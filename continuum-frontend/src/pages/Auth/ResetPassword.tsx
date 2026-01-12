import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import backArrowIcon from "../../assets/back-arrow.png"

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (newPassword.length < 8) {
      setLocalError("Password must be at least 8 characters");
      return;
    }

    if (newPassword !== confirmPassword) {
      setLocalError("Passwords do not match");
      return;
    }

    // Navigate to loading page after successful password reset
    navigate("/loading");
  };

  const displayError = localError;

  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-start justify-center pt-[137px] relative overflow-hidden">

      <div className="w-full max-w-[345px] h-[320px] rounded-2xl border border-[#F0F0F0] shadow-lg flex flex-col overflow-hidden">
        <div className="relative h-[54px] w-full flex items-center justify-center gap-4 px-6 py-4 bg-[#F9F9F9] border-b border-[#F5F5F5] text-[#595959]">
          <Link to="/login">
            <img src={backArrowIcon} alt="Back Arrow"
            className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5" />
          </Link>
          <h2 className="text-[16px] font-medium leading-[100%] tracking-[-0.01em] text-[#595959]">Reset password</h2>
        </div>

        <form onSubmit={handleSubmit} className="w-full">
            <div className="w-full h-[266px] flex flex-col gap-6 pt-6 px-6 pb-9 bg-white">

              <div className="w-full flex flex-col gap-2 relative">
                <div className="w-full h-[63px] flex flex-col gap-1">
                  <label htmlFor="new-password"
                    className=" text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">New Password</label>
                  <input
                    type="password"
                    id="new-password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    style={{ fontFamily: 'Satoshi' }}
                    className={`w-full h-[40px] border rounded-lg font-medium text-[14px] leading-[100%] tracking-[0] bg-[#FFFFFF] py-[8px] px-[16px] focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
                      }`}
                    placeholder="Enter new password"
                  />
                </div>
                <div className="w-full h-[63px] flex flex-col gap-1">
                  <label htmlFor="confirm-password" className="text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">Confirm new password</label>
                  <input
                    type="password"
                    id="confirm-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    style={{ fontFamily: 'Satoshi' }}
                    className={`w-full h-[40px] border rounded-lg font-medium text-[14px] leading-[100%] tracking-[0] bg-[#FFFFFF] py-[8px] px-[16px] focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
                      }`}
                    placeholder="Confirm new password"
                  />
                </div>
                {displayError && (
                  <span className="absolute -bottom-4 left-0 text-red-500 text-[11px] font-normal">
                    {displayError}
                  </span>
                )}
              </div>

              <button
                type="submit"
                className="w-full h-[40px] px-4 py-2 rounded-lg bg-gradient-to-r from-[#24B5F8] to-[#5521FE] text-white text-[14px] font-semibold leading-[100%] flex items-center justify-center gap-2">
                Reset password
              </button>

            </div>
          </form>

      </div>
    </div>
  );
}

export default ResetPassword;
