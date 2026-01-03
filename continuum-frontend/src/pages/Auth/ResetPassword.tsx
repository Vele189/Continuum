import backArrowIcon from "../../assets/back-arrow.png"
import { Link } from "react-router-dom";

const ResetPassword = () => {
  return (
    <div className="bg-linear-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden ">

      <div className="bg-white flex flex-col w-[345px] h-[320px] items-center rounded-2xl border-2 border-gray-100 shadow-lg">
        <div className="relative h-[54px] rounded-t-lg bg-[#F5F5F5] flex items-center justify-between w-full font-medium text-[#595959]">
          <Link to="/login">
            <img src={backArrowIcon} alt="Back Arrow" className="absolute left-4 top-3 h-4" />
          </Link>
          <h2 className="text-[16px] mx-auto">Rest password</h2>
        </div>


        <form className="">
          <div className="h-[266px] w-[345px] flex flex-col items-center justify-center gap-[24px]">

          <div className="w-[297px] h-[142px] flex flex-col mx-auto gap-[16px]">
            <div className="w-[297px] h-[63px] flex flex-col gap-[4px]">
              <label htmlFor="new-password" 
              className=" text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">New Password</label>
              <input
                type="password"
                id="new-password"
                className="w-[297px] h-[40px] border border-gray-300 rounded-lg 
            font-medium text-[14px] leading-[100%] tracking-[0] 
             opacity-100 py-[8px] px-[16px]"
                placeholder="Enter new password"
              />
            </div>
            <div className="w-[297px] h-[63px] flex flex-col gap-[4px]">
              <label htmlFor="confirm-password" className="text-[#151515] font-medium text-[14px] leading-[100%] tracking-[0]">Confirm new password</label>
         <input
  type="password"
  id="confirm-password"
  className="w-[297px] h-[40px] border border-gray-300 rounded-lg 
            font-medium text-[14px] leading-[100%] tracking-[0] 
             opacity-100 py-[8px] px-[16px]"
  placeholder="Confirm new password"
/>

            </div>
          </div>

<button
  type="submit"
  className="w-[297px] h-[40px] bg-[#2299fa] text-white text-[16px] font-bold py-2 px-4 rounded-lg"
>
  Reset password
</button>


          </div>
        </form>

      </div>
    </div>
  );
}

export default ResetPassword;