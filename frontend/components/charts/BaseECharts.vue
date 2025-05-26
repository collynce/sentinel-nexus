<template>
  <div ref="chartContainer" :style="{ height: height, width: width }" class="echarts-container"></div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, toRefs } from 'vue'
import * as echarts from 'echarts/core'
import {
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  MapChart,
  HeatmapChart,
  GraphChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
  ToolboxComponent,
  VisualMapComponent,
  GeoComponent,
  CalendarComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

// Register ECharts components
echarts.use([
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  MapChart,
  HeatmapChart,
  GraphChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
  ToolboxComponent,
  VisualMapComponent,
  GeoComponent,
  CalendarComponent,
  CanvasRenderer
])

const props = defineProps({
  option: {
    type: Object,
    required: true
  },
  theme: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '300px'
  },
  width: {
    type: String,
    default: '100%'
  },
  autoResize: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['chartReady', 'chartClick', 'chartMouseover', 'chartMouseout'])

const { option, theme, autoResize } = toRefs(props)
const chartContainer = ref(null)
let chartInstance = null

// Create chart instance
const initChart = () => {
  if (!chartContainer.value) return
  
  // Determine theme based on system/app preference if not explicitly set
  const isDark = document.documentElement.classList.contains('dark')
  const effectiveTheme = theme.value || (isDark ? 'dark' : '')
  
  chartInstance = echarts.init(chartContainer.value, effectiveTheme)
  
  // Register event handlers
  chartInstance.on('click', (params) => emit('chartClick', params))
  chartInstance.on('mouseover', (params) => emit('chartMouseover', params))
  chartInstance.on('mouseout', (params) => emit('chartMouseout', params))
  
  updateChart()
  emit('chartReady', chartInstance)
}

// Update chart with new options
const updateChart = () => {
  if (!chartInstance) return
  
  // Apply theme-aware defaults if not explicitly set
  const isDark = document.documentElement.classList.contains('dark')
  const defaultTextColor = isDark ? '#e2e8f0' : '#1e293b'
  const defaultAxisColor = isDark ? '#94a3b8' : '#64748b'
  const defaultSplitLineColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
  
  // Deep clone the option to avoid modifying the original
  const processedOption = JSON.parse(JSON.stringify(option.value))
  
  // Apply theme-aware defaults if not explicitly set
  if (!processedOption.textStyle) {
    processedOption.textStyle = { color: defaultTextColor }
  }
  
  // Apply theme-aware defaults to axes if they exist
  if (processedOption.xAxis && !processedOption.xAxis.axisLine) {
    processedOption.xAxis.axisLine = { lineStyle: { color: defaultAxisColor } }
    processedOption.xAxis.splitLine = { lineStyle: { color: defaultSplitLineColor } }
  }
  
  if (processedOption.yAxis && !processedOption.yAxis.axisLine) {
    processedOption.yAxis.axisLine = { lineStyle: { color: defaultAxisColor } }
    processedOption.yAxis.splitLine = { lineStyle: { color: defaultSplitLineColor } }
  }
  
  chartInstance.setOption(processedOption, true)
}

// Watch for option changes to update chart
watch(option, () => {
  updateChart()
}, { deep: true })

// Watch for theme changes
watch(theme, () => {
  if (chartInstance) {
    chartInstance.dispose()
    initChart()
  }
})

// Handle theme changes from system or app
const handleThemeChange = () => {
  if (chartInstance && !theme.value) {
    // Only auto-switch theme if no explicit theme is set
    chartInstance.dispose()
    initChart()
  }
}

// Handle window resize
const handleResize = () => {
  if (chartInstance && autoResize.value) {
    chartInstance.resize()
  }
}

onMounted(() => {
  initChart()
  
  if (autoResize.value) {
    window.addEventListener('resize', handleResize)
  }
  
  // Add theme change listeners
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange)
  document.addEventListener('theme-change', handleThemeChange)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  if (autoResize.value) {
    window.removeEventListener('resize', handleResize)
  }
  
  // Remove theme change listeners
  window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', handleThemeChange)
  document.removeEventListener('theme-change', handleThemeChange)
})

// Expose chart instance and methods to parent components
defineExpose({
  getChartInstance: () => chartInstance,
  resize: () => chartInstance?.resize(),
  clear: () => chartInstance?.clear(),
  dispose: () => chartInstance?.dispose()
})
</script>
