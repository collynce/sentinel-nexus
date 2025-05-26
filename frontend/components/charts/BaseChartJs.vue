<template>
  <div class="chart-container" :style="{ height: height, width: width }">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, toRefs } from 'vue'
import { Chart, registerables } from 'chart.js'

// Register Chart.js components
Chart.register(...registerables)

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['bar', 'line', 'pie', 'doughnut', 'radar', 'polarArea', 'bubble', 'scatter'].includes(value)
  },
  data: {
    type: Object,
    required: true
  },
  options: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: String,
    default: '300px'
  },
  width: {
    type: String,
    default: '100%'
  }
})

const { type, data, options } = toRefs(props)
const chartCanvas = ref(null)
let chartInstance = null

// Create chart instance
const createChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }

  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  
  // Apply theme-aware colors if not explicitly set
  const isDark = document.documentElement.classList.contains('dark')
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    color: isDark ? '#ffffff' : '#0f172a',
    scales: {
      x: {
        ticks: {
          color: isDark ? '#94a3b8' : '#64748b'
        },
        grid: {
          color: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
        }
      },
      y: {
        ticks: {
          color: isDark ? '#94a3b8' : '#64748b'
        },
        grid: {
          color: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
        }
      }
    }
  }

  // Merge default options with user options
  const mergedOptions = {
    ...defaultOptions,
    ...options.value
  }

  chartInstance = new Chart(ctx, {
    type: type.value,
    data: data.value,
    options: mergedOptions
  })
}

// Watch for data changes to update chart
watch([data, options], () => {
  if (chartInstance) {
    chartInstance.data = data.value
    chartInstance.options = { ...chartInstance.options, ...options.value }
    chartInstance.update()
  }
}, { deep: true })

// Watch for theme changes
const handleThemeChange = () => {
  if (chartInstance) {
    createChart()
  }
}

onMounted(() => {
  createChart()
  
  // Add theme change listener
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange)
  document.addEventListener('theme-change', handleThemeChange)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  // Remove theme change listener
  window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', handleThemeChange)
  document.removeEventListener('theme-change', handleThemeChange)
})
</script>
