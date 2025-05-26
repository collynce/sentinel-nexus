<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:network" class="h-5 w-5" />
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
          @click="handleNodeClick"
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
    default: 'Threat Relationship Network'
  },
  description: {
    type: String,
    default: 'Connections between threats, actors, and campaigns'
  },
  data: {
    type: Object,
    required: true,
    // Expected format: { nodes: [...], links: [...] }
    // nodes: [{ id: '1', name: 'DanaBot', category: 'malware', value: 20 }, ...]
    // links: [{ source: '1', target: '2', value: 5 }, ...]
  },
  height: {
    type: String,
    default: '500px'
  }
})

const emit = defineEmits(['nodeClick'])

const chartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  
  // Define category colors
  const categoryColors = {
    'malware': '#ef4444',      // red
    'campaign': '#f97316',     // orange
    'actor': '#3b82f6',        // blue
    'vulnerability': '#eab308', // yellow
    'target': '#a855f7',       // purple
    'ioc': '#10b981'           // emerald
  }
  
  // Create categories array from unique categories in nodes
  const categories = [...new Set(props.data.nodes.map(node => node.category))]
    .map(category => ({
      name: category,
      itemStyle: {
        color: categoryColors[category] || '#94a3b8' // Default to slate if category not found
      }
    }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `<strong>${params.data.name}</strong><br/>
                  Type: ${params.data.category}<br/>
                  ${params.data.description || ''}`
        } else if (params.dataType === 'edge') {
          return `${params.data.source} → ${params.data.target}<br/>
                  ${params.data.description || ''}`
        }
        return ''
      }
    },
    legend: {
      data: categories.map(category => category.name),
      textStyle: {
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        name: 'Threat Network',
        type: 'graph',
        layout: 'force',
        data: props.data.nodes,
        links: props.data.links,
        categories: categories,
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          fontSize: 12,
          color: isDark ? '#e2e8f0' : '#1e293b'
        },
        force: {
          repulsion: 100,
          edgeLength: [50, 100]
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3,
          opacity: 0.7
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  }
})

const handleNodeClick = (params) => {
  if (params.dataType === 'node') {
    emit('nodeClick', params.data)
  }
}
</script>
