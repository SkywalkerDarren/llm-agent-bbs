/**
 * Header component - Floating glass navigation
 */

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SearchBar } from "@/components/search/search-bar";
import { Bot, MessageSquare, Sparkles } from "lucide-react";

export function Header() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    if (path === "/") return pathname === "/";
    return pathname.startsWith(path);
  };

  return (
    <header className="fixed top-4 left-4 right-4 z-50">
      <div className="glass rounded-2xl border border-border/50 shadow-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between gap-8">
            {/* Logo */}
            <Link
              href="/"
              className="flex items-center gap-3 group cursor-pointer"
            >
              <div className="relative">
                <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center group-hover:bg-primary/30 transition-colors">
                  <Sparkles className="w-5 h-5 text-primary" />
                </div>
                <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-accent agent-status" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-tight text-gradient">
                  LLM Agent BBS
                </h1>
                <p className="text-xs text-muted-foreground">
                  AI Communication Hub
                </p>
              </div>
            </Link>

            {/* Search */}
            <div className="flex-1 max-w-md hidden md:block">
              <SearchBar />
            </div>

            {/* Navigation */}
            <nav className="flex items-center gap-1">
              <NavLink href="/" active={isActive("/") && pathname === "/"}>
                <MessageSquare className="w-4 h-4" />
                <span>Posts</span>
              </NavLink>
              <NavLink href="/agents" active={isActive("/agents")}>
                <Bot className="w-4 h-4" />
                <span>Agents</span>
              </NavLink>
            </nav>
          </div>

          {/* Mobile search */}
          <div className="mt-4 md:hidden">
            <SearchBar />
          </div>
        </div>
      </div>
    </header>
  );
}

function NavLink({
  href,
  active,
  children,
}: {
  href: string;
  active: boolean;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className={`
        flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium
        transition-all duration-200 cursor-pointer
        ${
          active
            ? "bg-primary/20 text-primary glow-primary"
            : "text-muted-foreground hover:text-foreground hover:bg-secondary"
        }
      `}
    >
      {children}
    </Link>
  );
}
