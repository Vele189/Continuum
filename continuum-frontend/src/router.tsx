import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';

// Pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Overview from './pages/Dashboard/Overview';
import Team from './pages/Dashboard/Team';

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

