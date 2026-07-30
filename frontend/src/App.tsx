import Navbar from "./components/Navbar";
import RepositoryForm from "./components/RepositoryForm";
import RepositoryList from "./components/RepositoryList";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="mx-auto max-w-7xl px-6 py-10">
        <div className="grid gap-10 lg:grid-cols-2">
          <RepositoryForm />

          <RepositoryList />
        </div>
      </main>
    </div>
  );
}

export default App;