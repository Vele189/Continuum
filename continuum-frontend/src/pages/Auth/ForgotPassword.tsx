import { FaArrowLeft } from "react-icons/fa";
import { Link } from "react-router-dom";

const ForgotPassword = () => {
  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden ">
      <div className="relative bg-white w-86.25 h-75.75  flex flex-col justify-center items-center pt-2 border-2 border-gray-100 rounded-2xl shadow-lg">
        <div className="absolute top-0 left-0 h-[54px] rounded-t-lg px-6 bg-[#F9F9F9] gap-4 flex items-center mb-6 w-full text-[22px] font-medium text-[#595959]">
          <Link to="/login">
            <FaArrowLeft className="text-[20px] font-light" />
          </Link>
          <h2 className="mb-0 ml-12">Forgot Password</h2>
        </div>

    <div className="px-6 h-[249px]">

        <p className="text-gray-400 mt-4 mb-6 text-[16px]">
          We will email a reset link to your email address you used.
        </p>

        <form className="w-full">
          <div>
            <label
              htmlFor="email"
              className="block text-gray-900 mb-2 text-[16px]"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              className="w-full px-4 py-2 mb-6 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-500 text-[16px]"
              placeholder="you@example.com"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-[#2299fa] text-white text-[16px] font-bold  py-2 px-4 rounded-lg"
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
