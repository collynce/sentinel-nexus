<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:line-chart" class="h-5 w-5" />
        {{ title }}
      </CardTitle>
      <CardDescription>{{ description }}</CardDescription>
    </CardHeader>
    <CardContent>
      <ClientOnly>
        <BaseChartJs
          type="line"
          :data="chartData"
          :options="chartOptions"
          :height="height"
        />
      </ClientOnly>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import BaseChartJs from './BaseChartJs.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Threat Trend'
  },
  description: {
    type: String,
    default: 'Trend of threats detected over time'
  },
  data: {
    type: Array,
    required: true,
    // Expected format: [{ date: '2025-05-01', critical: 5, high: 10, medium: 15, low: 8 }, ...]
  },
  height: {
    type: String,
    default: '250px'
  }
})

const chartData = computed(() => {
  // Extract dates for labels
  const labels = props.data.map(item => {
    const date = new Date(item.date)
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' }).format(date)
  })
  
  // Get all severity types (excluding 'date')
  const severityTypes = Object.keys(props.data[0] || {}).filter(key => key !== 'date')
  
  // Create datasets for each severity type
  const datasets = severityTypes.map(type => {
    const color = getColorForSeverity(type)
    return {
      label: type.charAt(0).toUpperCase() + type.slice(1),
      data: props.data.map(item => item[type]),
      borderColor: color,
      backgroundColor: `${color}33`, // Add transparency
      tension: 0.3,
      fill: false,
      pointRadius: 3,
      pointHoverRadius: 5
    }
  })
  
  return {
    labels,
    datasets
  }
})

const chartOptions = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false
    },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          color: isDark ? '#e2e8f0' : '#1e293b',
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0
        }
      }
    }
  }
})

// Helper function to get color based on severity
function getColorForSeverity(severity) {
  const colors = {
    critical: 'rgb(239, 68, 68)',   // red
    high: 'rgb(249, 115, 22)',       // orange
    medium: 'rgb(234, 179, 8)',      // yellow
    low: 'rgb(34, 197, 94)',         // green
    info: 'rgb(148, 163, 184)'       // slate
  }
  return colors[severity.toLowerCase()] || 'rgb(59, 130, 246)' // Default to blue
}
</script>
