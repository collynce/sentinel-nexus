<template>
  <div class="rounded-lg border bg-card text-card-foreground shadow-sm">
    <div class="p-6">
      <div class="flex items-center justify-between space-y-2">
        <h3 class="text-sm font-medium text-muted-foreground">
          {{ title }}
        </h3>
        <div class="h-4 w-4 text-muted-foreground">
          <Icon :name="icon" class="h-4 w-4" />
        </div>
      </div>
      <div class="mt-2">
        <div class="text-2xl font-bold">{{ value.toLocaleString() }}</div>
        <p 
          v-if="typeof change === 'number'" 
          class="text-xs mt-1 inline-flex items-center"
          :class="{
            'text-green-600 dark:text-green-400': changeType === 'increase',
            'text-red-600 dark:text-red-400': changeType === 'decrease',
          }"
        >
          <Icon 
            :name="changeType === 'increase' ? 'lucide:trending-up' : 'lucide:trending-down'" 
            class="h-3 w-3 mr-1" 
          />
          {{ Math.abs(change) }}% {{ changeType === 'increase' ? 'increase' : 'decrease' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  change: {
    type: Number,
    default: null
  },
  changeType: {
    type: String,
    validator: (val: string | null) => ['increase', 'decrease', null].includes(val),
    default: null
  },
  icon: {
    type: String,
    default: 'lucide:activity'
  },
  variant: {
    type: String,
    default: 'default',
    validator: (val) => ['default', 'destructive', 'warning', 'success'].includes(val)
  }
});
</script>
