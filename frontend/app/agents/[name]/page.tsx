/**
 * Agent detail page - displays agent profile and their posts
 */

"use client";

import { use } from "react";
import { useAgent, useAgentPosts } from "@/hooks/use-data";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { PostList } from "@/components/posts/post-list";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";

export default function AgentDetailPage({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = use(params);
  const { agent, isLoading: agentLoading, isError: agentError } = useAgent(name);
  const { posts, isLoading: postsLoading, isError: postsError } = useAgentPosts(name);

  if (agentError || postsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          Failed to load agent information. Please try again later.
        </AlertDescription>
      </Alert>
    );
  }

  if (agentLoading) {
    return <div className="text-center py-12">Loading agent...</div>;
  }

  if (!agent) {
    return (
      <Alert>
        <AlertDescription>Agent not found.</AlertDescription>
      </Alert>
    );
  }

  const initials = agent.agent_name
    .split("_")
    .map((word) => word[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-start gap-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="text-2xl">{initials}</AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <CardTitle className="text-2xl">@{agent.agent_name}</CardTitle>
              <p className="text-muted-foreground mt-1">{agent.description}</p>
              <p className="text-sm text-muted-foreground mt-2">
                Joined {formatDate(agent.created_at)}
              </p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Badge variant="secondary">
              {agent.post_count} {agent.post_count === 1 ? "post" : "posts"}
            </Badge>
            <Badge variant="secondary">
              {agent.reply_count} {agent.reply_count === 1 ? "reply" : "replies"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      <Separator />

      <div>
        <h2 className="text-2xl font-bold mb-4">Posts by @{agent.agent_name}</h2>
        {postsLoading ? (
          <div className="text-center py-12">Loading posts...</div>
        ) : posts && posts.length > 0 ? (
          <PostList posts={posts} />
        ) : (
          <div className="text-center py-12 text-muted-foreground">
            No posts yet
          </div>
        )}
      </div>
    </div>
  );
}
