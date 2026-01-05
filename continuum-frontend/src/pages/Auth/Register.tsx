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

  const [touched, setTouched] = useState({
    email: false,
    firstName: false,
    surname: false,
    password: false,
    confirmPassword: false
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Real-time validation functions
  const validateEmail = (email: string) => {
    if (!email.trim()) return 'Email is required';
    if (!/\S+@\S+\.\S+/.test(email)) return 'Please enter a valid email address';
    return '';
  };

  const validateFirstName = (name: string) => {
    if (!name.trim()) return 'First name is required';
    if (name.trim().length < 2) return 'First name must be at least 2 characters';
    return '';
  };

  const validateSurname = (name: string) => {
    if (!name.trim()) return 'Surname is required';
    if (name.trim().length < 2) return 'Surname must be at least 2 characters';
    return '';
  };

  const validatePassword = (password: string) => {
    if (!password) return 'Password is required';
    if (password.length < 8) return 'Password must be at least 8 characters';
    if (!/[A-Z]/.test(password)) return 'Password must contain at least one uppercase letter';
    if (!/[a-z]/.test(password)) return 'Password must contain at least one lowercase letter';
    if (!/[0-9]/.test(password)) return 'Password must contain at least one number';
    return '';
  };

  const validateConfirmPassword = (confirmPassword: string, password: string) => {
    if (!confirmPassword) return 'Please confirm your password';
    if (password !== confirmPassword) return 'Passwords do not match';
    return '';
  };

  // Get current errors
  const errors = {
    email: touched.email ? validateEmail(formData.email) : '',
    firstName: touched.firstName ? validateFirstName(formData.firstName) : '',
    surname: touched.surname ? validateSurname(formData.surname) : '',
    password: touched.password ? validatePassword(formData.password) : '',
    confirmPassword: touched.confirmPassword ? validateConfirmPassword(formData.confirmPassword, formData.password) : ''
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleBlur = (field: keyof typeof touched) => {
    setTouched({
      ...touched,
      [field]: true
    });
  };

  const validateForm = () => {
    // Mark all fields as touched
    setTouched({
      email: true,
      firstName: true,
      surname: true,
      password: true,
      confirmPassword: true
    });

    // Check if there are any errors
    return !validateEmail(formData.email) &&
           !validateFirstName(formData.firstName) &&
           !validateSurname(formData.surname) &&
           !validatePassword(formData.password) &&
           !validateConfirmPassword(formData.confirmPassword, formData.password);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 500));

      navigate('/email-verification', {
        state: { email: formData.email }
      });
    } catch (err) {
      console.error('Registration failed:', err);
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
              onBlur={() => handleBlur('email')}
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
              onBlur={() => handleBlur('firstName')}
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
              onBlur={() => handleBlur('surname')}
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
              onBlur={() => handleBlur('password')}
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
              onBlur={() => handleBlur('confirmPassword')}
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
