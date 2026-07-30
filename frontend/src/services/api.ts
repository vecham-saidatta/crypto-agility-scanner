const API_BASE_URL = "http://localhost:8000";

export interface CreateRepositoryRequest {
  name: string;
  url: string;
  default_branch: string;
}

export interface Repository {
  id: number;
  name: string;
  url: string;
  default_branch: string;
  created_at: string;
}

export async function createRepository(
  repository: CreateRepositoryRequest
): Promise<Repository> {
  const response = await fetch(`${API_BASE_URL}/repositories/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(repository),
  });

  if (!response.ok) {
    throw new Error(`Failed to create repository: ${response.status}`);
  }

  return response.json();
}

export async function getRepositories(): Promise<Repository[]> {
  const response = await fetch(`${API_BASE_URL}/repositories/`);

  if (!response.ok) {
    throw new Error(
      `Failed to fetch repositories: ${response.status} ${response.statusText}`
    );
  }

  return response.json();
}