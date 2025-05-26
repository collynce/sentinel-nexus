<template>
  <Card :class="{'border-primary': source.status === 'active'}">
    <CardHeader class="pb-2">
      <CardTitle class="text-lg flex items-center justify-between">
        <div class="flex items-center gap-2">
          <Icon :name="getSourceIcon(source.type)" class="h-5 w-5" />
          {{ source.name }}
        </div>
        <Badge :variant="getStatusVariant(source.status)">
          {{ source.status }}
        </Badge>
      </CardTitle>
      <CardDescription>{{ source.description }}</CardDescription>
    </CardHeader>
    <CardContent class="pb-2">
      <div class="space-y-2">
        <div class="grid grid-cols-2 gap-2 text-sm">
          <div>
            <p class="text-muted-foreground">Type</p>
            <p class="font-medium">{{ source.type }}</p>
          </div>
          <div>
            <p class="text-muted-foreground">Last Fetch</p>
            <p class="font-medium">{{ formatTime(source.lastFetch) }}</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2 text-sm">
          <div>
            <p class="text-muted-foreground">Items Collected</p>
            <p class="font-medium">{{ source.itemsCollected.toLocaleString() }}</p>
          </div>
          <div>
            <p class="text-muted-foreground">Threats Found</p>
            <p class="font-medium">{{ source.threatsFound.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </CardContent>
    <CardFooter class="flex justify-between">
      <Button variant="outline" size="sm">
        <Icon name="lucide:settings" class="mr-2 h-4 w-4" />
        Configure
      </Button>
      <Button variant="outline" size="sm" :disabled="source.status === 'fetching'">
        <Icon name="lucide:refresh-cw" class="mr-2 h-4 w-4" :class="{'animate-spin': source.status === 'fetching'}" />
        Refresh
      </Button>
    </CardFooter>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const props = defineProps({
  source: {
    type: Object,
    required: true
  }
})

function getSourceIcon(type) {
  const icons = {
    'news': 'lucide:newspaper',
    'social': 'lucide:message-circle',
    'dark_web': 'lucide:shield',
    'vulnerability': 'lucide:alert-triangle',
    'paste': 'lucide:clipboard',
    'feed': 'lucide:rss'
  }
  return icons[type.toLowerCase()] || 'lucide:database'
}

function getStatusVariant(status) {
  const variants = {
    'active': 'success',
    'inactive': 'secondary',
    'error': 'destructive',
    'fetching': 'warning'
  }
  return variants[status.toLowerCase()] || 'outline'
}

function formatTime(timestamp) {
  if (!timestamp) return 'Never'
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`
  
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `${diffDays}d ago`
  
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric'
  }).format(date)
}
</script>
