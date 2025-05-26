<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:calendar-days" class="h-5 w-5" />
        {{ title }}
      </CardTitle>
      <CardDescription>{{ description }}</CardDescription>
    </CardHeader>
    <CardContent>
      <ClientOnly>
        <VChart
          :option="chartOption"
          :height="height"
          autoresize
        />
      </ClientOnly>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

const props = defineProps({
  title: {
    type: String,
    default: 'Threat Activity Calendar'
  },
  description: {
    type: String,
    default: 'Daily threat detection activity'
  },
  data: {
    type: Array,
    required: true,
    // Expected format: [['2025-05-01', 5], ['2025-05-02', 12], ...]
    // Each entry is [date, count]
  },
  height: {
    type: String,
    default: '250px'
  },
  range: {
    type: Array,
    default: () => {
      // Default to current month and previous 5 months
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 5)
      start.setDate(1)
      return [start.toISOString().split('T')[0], end.toISOString().split('T')[0]]
    }
  }
})

// Ensure data is properly formatted for ECharts
const formattedData = computed(() => {
  // Make sure each item is an array with exactly two elements: [date, value]
  return props.data.map(item => {
    if (Array.isArray(item) && item.length === 2) {
      return item;
    } else if (typeof item === 'object' && item.date && item.value !== undefined) {
      return [item.date, item.value];
    } else {
      console.warn('Invalid data format for calendar item:', item);
      return ['2025-01-01', 0]; // Default fallback to prevent errors
    }
  });
});

// Calculate max value for visualMap
const maxValue = computed(() => {
  const values = formattedData.value.map(item => item[1]);
  return Math.max(...values, 10);
});

const chartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false;
  
  return {
    tooltip: {
      position: 'top',
      formatter: function (params) {
        if (!params.data) return '';
        return `${params.data[0]}: ${params.data[1]} threats`;
      }
    },
    visualMap: {
      min: 0,
      max: maxValue.value,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      top: 'top',
      inRange: {
        color: ['#a5f3fc', '#0ea5e9', '#0369a1']
      },
      textStyle: {
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    calendar: {
      top: 60,
      left: 30,
      right: 30,
      cellSize: ['auto', 15],
      range: props.range,
      itemStyle: {
        borderWidth: 0.5,
        borderColor: isDark ? '#334155' : '#e2e8f0'
      },
      yearLabel: { show: true },
      dayLabel: {
        firstDay: 1,
        nameMap: 'en',
        color: isDark ? '#94a3b8' : '#64748b'
      },
      monthLabel: {
        nameMap: 'en',
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    series: [
      {
        type: 'heatmap',
        coordinateSystem: 'calendar',
        calendarIndex: 0,
        data: formattedData.value
      }
    ]
  };
});
</script>
