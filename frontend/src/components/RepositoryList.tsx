import { useEffect, useState } from "react";
import { getRepositories } from "../services/api";
import type { Repository } from "../services/api";

function RepositoryList() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRepositories() {
      try {
        const data = await getRepositories();
        setRepositories(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load repositories.");
      } finally {
        setLoading(false);
      }
    }

    loadRepositories();
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl bg-white p-6 shadow-sm border border-slate-200">
        <p className="text-slate-500">Loading repositories...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-white p-6 shadow-sm border border-red-200">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (repositories.length === 0) {
    return (
      <div className="rounded-xl bg-white p-6 shadow-sm border border-slate-200">
        <p className="text-slate-500">
          No repositories have been added yet.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-2xl font-semibold text-slate-900">
          Repositories
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Repositories registered with the Crypto Agility Scanner.
        </p>
      </div>

      <div className="grid gap-4">
        {repositories.map((repository) => (
          <div
            key={repository.id}
            className="rounded-xl bg-white p-6 shadow-sm border border-slate-200"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  {repository.name}
                </h3>

                <a
                  href={repository.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1 block text-sm text-blue-600 hover:underline"
                >
                  {repository.url}
                </a>
              </div>

              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                {repository.default_branch}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RepositoryList;
