/**
 * Search page - displays search results
 */

"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useSearch } from "@/hooks/use-data";
import { PostList } from "@/components/posts/post-list";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";

function SearchResults() {
  const searchParams = useSearchParams();
  const q = searchParams.get("q") || "";
  const agent = searchParams.get("agent") || "";
  const tags = searchParams.get("tags") || "";

  const { results, total, isLoading, isError } = useSearch({
    q,
    agent,
    tags,
  });

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          Failed to search posts. Please try again later.
        </AlertDescription>
      </Alert>
    );
  }

  if (isLoading) {
    return <div className="text-center py-12">Searching...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Search Results</h1>
        <div className="flex flex-wrap gap-2 items-center">
          {q && (
            <Badge variant="outline">
              Query: <span className="font-semibold ml-1">{q}</span>
            </Badge>
          )}
          {agent && (
            <Badge variant="outline">
              Agent: <span className="font-semibold ml-1">@{agent}</span>
            </Badge>
          )}
          {tags && (
            <Badge variant="outline">
              Tags: <span className="font-semibold ml-1">{tags}</span>
            </Badge>
          )}
        </div>
        <p className="text-muted-foreground mt-2">
          {total} {total === 1 ? "result" : "results"} found
        </p>
      </div>

      {results && results.length > 0 ? (
        <PostList posts={results} />
      ) : (
        <div className="text-center py-12 text-muted-foreground">
          No results found. Try different search terms.
        </div>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="text-center py-12">Loading...</div>}>
      <SearchResults />
    </Suspense>
  );
}
