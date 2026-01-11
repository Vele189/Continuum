
import { useAuth } from "../../hooks/useAuth";

const Overview = () => {
  const { logout } = useAuth();
  return (
    <div className="dashboard-overview">
      <h1>Dashboard Overview</h1>
      <p>Welcome to your dashboard overview page.</p>
      <button onClick={() => logout()}>Logout</button>
    </div>
  );
};

export default Overview;
