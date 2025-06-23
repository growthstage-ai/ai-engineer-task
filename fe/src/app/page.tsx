"use client";

import {
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
  ChatBubbleTimestamp,
} from "@/components/ui/chat/chat-bubble";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { Button } from "@/components/ui/button";
import { useChat } from "@/lib/useChat";

export default function Home() {
  const { messages, input, setInput, loading, sendMessage, handleKeyDown } =
    useChat();

  return (
    <main className="flex h-screen w-full max-w-3xl flex-col items-center mx-auto">
      <div className="flex flex-col w-full h-full flex-1 border rounded-lg mt-8 bg-background shadow-md">
        <ChatMessageList className="flex-1 min-h-0">
          {messages.map((msg) => (
            <ChatBubble
              key={msg.id}
              variant={msg.role === "user" ? "sent" : "received"}
            >
              <ChatBubbleAvatar
                fallback={msg.role === "user" ? "U" : "A"}
                className="w-8 h-8"
              />
              <div className="flex flex-col">
                <ChatBubbleMessage
                  variant={msg.role === "user" ? "sent" : "received"}
                  isLoading={
                    loading && msg.role === "assistant" && msg.content === ""
                  }
                >
                  {msg.content}
                </ChatBubbleMessage>
                <ChatBubbleTimestamp timestamp={msg.timestamp} />
              </div>
            </ChatBubble>
          ))}
        </ChatMessageList>
        <form
          className="flex items-center gap-2 p-4 border-t"
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
        >
          <ChatInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={loading}
            className="flex-1"
          />
          <Button type="submit" disabled={loading || !input.trim()}>
            Send
          </Button>
        </form>
      </div>
    </main>
  );
}
