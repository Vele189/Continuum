import { Outlet } from 'react-router-dom';
import CustomCursor from './components/CustomCursor';

function App() {
  return (
    <>
      <CustomCursor />
      <Outlet />
    </>
  );
}

export default App;
