# Continuum Backend API

This is the backend for the Continuum application, built with **FastAPI**. It handles user authentication, role-based access control, and user management.

## Base URL
Local Development: `http://localhost:8000`
API Version Prefix: `/api/v1`

---

## Authentication & Users

### 1. Register User
Create a new user account.
- **Endpoint**: `POST /api/v1/users/`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "jane.doe@example.com",
    "password": "SecurePassword123!",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "frontend" 
  }
  ```
  - `role` options: `frontend`, `backend`, `designer`, `project_manager`, `client` (Client = Admin).
- **Response (200 OK)**: Returns the created user object.

### 2. Login
Authenticate a user and receive access/refresh tokens.
- **Endpoint**: `POST /api/v1/auth/login`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "jane.doe@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJI...",
    "token_type": "bearer",
    "refresh_token": "eyJhbGciOiJI..."
  }
  ```

### 3. Refresh Token
Exchange a refresh token for a new access token when the current one expires.
- **Endpoint**: `POST /api/v1/auth/refresh-token`
- **Access**: Public (Requires valid refresh token)
- **Request Body/Query**:
  can be passed as query param `?refresh_token=...` or in body. 
  *(Note: Check specific implementation preference, usually body is preferred for security)*
  ```json
  {
      "refresh_token": "YOUR_REFRESH_TOKEN_STRING"
  }
  ```
- **Response (200 OK)**: Returns new `access_token` and `refresh_token`.

### 4. Verify Email
Verify a user's email address using the token received (simulated email in server logs).
- **Endpoint**: `GET /api/v1/users/verify-email`
- **Access**: Public
- **Query Parameters**:
  - `token`: The verification string sent to the user.
- **Example**: `GET /api/v1/users/verify-email?token=d097ffdb-56b7...`
- **Response (200 OK)**:
  ```json
  {
    "message": "Email verified successfully"
  }
  ```

---

## Password Management

### 1. Request Password Reset
Initiate the flow to reset a forgotten password.
- **Endpoint**: `POST /api/v1/auth/password-recovery/{email}`
- **Access**: Public
- **Path Parameters**:
  - `email`: The email address of the user.
- **Response (200 OK)**:
  ```json
  {
    "message": "If this email exists, a password reset token has been sent."
  }
  ```
  *(Check server console for the mock email/token)*

### 2. Reset Password
Set a new password using the valid reset token.
- **Endpoint**: `POST /api/v1/auth/reset-password`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "token": "RESET_TOKEN_FROM_EMAIL",
    "new_password": "NewSecurePassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "message": "Password updated successfully"
  }
  ```

---

## Role-Based Access Control (RBAC)

The system distinguishes between **Admins** (role=`client`) and **Members** (other roles).

### Admin Dashboard
Example of a protected admin-only route.
- **Endpoint**: `GET /api/v1/admin/dashboard`
- **Access**: Protected (Requires `Authorization: Bearer <token>`)
- **Permissions**: User role must be `client`.
- **Response**:
  - **200 OK**: If user is Admin.
  - **403 Forbidden**: If user is a Member (Frontend, Backend, etc.).

---

## Additional Notes

1.  **Token Expiry**: 
    - Access Token: 30 Minutes.
    - Refresh Token: 24 Hours.
    - Implement an interceptor to catch `401 Unauthorized` responses and attempt to use the `refresh_token` endpoint to get a new access token before logging the user out.
2.  **Mock Emails**: Since we don't have an SMTP server, look at the **backend terminal/logs** to grab verification and reset tokens during development.
