/**
 * Reply tree component for displaying nested replies recursively
 */

import { ReplyItem } from "./reply-item";
import { Separator } from "@/components/ui/separator";
import type { Reply } from "@/lib/types";

interface ReplyTreeProps {
  replies: Reply[];
  depth?: number;
}

export function ReplyTree({ replies, depth = 0 }: ReplyTreeProps) {
  if (replies.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      {replies.map((reply, index) => (
        <div key={reply.reply_id}>
          <ReplyItem reply={reply} depth={depth} />
          {reply.replies && reply.replies.length > 0 && (
            <div className="mt-4">
              <ReplyTree replies={reply.replies} depth={depth + 1} />
            </div>
          )}
          {index < replies.length - 1 && <Separator className="my-4" />}
        </div>
      ))}
    </div>
  );
}
