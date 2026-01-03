import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import backArrowIcon from "../../assets/back-arrow.png"
import { useAuth } from "../../hooks/useAuth";

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const [searchParams] = useSearchParams();
  const { resetPassword, loading, error: apiError } = useAuth();

  const token = searchParams.get("token");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);

    if (!token) {
      setLocalError("Invalid or missing token");
      return;
    }

    if (newPassword.length < 8) {
      setLocalError("Password must be at least 8 characters");
      return;
    }

    if (newPassword !== confirmPassword) {
      setLocalError("Passwords do not match");
      return;
    }

    try {
      await resetPassword(token, newPassword);
      setSuccess(true);
    } catch (err) {
      // Error handled by useAuth
    }
  };

  const displayError = localError || apiError;

  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden">

      <div className="bg-white flex flex-col w-[345px] h-[320px] items-center rounded-2xl border-2 border-gray-100 shadow-lg">
        <div className="relative h-[54px] rounded-t-lg bg-[#F5F5F5] flex items-center justify-between w-full font-medium text-[#595959]">
          <Link to="/login">
            <img src={backArrowIcon} alt="Back Arrow" className="absolute left-4 top-3 h-4" />
          </Link>
          <h2 className="text-[16px] mx-auto">Rest password</h2>
        </div>

        {success ? (
          <div className="h-[266px] w-[345px] flex flex-col items-center justify-center gap-4 text-center">
            <p className="text-gray-900 font-medium text-[16px]">
              Password updated successfully!
            </p>
            <Link to="/login" className="text-[#2299fa] font-bold text-[14px]">
              Back to Login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="w-full">
            <div className="h-[266px] w-[345px] flex flex-col items-center justify-center gap-[24px]">

              <div className="w-[297px] h-[142px] flex flex-col mx-auto gap-[16px] relative">
                <div className="w-[297px] h-[63px] flex flex-col gap-[4px]">
                  <label htmlFor="new-password"
                    className=" text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">New Password</label>
                  <input
                    type="password"
                    id="new-password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className={`w-[297px] h-[40px] border rounded-lg font-medium text-[14px] leading-[100%] tracking-[0] opacity-100 py-[8px] px-[16px] focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
                      }`}
                    placeholder="Enter new password"
                  />
                </div>
                <div className="w-[297px] h-[63px] flex flex-col gap-[4px]">
                  <label htmlFor="confirm-password" className="text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">Confirm new password</label>
                  <input
                    type="password"
                    id="confirm-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className={`w-[297px] h-[40px] border rounded-lg font-medium text-[14px] leading-[100%] tracking-[0] opacity-100 py-[8px] px-[16px] focus:outline-none focus:ring focus:ring-blue-500 ${displayError ? "border-red-500" : "border-gray-300"
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
                disabled={loading}
                className={`w-[297px] h-[40px] bg-[#2299fa] text-white text-[16px] font-bold py-2 px-4 rounded-lg transition-all ${loading ? "animate-pulse opacity-80" : "hover:bg-[#1a8ae5]"
                  }`}
              >
                Rest password
              </button>

            </div>
          </form>
        )}

      </div>
    </div>
  );
}

export default ResetPassword;