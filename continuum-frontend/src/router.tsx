import { createBrowserRouter } from 'react-router-dom';
import App from './App';

// Auth pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import ForgotPassword from './pages/Auth/ForgotPassword';
import ResetPassword from './pages/Auth/ResetPassword';
import Loading from './pages/Auth/Loading';
import EmailVerification from './pages/Auth/EmailVerification';
import SignUp from './pages/Auth/SignUp';

// Main pages
import Landing from './pages/Landing';
import Overview from './pages/Dashboard/Overview';
import Team from './pages/Dashboard/Team';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      // Landing
      { index: true, element: <Landing /> },
      
      // Auth
      { path: 'login', element: <Login /> },
      { path: 'register', element: <Register /> },
      { path: 'forgot-password', element: <ForgotPassword /> },
      { path: 'reset-password', element: <ResetPassword /> },
      { path: 'loading', element: <Loading /> },
      { path: 'email-verification', element: <EmailVerification /> },
      { path: 'sign-up', element: <SignUp /> },
      
      // Dashboard
      { path: 'dashboard', element: <Overview /> },
      { path: 'dashboard/team', element: <Team /> },
    ],
  },
]);

export default router;
