// import { useRuntimeConfig } from '#app'

interface CopilotMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp?: string
}

interface CopilotContext {
  [key: string]: any
}

interface CopilotResponse {
  response: CopilotMessage
  context: CopilotContext
}

interface CopilotConversation {
  id: string
  title: string
  createdAt: string
  updatedAt: string
  messageCount: number
}

/**
 * Composable for interacting with the Sentinel Nexus backend API
 */
export function useBackendApi() {
  const config = process.client ? useRuntimeConfig() : { public: { apiBaseUrl: 'http://localhost:8000/api/v1' } }
  const baseUrl = config.public.apiBaseUrl || 'http://localhost:8000/api/v1'
  
  /**
   * Generic fetch wrapper with error handling
   */
  async function apiFetch(endpoint: string, options: any = {}) {
    try {
      const url = `${baseUrl}${endpoint}`
      const response = await $fetch(url, {
        ...options,
        // Add any auth headers or other common options here
        onResponseError({ response }) {
          throw new Error(`API Error: ${response.status} ${response._data?.detail || 'Unknown error'}`)
        }
      })
      return response
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }
  
  // Threat-related API functions
  const threats = {
    getAll: (params = {}) => apiFetch('/threats', { params }),
    getById: (id: string) => apiFetch(`/threats/${id}`),
    create: (data: any) => apiFetch('/threats', { method: 'POST', body: data }),
    update: (id: string, data: any) => apiFetch(`/threats/${id}`, { method: 'PUT', body: data }),
    delete: (id: string) => apiFetch(`/threats/${id}`, { method: 'DELETE' })
  }
  
  // Analysis-related API functions
  const analysis = {
    submit: (data: any) => apiFetch('/analysis', { method: 'POST', body: data }),
    getResults: (params = {}) => apiFetch('/analysis/results', { params }),
    getResultById: (id: string) => apiFetch(`/analysis/results/${id}`),
    extractIocs: (text: string) => apiFetch('/analysis/extract-iocs', { method: 'POST', body: { text } })
  }
  
  // Sources-related API functions
  const sources = {
    getAll: (params = {}) => apiFetch('/sources', { params }),
    getById: (id: string) => apiFetch(`/sources/${id}`),
    create: (data: any) => apiFetch('/sources', { method: 'POST', body: data }),
    update: (id: string, data: any) => apiFetch(`/sources/${id}`, { method: 'PUT', body: data }),
    delete: (id: string) => apiFetch(`/sources/${id}`, { method: 'DELETE' })
  }
  
  // Actions-related API functions
  const actions = {
    getAll: (params = {}) => apiFetch('/actions', { params }),
    getById: (id: string) => apiFetch(`/actions/${id}`),
    create: (data: any) => apiFetch('/actions', { method: 'POST', body: data }),
    execute: (id: string) => apiFetch(`/actions/${id}/execute`, { method: 'POST' })
  }

  // Copilot-related API functions
  const copilot = {
    /**
     * Send a chat message to the copilot
     * @param messages Array of message objects with role and content
     * @param context Optional conversation context
     * @returns Promise with the assistant's response
     */
    chat: (messages: CopilotMessage[], context: CopilotContext = {}): Promise<CopilotResponse> => 
      apiFetch('/copilot/chat', { 
        method: 'POST', 
        body: { 
          messages: messages.map(m => ({
            role: m.role,
            content: m.content,
            timestamp: m.timestamp || new Date().toISOString()
          })),
          context 
        } 
      }),

    /**
     * Get conversation history
     * @param limit Number of conversations to return
     * @param offset Pagination offset
     * @returns Promise with list of conversations
     */
    getConversations: (params: { limit?: number; offset?: number } = {}) => 
      apiFetch('/copilot/conversations', { params }),
      
    /**
     * Get a specific conversation by ID
     * @param id Conversation ID
     * @returns Promise with conversation details and messages
     */
    getConversation: (id: string) => 
      apiFetch(`/copilot/conversations/${id}`),
      
    /**
     * Delete a conversation
     * @param id Conversation ID
     * @returns Promise indicating success
     */
    deleteConversation: (id: string) =>
      apiFetch(`/copilot/conversations/${id}`, { method: 'DELETE' }),
      
    /**
     * Generate a title for a conversation based on messages
     * @param messages Array of messages
     * @returns Promise with generated title
     */
    generateTitle: (messages: CopilotMessage[]) =>
      apiFetch('/copilot/generate-title', { 
        method: 'POST',
        body: { messages }
      })
  }
  
  return {
    threats,
    analysis,
    sources,
    actions,
    copilot,
    apiFetch
  }
}
