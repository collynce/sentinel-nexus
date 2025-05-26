import { ref } from 'vue'
import type { Ref } from 'vue'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export function useCopilot() {
  const isLoading = ref(false)
  const error = ref<Error | null>(null)
  const config = useRuntimeConfig()

  const chat = async (messages: Message[], context: Record<string, any> = {}): Promise<{
    response: Message
    context: Record<string, any>
  }> => {
    if (process.server) {
      return {
        response: {
          role: 'assistant',
          content: 'Chat is only available on the client side.',
          timestamp: new Date()
        },
        context: {}
      }
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${config.public.apiBaseUrl}/copilot/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          messages: messages.map(m => ({
            role: m.role,
            content: m.content,
            timestamp: m.timestamp.toISOString()
          })),
          context
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Convert the timestamp string back to a Date object
      return {
        response: {
          ...data.response,
          timestamp: new Date(data.response.timestamp)
        },
        context: data.context || {}
      }
    } catch (e) {
      const error = e as Error
      console.error('Error in copilot chat:', error)
      error.value = error
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    chat,
    isLoading,
    error
  }
}
