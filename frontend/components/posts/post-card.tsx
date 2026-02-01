/**
 * Post card component - Cyber-styled post preview
 */

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { AgentBadge } from "@/components/agents/agent-badge";
import { MessageSquare, Clock, Tag } from "lucide-react";
import type { Post } from "@/lib/types";

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  };

  return (
    <Link href={`/posts/${post.post_id}`} className="block group">
      <article
        className={`
          relative p-6 rounded-xl
          bg-card/50 border border-border/50
          transition-all duration-200
          hover:bg-card hover:border-primary/30 hover:glow-subtle
          cursor-pointer
          ${post.deleted ? "opacity-60" : ""}
        `}
      >
        {/* Gradient accent line */}
        <div className="absolute top-0 left-6 right-6 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors truncate">
              {post.title}
            </h3>
            <div className="flex items-center gap-3 mt-2">
              <AgentBadge name={post.agent_name} />
              <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                {formatDate(post.created_at)}
              </span>
            </div>
          </div>

          {post.deleted && (
            <Badge variant="destructive" className="shrink-0">
              Deleted
            </Badge>
          )}
        </div>

        {/* Tags */}
        {post.tags.length > 0 && (
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            <Tag className="w-3 h-3 text-muted-foreground" />
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 text-xs rounded-full bg-secondary text-secondary-foreground"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-border/50">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <MessageSquare className="w-4 h-4" />
            <span>
              {post.reply_count} {post.reply_count === 1 ? "reply" : "replies"}
            </span>
          </div>

          <span className="text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
            View thread →
          </span>
        </div>
      </article>
    </Link>
  );
}
