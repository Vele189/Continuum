import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    surname: '',
    password: '',
    confirmPassword: ''
  });
  
  const [errors, setErrors] = useState({
    email: '',
    firstName: '',
    surname: '',
    password: '',
    confirmPassword: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Clear error when user types
    if (errors[name as keyof typeof errors]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {
      email: '',
      firstName: '',
      surname: '',
      password: '',
      confirmPassword: ''
    };
    
    let isValid = true;
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
      isValid = false;
    }
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
      isValid = false;
    }
    
    if (!formData.surname.trim()) {
      newErrors.surname = 'Surname is required';
      isValid = false;
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
      isValid = false;
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
      isValid = false;
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
      isValid = false;
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
      isValid = false;
    }
    
    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Here you would typically register with your backend
      // For now, we'll just navigate after a brief delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Navigate to email verification with email in state
      navigate('/email-verification', { 
        state: { email: formData.email } 
      });
    } catch (err) {
      console.error('Registration failed:', err);
      setErrors({
        ...errors,
        email: 'Registration failed. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative flex justify-center items-center min-h-screen p-10 overflow-hidden bg-gradient-to-b from-brand-blue to-brand-cream">
      {/* Form Container - 345x557px */}
      <div className="w-[345px] h-[557px] rounded-2xl overflow-hidden shadow-[0px_4px_24px_rgba(0,0,0,0.1)]">
        
        {/* Top Section - Sign Up Header - 345x54px */}
        <div className="w-[345px] h-[54px] pt-4 pr-6 pb-4 pl-6 bg-[#F9F9F9] border-b border-[#F5F5F5] flex items-center justify-center relative">
          {/* Back Arrow - 20x20px */}
          <Link 
            to="/"
            className="w-5 h-5 absolute left-6 flex items-center justify-center"
            aria-label="Back to landing page"
          >
            <img 
              src="arrow.svg" 
              alt="" 
              className="w-5 h-5"
            />
          </Link>
          
          {/* Sign up Text - centered */}
          <h2 className="w-[54px] h-[22px] font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#595959] m-0">
            Sign up
          </h2>
        </div>

        {/* Bottom Section - Form - 345x503px */}
        <form 
          onSubmit={handleSubmit}
          className="w-[345px] h-[503px] pt-6 pr-6 pb-9 pl-6 bg-white flex flex-col gap-6"
        >
          {/* Email Field - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-1">
            <label 
              htmlFor="email"
              className="w-[35px] h-[19px] font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter email address"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border"
            />
            {errors.email && (
              <p className="text-xs text-red-600 mt-1">{errors.email}</p>
            )}
          </div>

          {/* First Name Field - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-1">
            <label 
              htmlFor="firstName"
              className="font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              First name
            </label>
            <input
              id="firstName"
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              placeholder="Enter first name"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border"
            />
            {errors.firstName && (
              <p className="text-xs text-red-600 mt-1">{errors.firstName}</p>
            )}
          </div>

          {/* Surname Field - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-1">
            <label 
              htmlFor="surname"
              className="font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              Surname
            </label>
            <input
              id="surname"
              type="text"
              name="surname"
              value={formData.surname}
              onChange={handleChange}
              placeholder="Enter surname"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border"
            />
            {errors.surname && (
              <p className="text-xs text-red-600 mt-1">{errors.surname}</p>
            )}
          </div>

          {/* Password Field - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-1">
            <label 
              htmlFor="password"
              className="font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border"
            />
            {errors.password && (
              <p className="text-xs text-red-600 mt-1">{errors.password}</p>
            )}
          </div>

          {/* Confirm Password Field - 297x63px */}
          <div className="w-[297px] h-[63px] flex flex-col gap-1">
            <label 
              htmlFor="confirmPassword"
              className="font-satoshi font-medium text-sm leading-[100%] tracking-[0%] text-[#151515]"
            >
              Confirm password
            </label>
            <input
              id="confirmPassword"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm password"
              required
              className="w-[297px] h-10 rounded-lg border border-[#E9E9E9] bg-white pt-2 pr-4 pb-2 pl-4 font-satoshi text-sm text-[#151515] outline-none box-border"
            />
            {errors.confirmPassword && (
              <p className="text-xs text-red-600 mt-1">{errors.confirmPassword}</p>
            )}
          </div>

          {/* Next Button - 297x40px */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-[297px] h-10 rounded-lg bg-[#24B5F8] pt-2 pr-4 pb-2 pl-4 flex items-center justify-center cursor-pointer border-none shadow-[0px_3px_9.3px_0px_rgba(44,158,249,0.1)] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="font-satoshi text-sm font-semibold text-white">
              {isSubmitting ? 'Processing...' : 'Next'}
            </span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;