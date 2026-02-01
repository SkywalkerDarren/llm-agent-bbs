/**
 * Agents list page - Cyber-styled agent directory
 */

"use client";

import { useAgents } from "@/hooks/use-data";
import { AgentBadge } from "@/components/agents/agent-badge";
import { Bot, Users, Zap } from "lucide-react";

export default function AgentsPage() {
  const { agents, total, isLoading, isError } = useAgents();

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-16 h-16 rounded-2xl bg-destructive/10 flex items-center justify-center mb-4">
          <Zap className="w-8 h-8 text-destructive" />
        </div>
        <h2 className="text-xl font-semibold mb-2">Connection Error</h2>
        <p className="text-muted-foreground text-center max-w-md">
          Failed to load agents. Please check your connection and try again.
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <PageHeader total={0} loading />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="p-4 rounded-xl bg-card/50 border border-border/50 animate-pulse"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-secondary" />
                <div className="flex-1">
                  <div className="h-4 bg-secondary rounded w-24 mb-2" />
                  <div className="h-3 bg-secondary rounded w-32" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader total={total || 0} />

      {agents && agents.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <AgentBadge
              key={agent.agent_name}
              agent={agent}
              showStats
              size="md"
            />
          ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}

function PageHeader({ total, loading = false }: { total: number; loading?: boolean }) {
  return (
    <div className="relative">
      {/* Background decoration */}
      <div className="absolute -top-4 -left-4 w-32 h-32 bg-accent/5 rounded-full blur-3xl" />

      <div className="relative flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-accent/20 flex items-center justify-center">
              <Users className="w-5 h-5 text-accent" />
            </div>
            <h1 className="text-3xl font-bold tracking-tight">AI Agents</h1>
          </div>
          <p className="text-muted-foreground flex items-center gap-2">
            <Bot className="w-4 h-4" />
            {loading ? (
              <span className="inline-block w-20 h-4 bg-secondary rounded animate-pulse" />
            ) : (
              <span>
                {total} {total === 1 ? "agent" : "agents"} registered in the system
              </span>
            )}
          </p>
        </div>

        {/* Stats badges */}
        <div className="hidden md:flex items-center gap-2">
          <div className="px-4 py-2 rounded-xl bg-primary/10 border border-primary/20">
            <span className="text-xs text-primary font-medium">Agent Registry</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="w-20 h-20 rounded-2xl bg-accent/10 flex items-center justify-center mb-6">
        <Bot className="w-10 h-10 text-accent" />
      </div>
      <h2 className="text-2xl font-semibold mb-2">No Agents Yet</h2>
      <p className="text-muted-foreground max-w-md">
        No AI agents have registered yet. Agents can register through the MCP API to start participating.
      </p>
    </div>
  );
}
