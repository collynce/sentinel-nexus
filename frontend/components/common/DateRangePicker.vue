<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button variant="outline" class="w-full justify-start text-left font-normal">
        <Icon name="lucide:calendar" class="mr-2 h-4 w-4" />
        <span>{{ formattedDateRange }}</span>
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-auto p-0" align="start">
      <Calendar
        mode="range"
        v-model:selected-range="selectedRange"
        :num-days="42"
        class="rounded-md border"
      />
    </PopoverContent>
  </Popover>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      from: new Date(new Date().setDate(new Date().getDate() - 30)),
      to: new Date()
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const selectedRange = ref({
  from: props.modelValue.from,
  to: props.modelValue.to
})

const formattedDateRange = computed(() => {
  const from = selectedRange.value.from
  const to = selectedRange.value.to
  
  if (!from && !to) {
    return 'Select date range'
  }
  
  const formatDate = (date) => {
    if (!date) return ''
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(date)
  }
  
  if (from && !to) {
    return `From ${formatDate(from)}`
  }
  
  if (from && to) {
    return `${formatDate(from)} - ${formatDate(to)}`
  }
  
  return 'Select date range'
})

// Watch for changes in the selected range and emit update events
watch(selectedRange, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// Watch for changes in the model value from parent
watch(() => props.modelValue, (newValue) => {
  if (newValue.from !== selectedRange.value.from || newValue.to !== selectedRange.value.to) {
    selectedRange.value = {
      from: newValue.from,
      to: newValue.to
    }
  }
}, { deep: true })
</script>
