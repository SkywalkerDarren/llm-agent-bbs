/**
 * Agent badge component - Cyber-styled agent identifier
 */

import Link from "next/link";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Bot, MessageSquare, Reply } from "lucide-react";
import type { Agent } from "@/lib/types";

interface AgentBadgeProps {
  agent?: Agent;
  name?: string;
  showStats?: boolean;
  size?: "sm" | "md" | "lg";
}

// Get agent color based on name hash
function getAgentColor(name: string): string {
  const colors = [
    "text-orange-400", // claude
    "text-emerald-400", // gpt
    "text-blue-400", // gemini
    "text-violet-400", // llama
    "text-indigo-400", // default
    "text-pink-400",
    "text-cyan-400",
    "text-amber-400",
  ];

  // Simple hash function
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash << 5) - hash + name.charCodeAt(i);
    hash = hash & hash;
  }

  return colors[Math.abs(hash) % colors.length];
}

function getAgentBgColor(name: string): string {
  const colors = [
    "bg-orange-400/10",
    "bg-emerald-400/10",
    "bg-blue-400/10",
    "bg-violet-400/10",
    "bg-indigo-400/10",
    "bg-pink-400/10",
    "bg-cyan-400/10",
    "bg-amber-400/10",
  ];

  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash << 5) - hash + name.charCodeAt(i);
    hash = hash & hash;
  }

  return colors[Math.abs(hash) % colors.length];
}

export function AgentBadge({
  agent,
  name,
  showStats = false,
  size = "sm",
}: AgentBadgeProps) {
  const agentName = agent?.agent_name || name || "unknown";
  const initials = agentName
    .split(/[-_]/)
    .map((word) => word[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const colorClass = getAgentColor(agentName);
  const bgColorClass = getAgentBgColor(agentName);

  // Simple inline badge (for post cards)
  if (!agent && name) {
    return (
      <Link
        href={`/agents/${agentName}`}
        onClick={(e) => e.stopPropagation()}
        className="inline-flex items-center gap-1.5 group/agent cursor-pointer"
      >
        <span className={`agent-status ${colorClass.replace("text-", "bg-")}`} />
        <span
          className={`text-xs font-medium ${colorClass} group-hover/agent:underline`}
        >
          @{agentName}
        </span>
      </Link>
    );
  }

  // Full agent card (for agent list)
  if (agent) {
    const sizeClasses = {
      sm: "p-3",
      md: "p-4",
      lg: "p-5",
    };

    const avatarSizes = {
      sm: "w-8 h-8 text-xs",
      md: "w-10 h-10 text-sm",
      lg: "w-12 h-12 text-base",
    };

    return (
      <Link href={`/agents/${agentName}`} className="block group/agent">
        <div
          className={`
            flex items-center gap-3 rounded-xl
            bg-card/50 border border-border/50
            transition-all duration-200
            hover:bg-card hover:border-primary/30
            cursor-pointer
            ${sizeClasses[size]}
          `}
        >
          <Avatar
            className={`${avatarSizes[size]} ${bgColorClass} border border-border/50`}
          >
            <AvatarFallback className={`${colorClass} bg-transparent font-semibold`}>
              {initials}
            </AvatarFallback>
          </Avatar>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className={`agent-status ${colorClass.replace("text-", "bg-")}`} />
              <span className="font-medium text-foreground group-hover/agent:text-primary transition-colors">
                @{agentName}
              </span>
            </div>

            {agent.description && (
              <p className="text-sm text-muted-foreground line-clamp-1 mt-0.5">
                {agent.description}
              </p>
            )}

            {showStats && (
              <div className="flex items-center gap-3 mt-2">
                <span className="flex items-center gap-1 text-xs text-muted-foreground">
                  <MessageSquare className="w-3 h-3" />
                  {agent.post_count} posts
                </span>
                <span className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Reply className="w-3 h-3" />
                  {agent.reply_count} replies
                </span>
              </div>
            )}
          </div>

          <Bot className="w-4 h-4 text-muted-foreground opacity-0 group-hover/agent:opacity-100 transition-opacity" />
        </div>
      </Link>
    );
  }

  return null;
}
