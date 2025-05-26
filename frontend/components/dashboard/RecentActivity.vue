<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:activity" class="h-5 w-5" />
        Recent Activity
      </CardTitle>
      <CardDescription>Latest threat intelligence updates</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <div v-for="(activity, index) in activities" :key="index" class="flex items-start gap-4 pb-4 border-b last:border-0 last:pb-0">
          <div :class="`bg-${getActivityColor(activity.type)}-100 dark:bg-${getActivityColor(activity.type)}-900/20 text-${getActivityColor(activity.type)}-700 dark:text-${getActivityColor(activity.type)}-400`" class="p-2 rounded-full">
            <Icon :name="getActivityIcon(activity.type)" class="h-4 w-4" />
          </div>
          <div class="space-y-1">
            <p class="text-sm font-medium">{{ activity.title }}</p>
            <p class="text-xs text-muted-foreground">{{ activity.description }}</p>
            <p class="text-xs text-muted-foreground">{{ formatTimeAgo(activity.timestamp) }}</p>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

const props = defineProps({
  activities: {
    type: Array,
    default: () => []
  }
})

function getActivityIcon(type) {
  const icons = {
    'threat': 'lucide:shield-alert',
    'source': 'lucide:database',
    'system': 'lucide:settings',
    'user': 'lucide:user'
  }
  return icons[type] || 'lucide:info'
}

function getActivityColor(type) {
  const colors = {
    'threat': 'red',
    'source': 'blue',
    'system': 'purple',
    'user': 'green'
  }
  return colors[type] || 'gray'
}

function formatTimeAgo(timestamp) {
  const now = new Date()
  const date = new Date(timestamp)
  const seconds = Math.floor((now - date) / 1000)
  
  if (seconds < 60) return 'just now'
  
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`
  
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`
  
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric'
  }).format(date)
}
</script>
