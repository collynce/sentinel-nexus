<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">SOC Co-Pilot</h1>
        <p class="text-muted-foreground">AI-powered security operations assistant</p>
      </div>
      <Button 
        variant="outline" 
        :disabled="isLoading"
        @click="startNewConversation"
      >
        <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
        New Conversation
      </Button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 h-[calc(100vh-12rem)]">
      <!-- Sidebar with conversation history -->
      <div class="hidden md:block border rounded-lg overflow-hidden">
        <div class="p-4 border-b bg-muted/50 flex justify-between items-center">
          <h3 class="font-medium">Recent Conversations</h3>
          <Button 
            variant="ghost" 
            size="icon" 
            class="h-8 w-8"
            :disabled="isLoading"
            @click="refreshConversations"
          >
            <Icon name="lucide:refresh-ccw" class="h-4 w-4" :class="{ 'animate-spin': isLoading }" />
          </Button>
        </div>
        <div class="p-2 space-y-1 overflow-y-auto max-h-[calc(100vh-16rem)]">
          <div v-if="conversations.length === 0" class="text-center p-4 text-muted-foreground text-sm">
            No conversations yet
          </div>
          <Button 
            v-for="conv in conversations" 
            :key="conv.id"
            variant="ghost" 
            class="w-full justify-start text-left h-auto py-3 group"
            :class="{ 'bg-accent': currentConversationId === conv.id }"
            @click="loadConversation(conv.id)"
          >
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start">
                <div class="font-medium truncate">
                  {{ conv.title || 'New Conversation' }}
                </div>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  class="h-6 w-6 opacity-0 group-hover:opacity-100"
                  @click.stop="deleteConversation(conv.id)"
                >
                  <Icon name="lucide:trash-2" class="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              </div>
              <div class="text-xs text-muted-foreground truncate">
                {{ formatLastMessage(conv.lastMessage) }}
              </div>
              <div class="text-xs text-muted-foreground mt-1">
                {{ formatDate(conv.updatedAt) }}
              </div>
            </div>
          </Button>
        </div>
      </div>
      
      <!-- Main chat interface -->
      <div class="md:col-span-3 border rounded-lg overflow-hidden flex flex-col h-full">
        <ChatInterface 
          v-if="currentConversationId"
          :key="currentConversationId"
          :conversation-id="currentConversationId"
          @new-message="handleNewMessage"
          @conversation-updated="refreshConversations"
        />
        <div v-else class="flex-1 flex items-center justify-center text-muted-foreground">
          <p>Select a conversation or create a new one to get started</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import ChatInterface from '@/components/copilot/ChatInterface.vue'
import { useBackendApi } from '~/composables/useBackendApi'

const { copilot } = useBackendApi()

// State
const isLoading = ref(false)
const conversations = ref([])
const currentConversationId = ref<string | null>(null)

// Format date for display
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) {
    return 'Today, ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (diffInDays === 1) {
    return 'Yesterday, ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (diffInDays < 7) {
    return date.toLocaleDateString([], { weekday: 'long', hour: '2-digit', minute: '2-digit' })
  } else {
    return date.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' })
  }
}

// Format last message preview
const formatLastMessage = (message: string) => {
  if (!message) return 'No messages yet'
  // Remove markdown and trim
  return message
    .replace(/[#*`_\[\]()]/g, '')
    .replace(/\n/g, ' ')
    .substring(0, 60)
    .trim() + (message.length > 60 ? '...' : '')
}

// Fetch conversations
const fetchConversations = async () => {
  try {
    isLoading.value = true
    const data = await copilot.getConversations()
    conversations.value = data
    
    // If no conversation is selected, select the most recent one
    if (conversations.value.length > 0 && !currentConversationId.value) {
      currentConversationId.value = conversations.value[0].id
    }
  } catch (error) {
    console.error('Failed to fetch conversations:', error)
    // toast({
    //   title: 'Error',
    //   description: 'Failed to load conversations',
    //   variant: 'destructive',
    // })
  } finally {
    isLoading.value = false
  }
}

// Start a new conversation
const startNewConversation = async () => {
  try {
    isLoading.value = true
    
    // Create a new conversation with a default title
    const newConv = {
      title: 'New Conversation',
      messages: [{
        role: 'assistant',
        content: 'Hello! I\'m your SOC Co-Pilot. How can I assist you with threat intelligence today?',
        timestamp: new Date().toISOString()
      }]
    }
    
    // In a real implementation, you would save this to the backend
    // For now, we'll just create a local ID
    const tempId = `conv-${Date.now()}`
    conversations.value.unshift({
      id: tempId,
      ...newConv,
      updatedAt: new Date().toISOString(),
      messageCount: 1
    })
    
    currentConversationId.value = tempId
  } catch (error) {
    console.error('Failed to create new conversation:', error)
    // toast({
    //   title: 'Error',
    //   description: 'Failed to create a new conversation',
    //   variant: 'destructive',
    // })
  } finally {
    isLoading.value = false
  }
}

// Load a specific conversation
const loadConversation = (conversationId: string) => {
  currentConversationId.value = conversationId
}

// Delete a conversation
const deleteConversation = async (conversationId: string) => {
  try {
    // In a real implementation, you would call the API to delete
    // await copilot.deleteConversation(conversationId)
    
    // For now, just remove it from the local state
    const index = conversations.value.findIndex(c => c.id === conversationId)
    if (index !== -1) {
      conversations.value.splice(index, 1)
    }
    
    // If we deleted the current conversation, select another one
    if (currentConversationId.value === conversationId) {
      currentConversationId.value = conversations.value[0]?.id || null
    }
    
    // toast({
    //   title: 'Conversation deleted',
    // })
  } catch (error) {
    console.error('Failed to delete conversation:', error)
    // toast({
    //   title: 'Error',
    //   description: 'Failed to delete conversation',
    //   variant: 'destructive',
    // })
  }
}

// Handle new messages from the chat interface
const handleNewMessage = async (message) => {
  try {
    // Update the last message in the conversation list
    const convIndex = conversations.value.findIndex(c => c.id === currentConversationId.value)
    if (convIndex !== -1) {
      conversations.value[convIndex].lastMessage = message.content
      conversations.value[convIndex].updatedAt = new Date().toISOString()
      
      // Keep the updated conversation at the top
      const updated = conversations.value.splice(convIndex, 1)[0]
      conversations.value.unshift(updated)
    }
  } catch (error) {
    console.error('Error updating conversation:', error)
  }
}

// Refresh conversations
const refreshConversations = () => {
  fetchConversations()
}

// Initial load
onMounted(() => {
  fetchConversations()
})
</script>
