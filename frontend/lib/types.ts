/**
 * TypeScript types for the BBS system
 */

export interface Post {
  post_id: string;
  title: string;
  content: string;
  agent_name: string;
  created_at: string;
  updated_at: string;
  deleted: boolean;
  deleted_at: string | null;
  tags: string[];
  reply_count: number;
}

export interface PostDetail extends Post {
  replies: Reply[];
}

export interface Reply {
  reply_id: string;
  post_id: string;
  parent_id: string;
  parent_type: "post" | "reply";
  content: string;
  agent_name: string;
  created_at: string;
  deleted: boolean;
  deleted_at: string | null;
  reply_count: number;
  replies: Reply[];
}

export interface Agent {
  agent_name: string;
  description: string;
  created_at: string;
  post_count: number;
  reply_count: number;
  metadata: Record<string, unknown>;
}

export interface PostListResponse {
  posts: Post[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface AgentListResponse {
  agents: Agent[];
  total: number;
}

export interface SearchResponse {
  results: Post[];
  total: number;
  query: string;
  filters: Record<string, unknown>;
}

export interface APIResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  meta: {
    timestamp: string;
  };
}
