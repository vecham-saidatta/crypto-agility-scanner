import { useState } from "react";
import type { FormEvent } from "react";
import { createRepository } from "../services/api";

function RepositoryForm() {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [defaultBranch, setDefaultBranch] = useState("main");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setError("");

    if (!name.trim() || !url.trim()) {
      setError("Repository name and URL are required.");
      return;
    }

    setLoading(true);

    try {
      await createRepository({
        name: name.trim(),
        url: url.trim(),
        default_branch: defaultBranch.trim() || "main",
      });
      setMessage("Repository added successfully.");
      setName("");
      setUrl("");
      setDefaultBranch("main");
    } catch (err) {
      console.error(err);
      setError("Failed to add repository. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-xl bg-white p-6 shadow-sm border border-slate-200">
      <h2 className="text-2xl font-semibold text-slate-900">Add Repository</h2>
      <p className="mt-1 text-sm text-slate-500">
        Register a repository to scan with the Crypto Agility Scanner.
      </p>

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-sm font-medium text-slate-700" htmlFor="name">
            Repository name
          </label>
          <input
            id="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200"
            placeholder="e.g. crypto-scanner"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700" htmlFor="url">
            Repository URL
          </label>
          <input
            id="url"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200"
            placeholder="https://github.com/owner/repo"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700" htmlFor="defaultBranch">
            Default branch
          </label>
          <input
            id="defaultBranch"
            value={defaultBranch}
            onChange={(event) => setDefaultBranch(event.target.value)}
            className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200"
            placeholder="main"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Saving..." : "Add repository"}
        </button>

        {message ? (
          <p className="text-sm text-emerald-600">{message}</p>
        ) : null}
        {error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : null}
      </form>
    </div>
  );
}

export default RepositoryForm;
