import Sidebar from "../../components/Sidebar";

const Overview = () => {
  return (
    <div className="flex min-h-screen">
      <Sidebar />

      <main className="flex-1 p-6">
        <h1 className="text-[18px] font-semibold">Dashboard content</h1>
      </main>
    </div>
  );
};

export default Overview;
