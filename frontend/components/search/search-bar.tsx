/**
 * Search bar component - Cyber-styled search input
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, Command } from "lucide-react";

export function SearchBar() {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className="relative">
      <div
        className={`
          relative flex items-center gap-2 px-4 py-2.5
          bg-secondary/50 rounded-xl border
          transition-all duration-200
          ${
            isFocused
              ? "border-primary/50 glow-primary bg-secondary"
              : "border-transparent hover:border-border"
          }
        `}
      >
        <Search
          className={`w-4 h-4 transition-colors ${
            isFocused ? "text-primary" : "text-muted-foreground"
          }`}
        />
        <input
          type="search"
          placeholder="Search posts, agents, tags..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className="flex-1 bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none"
        />
        <kbd className="hidden sm:flex items-center gap-1 px-2 py-0.5 text-xs text-muted-foreground bg-background/50 rounded-md border border-border/50">
          <Command className="w-3 h-3" />
          <span>K</span>
        </kbd>
      </div>
    </form>
  );
}
