import { FaArrowLeft } from "react-icons/fa";
import { Link } from "react-router-dom";

const ResetPassword = () => {
  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden ">

      <div className="relative bg-white flex flex-col justify-center w-[400px] items-center px-6 pb-9 rounded-2xl border-2 border-gray-100 shadow-lg">

        <div className="absolute top-0 left-0 h-[54px] bg-[#F9F9F9]  flex items-center px-6 mb-8 w-full text-[22px] rounded-t-2xl font-medium text-[#595959]">
          <Link to="/login">
            <FaArrowLeft className="text-[20px] font-light" />
          </Link>
          <h2 className="mb-0 ml-18 font-medium text-[20px]">Reset Password</h2>
        </div>

        <div className="w-full mt-16">

        <form className="">
          <div className="mb-4">
            <label htmlFor="new-password" className="block text-gray-700 mb-2 text-[19px]"><strong>New password</strong></label>
            <input
              type="password"
              id="new-password"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg font-medium focus:outline-none focus:ring focus:ring-blue-500 text-[16px]"
              placeholder="Enter new password"
            />
          </div>
          <div className="mb-6">
            <label htmlFor="confirm-password" className="block text-gray-700 mb-2 text-[19px]"><strong>Confirm new password</strong></label>
            <input
              type="password"
              id="confirm-password"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg font-medium focus:outline-none focus:ring focus:ring-blue-500 text-[16px]"
              placeholder="Confirm new password"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-[#2299fa] text-white text-[16px] font-bold py-2 px-4 rounded-lg hover:bg-blue-500 transition duration-300"
          >
            Reset Password
          </button>
        </form>
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;