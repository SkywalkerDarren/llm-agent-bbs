/**
 * React hooks for data fetching
 */

import useSWR from "swr";
import { api } from "@/lib/api";
import type {
  PostListResponse,
  PostDetail,
  AgentListResponse,
  Agent,
  SearchResponse,
} from "@/lib/types";

export function usePosts(params?: {
  page?: number;
  page_size?: number;
  include_deleted?: boolean;
}) {
  const key = params ? ["posts", params] : "posts";
  const { data, error, isLoading, mutate } = useSWR<PostListResponse>(
    key,
    () => api.getPosts(params)
  );

  return {
    posts: data?.posts,
    total: data?.total,
    page: data?.page,
    pageSize: data?.page_size,
    totalPages: data?.total_pages,
    isLoading,
    isError: error,
    mutate,
  };
}

export function usePost(postId: string | null, includeDeleted = false) {
  const { data, error, isLoading, mutate } = useSWR<PostDetail>(
    postId ? ["post", postId, includeDeleted] : null,
    postId ? () => api.getPost(postId, includeDeleted) : null
  );

  return {
    post: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useAgents() {
  const { data, error, isLoading, mutate } = useSWR<AgentListResponse>(
    "agents",
    () => api.getAgents()
  );

  return {
    agents: data?.agents,
    total: data?.total,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useAgent(agentName: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Agent>(
    agentName ? ["agent", agentName] : null,
    agentName ? () => api.getAgent(agentName) : null
  );

  return {
    agent: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useAgentPosts(agentName: string | null) {
  const { data, error, isLoading, mutate } = useSWR<PostListResponse>(
    agentName ? ["agent-posts", agentName] : null,
    agentName ? () => api.getAgentPosts(agentName) : null
  );

  return {
    posts: data?.posts,
    total: data?.total,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useSearch(params: {
  q?: string;
  agent?: string;
  tags?: string;
  include_deleted?: boolean;
}) {
  const hasParams = params.q || params.agent || params.tags;
  const { data, error, isLoading, mutate } = useSWR<SearchResponse>(
    hasParams ? ["search", params] : null,
    hasParams ? () => api.searchPosts(params) : null
  );

  return {
    results: data?.results,
    total: data?.total,
    query: data?.query,
    filters: data?.filters,
    isLoading,
    isError: error,
    mutate,
  };
}
