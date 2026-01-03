import { Link } from "react-router-dom";
import backArrowIcon from "../../assets/back-arrow.png"

const ForgotPassword = () => {
  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden ">

      <div className="bg-white w-[345px] h-[303px] border-2 border-gray-100 rounded-2xl shadow-lg flex flex-col justify-center items-center">

<div className="relative h-[54px] rounded-t-lg bg-[#F5F5F5] flex items-center justify-between w-full font-medium text-[#595959]">
  <Link to="/login">
    <img src={backArrowIcon} alt="Back Arrow" className="absolute top-3 left-4 h-4" />
  </Link>
  <h2 className="text-[16px] mx-auto">Forgot Password</h2>
</div>



    <div className="w-[345px] h-[249px] flex flex-col justify-center items-center gap-6">

<p
  className="w-[297px] h-[38px] text-gray-400 font-medium text-[14px] leading-[100%] tracking-[0]"
>
  We will email a reset link to your email address you used.
</p>


        <form className="w-full flex flex-col items-center gap-[24px]">
          <div className="w-[297px] h-[63px] flex flex-col gap-1 font-medium">
            <label
              htmlFor="email"
              className="block text-gray-900 text-[14px]"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              className="w-full h-[40px] px-4 py-2 border text-[14px] border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
              placeholder="amushiringani@gmail.com"
            />
          </div>

          <button
            type="submit"
            className="w-[297px] h-[40px] bg-[#2299fa] text-white text-[14px] font-bold  py-2 px-4 rounded-lg"
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
