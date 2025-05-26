<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:globe" class="h-5 w-5" />
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
          @click="handleChartClick"
        />
      </ClientOnly>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import * as echarts from 'echarts/core'

const props = defineProps({
  title: {
    type: String,
    default: 'Threat Geography Distribution'
  },
  description: {
    type: String,
    default: 'Distribution of threats by geographic location'
  },
  data: {
    type: Array,
    required: true,
    // Expected format: [{ name: 'United States', value: 120 }, { name: 'China', value: 80 }, ...]
  },
  height: {
    type: String,
    default: '400px'
  }
})

// Chart instance reference
const chartInstance = ref(null)

const chartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  
  // Sort data by value in descending order
  const sortedData = [...props.data].sort((a, b) => b.value - a.value)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} threats'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: isDark ? '#475569' : '#cbd5e1'
        }
      },
      axisLabel: {
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    yAxis: {
      type: 'category',
      data: sortedData.map(item => item.name),
      axisLine: {
        lineStyle: {
          color: isDark ? '#475569' : '#cbd5e1'
        }
      },
      axisLabel: {
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    series: [
      {
        name: 'Threats',
        type: 'bar',
        data: sortedData.map(item => item.value),
        itemStyle: {
          color: function(params) {
            // Color gradient based on value
            const value = params.value;
            const max = Math.max(...sortedData.map(item => item.value));
            const ratio = value / max;
            
            if (ratio > 0.7) return '#ef4444'; // red for high values
            if (ratio > 0.4) return '#f97316'; // orange for medium values
            return '#22c55e'; // green for low values
          }
        },
        label: {
          show: true,
          position: 'right',
          color: isDark ? '#e2e8f0' : '#1e293b'
        }
      }
    ]
  }
})

const handleChartClick = (params) => {
  console.log('Bar clicked:', params)
}
</script>
