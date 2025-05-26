// Type definitions for useCopilot composable

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date | string
}

export interface ChatResponse {
  response: Message
  context: Record<string, unknown>
}

export function useCopilot(): {
  chat: (messages: Message[], context: Record<string, unknown>) => Promise<ChatResponse>
  isLoading: boolean
  error: Error | null
}
