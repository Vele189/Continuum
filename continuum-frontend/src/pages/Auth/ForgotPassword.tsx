import { FaArrowLeft } from "react-icons/fa"; 


const ForgotPassword = () =>{
  return (
    
   
    <div className="bg-gradient-to-b from-[#B2E6F7] to-[#FFFFFF] min-h-screen flex items-center justify-center relative overflow-hidden ">

      <div className="bg-white w-86.25 h-75.75  flex flex-col justify-center items-center px-[24px] pt-[24px] pb-[36px] rounded-2xl shadow-lg">

      <div className="bg-[#F9F9F9]  flex items-center gap-4 mb-6 w-full text-2xl font-medium text-[#595959]"> 
          <FaArrowLeft className="text-xl" /> 
          <h2 className="mb-0 mx-6">Forgot Password</h2>
      </div>


        <p className="text-gray-400 mb-6">We will email a reset link to your email address you used.</p>

        <form className="w-full max-w-sm">
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-700 mb-2">Email</label>
            <input
              type="email"
              id="email"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-300"
          >
            Send reset link
          </button>
        </form>
      </div>
    </div>
  );

}





export default ForgotPassword;

