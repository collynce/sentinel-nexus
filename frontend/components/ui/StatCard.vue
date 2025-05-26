<template>
  <Card>
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle class="text-sm font-medium text-muted-foreground">
        {{ title }}
      </CardTitle>
      <div :class="`bg-${variant}/10 p-2 rounded-md`">
        <Icon :name="`lucide:${icon}`" :class="`h-4 w-4 text-${variant}`" />
      </div>
    </CardHeader>
    <CardContent>
      <div class="text-2xl font-bold">{{ value }}</div>
      <p v-if="trend" class="text-xs text-muted-foreground flex items-center mt-1">
        <span 
          :class="{
            'text-green-500': trendDirection === 'up',
            'text-red-500': trendDirection === 'down',
            'text-amber-500': trendDirection === 'neutral'
          }"
        >
          <Icon 
            :name="`lucide:${trendDirection === 'up' ? 'arrow-up' : trendDirection === 'down' ? 'arrow-down' : 'minus'}`" 
            class="h-3 w-3 mr-1 inline-block" 
          />
          {{ trend }}
        </span>
        <span class="ml-1">vs last period</span>
      </p>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">

defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String,
    default: 'activity'
  },
  trend: {
    type: String,
    default: ''
  },
  trendDirection: {
    type: String as () => 'up' | 'down' | 'neutral',
    default: 'neutral'
  },
  variant: {
    type: String,
    default: 'primary'
  }
})
</script>
