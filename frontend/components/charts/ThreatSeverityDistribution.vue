<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:pie-chart" class="h-5 w-5" />
        {{ title }}
      </CardTitle>
      <CardDescription>{{ description }}</CardDescription>
    </CardHeader>
    <CardContent>
      <ClientOnly>
        <BaseChartJs
          type="doughnut"
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
    default: 'Threat Severity Distribution'
  },
  description: {
    type: String,
    default: 'Distribution of threats by severity level'
  },
  data: {
    type: Object,
    required: true,
    // Expected format: { critical: 10, high: 25, medium: 40, low: 15, info: 5 }
  },
  height: {
    type: String,
    default: '250px'
  }
})

const chartData = computed(() => {
  return {
    labels: Object.keys(props.data).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
    datasets: [
      {
        data: Object.values(props.data),
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',  // Critical - red
          'rgba(249, 115, 22, 0.8)',  // High - orange
          'rgba(234, 179, 8, 0.8)',   // Medium - yellow
          'rgba(34, 197, 94, 0.8)',   // Low - green
          'rgba(148, 163, 184, 0.8)'  // Info - slate
        ],
        borderColor: [
          'rgb(239, 68, 68)',
          'rgb(249, 115, 22)',
          'rgb(234, 179, 8)',
          'rgb(34, 197, 94)',
          'rgb(148, 163, 184)'
        ],
        borderWidth: 1,
        hoverOffset: 4
      }
    ]
  }
})

const chartOptions = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  return {
    cutout: '65%',
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
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.raw || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((value / total) * 100);
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    }
  }
})
</script>
