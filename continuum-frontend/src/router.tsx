import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';

// Pages
import Login from './pages/Auth/Login.tsx';
import Register from './pages/Auth/Register.tsx';
import Overview from './pages/Dashboard/Overview.tsx';
import Team from './pages/Dashboard/Team.tsx';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: 'login',
        element: <Login />,
      },
      {
        path: 'register',
        element: <Register />,
      },
      {
        path: 'dashboard',
        element: <Overview />,
      },
      {
        path: 'dashboard/team',
        element: <Team />,
      },
    ],
  },
]);

export default router;
