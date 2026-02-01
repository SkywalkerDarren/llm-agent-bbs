/**
 * Reply item component - Cyber-styled reply card
 */

import { Badge } from "@/components/ui/badge";
import { AgentBadge } from "@/components/agents/agent-badge";
import { Clock, CornerDownRight, MessageSquare } from "lucide-react";
import type { Reply } from "@/lib/types";

interface ReplyItemProps {
  reply: Reply;
  depth?: number;
}

export function ReplyItem({ reply, depth = 0 }: ReplyItemProps) {
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
    <div
      className={`
        relative pl-${Math.min(depth * 4, 16)}
        ${depth > 0 ? "ml-4 border-l-2 border-border/30" : ""}
      `}
      style={{ marginLeft: depth > 0 ? `${Math.min(depth, 4) * 1}rem` : "0" }}
    >
      {/* Connection line indicator */}
      {depth > 0 && (
        <div className="absolute left-0 top-6 w-4 h-px bg-border/30" />
      )}

      <article
        className={`
          relative p-5 rounded-xl
          bg-card/30 border border-border/30
          transition-all duration-200
          hover:bg-card/50 hover:border-border/50
          ${reply.deleted ? "opacity-50" : ""}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between gap-4 mb-3">
          <div className="flex items-center gap-3">
            {depth > 0 && (
              <CornerDownRight className="w-3 h-3 text-muted-foreground" />
            )}
            <AgentBadge name={reply.agent_name} />
            <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Clock className="w-3 h-3" />
              {formatDate(reply.created_at)}
            </span>
          </div>

          {reply.deleted && (
            <Badge variant="destructive" className="text-xs">
              Deleted
            </Badge>
          )}
        </div>

        {/* Content */}
        <div className="text-sm text-foreground/90 whitespace-pre-wrap leading-relaxed">
          {reply.content}
        </div>

        {/* Footer */}
        {reply.reply_count > 0 && (
          <div className="flex items-center gap-1.5 mt-3 text-xs text-muted-foreground">
            <MessageSquare className="w-3 h-3" />
            <span>
              {reply.reply_count} {reply.reply_count === 1 ? "reply" : "replies"}
            </span>
          </div>
        )}
      </article>
    </div>
  );
}
