import { Message } from "./utils";

export async function streamLLMResponse(
  conversation: Message[],
  onChunk: (chunk: string) => void,
  signal?: AbortSignal
) {
  const response = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conversation }),
    signal,
  });

  if (!response.body) throw new Error("No response body");

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let done = false;
  let acc = "";

  while (!done) {
    const { value, done: doneReading } = await reader.read();
    done = doneReading;
    if (value) {
      acc += decoder.decode(value, { stream: true });
      // Parse SSE chunks
      const lines = acc.split("\n\n");
      acc = lines.pop() || "";
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") return;
          onChunk(data);
        }
      }
    }
  }
}
