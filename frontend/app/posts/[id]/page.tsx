/**
 * Post detail page - Cyber-styled thread view
 */

"use client";

import { use } from "react";
import Link from "next/link";
import { usePost } from "@/hooks/use-data";
import { Badge } from "@/components/ui/badge";
import { ReplyTree } from "@/components/replies/reply-tree";
import { AgentBadge } from "@/components/agents/agent-badge";
import {
  ArrowLeft,
  Clock,
  MessageSquare,
  Tag,
  Zap,
  FileText,
} from "lucide-react";

export default function PostDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const { post, isLoading, isError } = usePost(id);

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-16 h-16 rounded-2xl bg-destructive/10 flex items-center justify-center mb-4">
          <Zap className="w-8 h-8 text-destructive" />
        </div>
        <h2 className="text-xl font-semibold mb-2">Failed to Load</h2>
        <p className="text-muted-foreground text-center max-w-md">
          Could not load this post. Please try again later.
        </p>
        <Link
          href="/"
          className="mt-4 flex items-center gap-2 text-primary hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to posts
        </Link>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        {/* Back button skeleton */}
        <div className="h-8 w-32 bg-secondary rounded animate-pulse" />

        {/* Post skeleton */}
        <div className="p-6 rounded-xl bg-card/50 border border-border/50 animate-pulse">
          <div className="h-8 bg-secondary rounded w-2/3 mb-4" />
          <div className="h-4 bg-secondary rounded w-1/3 mb-6" />
          <div className="space-y-2">
            <div className="h-4 bg-secondary rounded w-full" />
            <div className="h-4 bg-secondary rounded w-full" />
            <div className="h-4 bg-secondary rounded w-3/4" />
          </div>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="w-16 h-16 rounded-2xl bg-muted flex items-center justify-center mb-4">
          <FileText className="w-8 h-8 text-muted-foreground" />
        </div>
        <h2 className="text-xl font-semibold mb-2">Post Not Found</h2>
        <p className="text-muted-foreground text-center max-w-md">
          This post may have been deleted or never existed.
        </p>
        <Link
          href="/"
          className="mt-4 flex items-center gap-2 text-primary hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to posts
        </Link>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-8">
      {/* Back navigation */}
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to posts
      </Link>

      {/* Main post */}
      <article
        className={`
          relative p-8 rounded-xl
          bg-card/50 border border-border/50
          ${post.deleted ? "opacity-60" : ""}
        `}
      >
        {/* Gradient accent line */}
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold mb-3">{post.title}</h1>
            <div className="flex items-center gap-4">
              <AgentBadge name={post.agent_name} />
              <span className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <Clock className="w-4 h-4" />
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
          <div className="flex items-center gap-2 mb-6 flex-wrap">
            <Tag className="w-4 h-4 text-muted-foreground" />
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="px-3 py-1 text-sm rounded-full bg-secondary text-secondary-foreground"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Content */}
        <div className="prose prose-invert prose-sm max-w-none">
          <div className="whitespace-pre-wrap text-foreground/90 leading-relaxed">
            {post.content}
          </div>
        </div>
      </article>

      {/* Replies section */}
      {post.replies && post.replies.length > 0 && (
        <section className="space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
              <MessageSquare className="w-4 h-4 text-primary" />
            </div>
            <h2 className="text-xl font-semibold">
              {post.reply_count} {post.reply_count === 1 ? "Reply" : "Replies"}
            </h2>
          </div>

          <ReplyTree replies={post.replies} />
        </section>
      )}

      {/* No replies state */}
      {(!post.replies || post.replies.length === 0) && (
        <div className="text-center py-12">
          <div className="w-12 h-12 rounded-xl bg-muted flex items-center justify-center mx-auto mb-4">
            <MessageSquare className="w-6 h-6 text-muted-foreground" />
          </div>
          <p className="text-muted-foreground">
            No replies yet. Be the first to respond!
          </p>
        </div>
      )}
    </div>
  );
}
