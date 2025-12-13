

export const routes ={
    login: '/login',
    register: '/register',
    forgotPassword: '/forgotpassword',
    resetPassword: '/resetpassword',
    dashboard: '/dashboard',
} as const;
  

export const mock_users = {
    valid_user: {
        email: 'Lethaboexample@gmail.com',
        password: 'valid_password@1234',
        firstname: 'Lethabo',
        lastname: 'Sehlapelo',
    },
    invalid_user: {
        email: 'invalid_user@example.com',
        password: 'invalid_password',
    },
} as const;

export const validation_messages_for_input = {
    missing_email: 'Enter an email address',
    missing_password: 'Enter a password',
    passwords_mismatch: 'Passwords do not match',
    invalid_email: 'Enter a valid email address',
    invalid_password: 'Enter a valid password',
    password_is_too_short: 'Password must be at least 10 characters long',
    failed_to_send_reset_link: 'Failed to send reset link, Please try again',
    failed_to_reset: 'Failed to reset password. Please try again'
}as const;

export const success_messages = {
    reset_link_sent: 'Reset link sent! Check your email for instructions to reset your password.',
    password_changed: 'Password changed successfully! You can now log in with your new password.',
}as const;

export const selectors ={
  // Common
  email_input: 'input[type="email"]',
  password_input: 'input[type="password"]',
  submit_button: 'button[type="submit"]',
  error_message: '[class*="bg-red-50"]',
  success_message: '[class*="bg-green-50"]',
  
  show_password_button: 'button[type="button"]',
  forgot_password_link: 'a[href="/forgotpassword"]',
  signup_link: 'a[href="\\\\register"]',
  
  firstname_input: 'input#firstname',
  lastname_input: 'input#lastname',
  confirm_password_input: 'input#confirm-password',
  login_link: 'a[href="/login"]',
  
  
  back_to_login_button: 'button:has-text("Back to Login")',
  
  new_password_input: 'input#new-password',
  go_to_login_button: 'button:has-text("Go to Login")',
} as const;


export const api_endpoints = {
    login: '/api/auth/login',
    register: '/api/auth/register',
    forgotPassword: '/api/auth/forgotpassword',
    resetPassword: '/api/auth/resetpassword',
} as const;

export const mock_response = {
    login: {
        success: {
            status: 200,
            body: {
                message: 'Login successful',
                token: 'valid_token',
                user: {
                    id: 1,
                    email: mock_users.valid_user.email,
                    firstname: mock_users.valid_user.firstname,
                    lastname: mock_users.valid_user.lastname,
                },
            },
        },
        failure: {
            status: 401,
            body: {
                message: 'Invalid credentials',
            },
        },
    },
    register: {
        success: {
            status: 201,
            body: {
                message: 'User registered successfully',
                user: {
                    id: 1,
                    email: mock_users.valid_user.email,
                    firstname: mock_users.valid_user.firstname,
                    lastname: mock_users.valid_user.lastname,
                },
            },
        },
        failure: {
            status: 400,
            body: {
                message: 'User already exists',
            },
        },
    },
    forgotPassword: {
        success: {
            status: 200,
            body: {
                message: 'Reset link sent! Check your email for instructions to reset your password.',
            },
        },
        failure: {
            status: 404,
            body: {
                message: 'User not found',
            },
        },
    },
    resetPassword: {
        success: {
            status: 200,
            body: {
                message: 'Password changed successfully! You can now log in with your new password.',
            },
        },
        failure: {
            status: 400,
            body: {
                message: 'Failed to reset password. Please try again',
            },
        },
    },
}   as const;