<template>
  <Card class="overflow-hidden">
    <CardHeader :class="`bg-${color}-50 dark:bg-${color}-950/20`" class="p-4">
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon :name="icon" class="h-5 w-5" />
        {{ title }}
      </CardTitle>
    </CardHeader>
    <CardContent class="p-4 pt-3">
      <div class="flex justify-between items-center">
        <div class="text-3xl font-bold">{{ count }}</div>
        <Badge :variant="trendVariant" class="flex items-center gap-1">
          <Icon v-if="trendDirection === 'up'" name="lucide:trending-up" class="h-3 w-3" />
          <Icon v-else name="lucide:trending-down" class="h-3 w-3" />
          {{ trend }}
        </Badge>
      </div>
      <p v-if="description" class="text-sm text-muted-foreground mt-1">{{ description }}</p>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: [Number, String],
    required: true
  },
  trend: {
    type: String,
    default: '0%'
  },
  description: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: 'blue'
  },
  icon: {
    type: String,
    default: 'lucide:alert-circle'
  }
})

const trendDirection = computed(() => {
  if (props.trend.startsWith('-')) return 'down'
  return 'up'
})

const trendVariant = computed(() => {
  if (trendDirection.value === 'down') return 'success'
  return 'destructive'
})
</script>
