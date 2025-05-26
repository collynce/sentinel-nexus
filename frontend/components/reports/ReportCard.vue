<template>
  <Card class="h-full flex flex-col">
    <CardHeader>
      <div class="flex justify-between items-start">
        <div>
          <CardTitle class="text-lg">{{ report.title }}</CardTitle>
          <CardDescription>{{ formatDate(report.createdAt) }}</CardDescription>
        </div>
        <Badge>{{ report.type }}</Badge>
      </div>
    </CardHeader>
    <CardContent class="flex-grow">
      <p class="text-sm text-muted-foreground line-clamp-3">{{ report.summary }}</p>
      
      <div class="mt-4 flex flex-wrap gap-2">
        <Badge v-for="tag in report.tags" :key="tag" variant="outline" class="text-xs">
          {{ tag }}
        </Badge>
      </div>
    </CardContent>
    <CardFooter class="border-t pt-4">
      <div class="flex justify-between items-center w-full">
        <div class="flex items-center gap-2">
          <Avatar class="h-6 w-6">
            <AvatarImage :src="report.author.avatar" />
            <AvatarFallback>{{ getInitials(report.author.name) }}</AvatarFallback>
          </Avatar>
          <span class="text-xs text-muted-foreground">{{ report.author.name }}</span>
        </div>
        <Button variant="ghost" size="sm" @click="navigateTo(`/reports/${report.id}`)">
          <Icon name="lucide:chevron-right" class="h-4 w-4" />
        </Button>
      </div>
    </CardFooter>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

const props = defineProps({
  report: {
    type: Object,
    required: true
  }
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

function getInitials(name) {
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
}
</script>
