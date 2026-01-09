import { createBrowserRouter } from 'react-router-dom';
import App from './App';

// Auth pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import ForgotPassword from './pages/Auth/ForgotPassword';
import ResetPassword from './pages/Auth/ResetPassword';

// Main pages
import Landing from './pages/Landing';
import Overview from './pages/Dashboard/Overview';
import Team from './pages/Dashboard/Team';

// Project pages
import Projects from './pages/Projects';
import ProjectSettings from './pages/Projects/ProjectSettings';

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

      // Dashboard
      { path: 'dashboard', element: <Overview /> },
      { path: 'dashboard/team', element: <Team /> },

      // Projects
      { path: 'projects', element: <Projects /> },
      { path: 'projects/:projectId/settings', element: <ProjectSettings /> },
    ],
  },
]);

export default router;
