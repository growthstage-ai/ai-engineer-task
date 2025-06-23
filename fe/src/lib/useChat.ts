import { useRef, useState } from "react";
import { Message, getTimestamp } from "./utils";
import { streamLLMResponse } from "./llm";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input,
      timestamp: getTimestamp(),
    };

    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setLoading(true);

    // Prepare for streaming
    const assistantMsg: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      timestamp: getTimestamp(),
    };
    setMessages((msgs) => [...msgs, assistantMsg]);

    abortRef.current = new AbortController();

    try {
      await streamLLMResponse(
        [...messages, userMsg],
        (chunk) => {
          setMessages((msgs) =>
            msgs.map((msg, i) =>
              i === msgs.length - 1 && msg.role === "assistant"
                ? { ...msg, content: msg.content + chunk }
                : msg
            )
          );
        },
        abortRef.current.signal
      );
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setMessages((msgs) => [
        ...msgs,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Error: Unable to get response from LLM.",
          timestamp: getTimestamp(),
        },
      ]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return {
    messages,
    input,
    setInput,
    loading,
    sendMessage,
    handleKeyDown,
  };
}
