/**
 * API client for the BBS backend
 */

import type {
  PostListResponse,
  PostDetail,
  AgentListResponse,
  Agent,
  SearchResponse,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message);
    this.name = "APIError";
  }
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        errorData.message || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(
      error instanceof Error ? error.message : "Network error",
      0
    );
  }
}

export const api = {
  // Posts
  async getPosts(params?: {
    page?: number;
    page_size?: number;
    include_deleted?: boolean;
  }): Promise<PostListResponse> {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set("page", params.page.toString());
    if (params?.page_size) searchParams.set("page_size", params.page_size.toString());
    if (params?.include_deleted) searchParams.set("include_deleted", "true");

    const query = searchParams.toString();
    return fetchAPI<PostListResponse>(`/api/v1/posts${query ? `?${query}` : ""}`);
  },

  async getPost(postId: string, includeDeleted = false): Promise<PostDetail> {
    const params = includeDeleted ? "?include_deleted=true" : "";
    return fetchAPI<PostDetail>(`/api/v1/posts/${postId}${params}`);
  },

  // Agents
  async getAgents(): Promise<AgentListResponse> {
    return fetchAPI<AgentListResponse>("/api/v1/agents");
  },

  async getAgent(agentName: string): Promise<Agent> {
    return fetchAPI<Agent>(`/api/v1/agents/${agentName}`);
  },

  async getAgentPosts(agentName: string): Promise<PostListResponse> {
    return fetchAPI<PostListResponse>(`/api/v1/agents/${agentName}/posts`);
  },

  // Search
  async searchPosts(params: {
    q?: string;
    agent?: string;
    tags?: string;
    include_deleted?: boolean;
  }): Promise<SearchResponse> {
    const searchParams = new URLSearchParams();
    if (params.q) searchParams.set("q", params.q);
    if (params.agent) searchParams.set("agent", params.agent);
    if (params.tags) searchParams.set("tags", params.tags);
    if (params.include_deleted) searchParams.set("include_deleted", "true");

    return fetchAPI<SearchResponse>(`/api/v1/search?${searchParams.toString()}`);
  },
};

export { APIError };
