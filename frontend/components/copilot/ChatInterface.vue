<template>
  <div class="flex flex-col h-full">
    <!-- Chat Messages -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center">
        <div class="bg-primary/10 p-4 rounded-full mb-4">
          <Icon name="lucide:message-square" class="h-10 w-10 text-primary" />
        </div>
        <h3 class="text-lg font-medium">SOC Co-Pilot</h3>
        <p class="text-muted-foreground max-w-md mt-2">
          Ask questions about threats, request analysis, or get recommendations for security incidents.
        </p>
      </div>
      
      <div v-for="(message, index) in messages" :key="index" 
           :class="`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`">
        <div :class="`max-w-[80%] rounded-lg p-4 ${message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`">
          <div class="flex items-start gap-2">
            <Avatar v-if="message.role !== 'user'" class="h-8 w-8 mt-0.5">
              <AvatarImage src="/avatars/assistant.png" alt="Assistant" />
              <AvatarFallback>AI</AvatarFallback>
            </Avatar>
            <div>
              <div class="text-sm">
                <div v-html="formatMessage(message.content)"></div>
              </div>
              <div class="text-xs text-muted-foreground mt-1">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="isLoading" class="flex justify-start">
        <div class="max-w-[80%] rounded-lg p-4 bg-muted">
          <div class="flex items-center gap-2">
            <div class="flex space-x-1">
              <div class="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce"></div>
              <div class="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce delay-75"></div>
              <div class="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce delay-150"></div>
            </div>
            <span class="text-xs text-muted-foreground">Thinking...</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Input Area -->
    <div class="border-t p-4">
      <form @submit.prevent="sendMessage" class="flex gap-2">
        <div class="relative flex-1">
          <Textarea 
            v-model="userInput" 
            placeholder="Ask about threats, request analysis, or get recommendations..." 
            class="min-h-[80px] resize-none pr-12"
            :disabled="isLoading"
            @keydown="handleKeyDown"
          />
          <div class="absolute right-3 bottom-3 text-xs text-muted-foreground">
            Ctrl+Enter to send
          </div>
        </div>
        <Button 
          type="submit" 
          size="icon" 
          class="h-10 w-10 shrink-0 self-end"
          :disabled="isLoading || !userInput.trim()"
        >
          <Icon v-if="isLoading" name="lucide:loader-2" class="h-4 w-4 animate-spin" />
          <Icon v-else name="lucide:send" class="h-4 w-4" />
        </Button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { toast } from 'vue-sonner'
import { useBackendApi } from '../../composables/useBackendApi'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// Chat state
const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: 'Hello! I\'m your SOC Co-Pilot. How can I assist you with threat intelligence today?',
    timestamp: new Date()
  }
])

const userInput = ref('')
const isLoading = ref(false)
const error = ref<Error | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)

// Format message content with markdown support (basic implementation)
const formatMessage = (content: string) => {
  // Simple markdown to HTML conversion (very basic)
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
    .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
    .replace(/`([^`]+)`/g, '<code>$1</code>') // Inline code
    .replace(/\n/g, '<br>') // New lines
}


// Handle keyboard shortcuts
const handleKeyDown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && userInput.value.trim()) {
    sendMessage()
  }
}

// Send message to the API
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return
  
  const userMessage: Message = {
    role: 'user',
    content: userInput.value,
    timestamp: new Date()
  }
  
  // Add user message to chat
  messages.value.push(userMessage)
  const currentMessages = [...messages.value]
  userInput.value = ''
  isLoading.value = true
  
  // Scroll to bottom
  await nextTick()
  scrollToBottom()
  
  try {
    const api = useBackendApi()
    const response = await api.copilot.chat(
      currentMessages.map(m => ({
        role: m.role,
        content: m.content,
        timestamp: m.timestamp.toISOString()
      }))
    )
    
    // Add assistant's response to chat
    messages.value.push({
      role: 'assistant',
      content: response.response.content,
      timestamp: new Date()
    })
    
  } catch (err) {
    console.error('Error sending message:', err)
    toast.error('Failed to get response from the assistant. Please try again.')
    error.value = err as Error
  } finally {
    isLoading.value = false
    // Scroll to bottom after response
    await nextTick()
    scrollToBottom()
  }
}

// Scroll chat to bottom
const scrollToBottom = () => {
  return content.replace(
    /(https?:\/\/[^\s]+)/g, 
    '<a href="$1" target="_blank" class="text-primary underline">$1</a>'
  )
}

function formatTime(timestamp) {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(timestamp)
}


// Scroll to bottom on initial load
onMounted(() => {
  scrollToBottom()
})
</script>
