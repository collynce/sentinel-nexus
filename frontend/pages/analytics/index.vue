<template>
  <div class="container py-6 space-y-6">
    <!-- Header with title and actions -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Threat Intelligence Analytics</h1>
        <p class="text-muted-foreground">Analyze and visualize threat data patterns</p>
      </div>
      <div class="flex items-center gap-2 w-full md:w-auto">
        <Input 
          v-model="searchQuery" 
          placeholder="Search threats..." 
          class="w-full md:w-[300px]"
        >
          <template #left>
            <Icon name="lucide:search" class="h-4 w-4 text-muted-foreground" />
          </template>
        </Input>
        <DateRangePicker v-model="filters.dateRange" class="w-[200px]" />
        <Button variant="outline" size="icon" @click="refreshData">
          <Icon name="lucide:refresh-cw" class="h-4 w-4" :class="{ 'animate-spin': loading }" />
        </Button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard 
        title="Total Threats" 
        :value="filteredThreats.length" 
        :change="12" 
        changeType="increase" 
        icon="shield-alert"
      />
      <StatCard 
        title="Critical" 
        :value="threatsBySeverity.critical || 0" 
        :change="8" 
        changeType="increase" 
        icon="alert-octagon"
        variant="destructive"
      />
      <StatCard 
        title="High Severity" 
        :value="threatsBySeverity.high || 0" 
        :change="-3" 
        changeType="decrease" 
        icon="alert-triangle"
        variant="warning"
      />
      <StatCard 
        title="Active Campaigns" 
        :value="activeCampaigns" 
        :change="2" 
        changeType="increase" 
        icon="activity"
      />
    </div>

    <!-- Filters -->
    <Card>
      <CardContent class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <Label for="severity-filter">Severity</Label>
            <Select id="severity-filter" v-model="filters.severity">
              <option value="all">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </Select>
          </div>
          <div>
            <Label for="type-filter">Threat Type</Label>
            <Select id="type-filter" v-model="filters.type">
              <option value="all">All Types</option>
              <option value="malware">Malware</option>
              <option value="phishing">Phishing</option>
              <option value="vulnerability">Vulnerability</option>
              <option value="apt">APT</option>
            </Select>
          </div>
          <div>
            <Label for="source-filter">Data Source</Label>
            <Select id="source-filter" v-model="filters.source">
              <option value="all">All Sources</option>
              <option value="osint">OSINT</option>
              <option value="internal">Internal</option>
              <option value="partner">Partner Feeds</option>
            </Select>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Visualization Tabs -->
    <!-- Main Content -->
    <div class="grid gap-6">
      <!-- Charts Row 1 -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Severity Distribution -->
        <Card>
          <CardHeader>
            <CardTitle>Threat Severity Distribution</CardTitle>
          </CardHeader>
          <CardContent class="h-[300px]">
            <ThreatSeverityDistribution :data="severityData" />
          </CardContent>
        </Card>

        <!-- Trend Chart -->
        <Card>
          <CardHeader>
            <div class="flex justify-between items-center">
              <CardTitle>Threats Over Time</CardTitle>
              <Select v-model="trendTimeRange" class="w-[180px]">
                <SelectTrigger>
                  <SelectValue placeholder="Select time range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                  <SelectItem value="1y">Last year</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent class="h-[300px]">
            <ThreatTrendChart :data="trendData" />
          </CardContent>
        </Card>
      </div>

      <!-- Geography Map -->
      <Card>
        <CardHeader>
          <CardTitle>Geographic Threat Distribution</CardTitle>
        </CardHeader>
        <CardContent class="h-[500px]">
          <ThreatGeographyMap :data="geoData" />
        </CardContent>
      </Card>

      <!-- Network Graph -->
      <Card>
        <CardHeader>
          <CardTitle>Threat Relationships</CardTitle>
          <CardDescription>Visualizing connections between threats and indicators</CardDescription>
        </CardHeader>
        <CardContent class="h-[600px]">
          <ThreatNetworkGraph 
            :data="networkData" 
            @node-click="handleNodeClick"
          />
        </CardContent>
      </Card>

      <!-- Recent Threats -->
      <Card>
        <CardHeader>
          <CardTitle>Recent Threats</CardTitle>
          <CardDescription>Most recently identified threats and campaigns</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <ThreatCard 
              v-for="threat in paginatedThreats" 
              :key="threat.id" 
              :threat="threat" 
              @view-details="openThreatDetails"
              class="h-full"
            />
          </div>
          
          <!-- Pagination -->
          <div v-if="totalPages > 1" class="mt-6 flex justify-between items-center">
            <div class="text-sm text-muted-foreground">
              Showing page {{ currentPage }} of {{ totalPages }}
            </div>
            <div class="flex gap-2">
              <Button 
                variant="outline" 
                size="sm" 
                :disabled="currentPage <= 1"
                @click="currentPage--"
              >
                Previous
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                :disabled="currentPage >= totalPages"
                @click="currentPage++"
              >
                Next
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Threat Details Modal -->
    <ThreatDetails 
      v-if="selectedThreat" 
      :threat="selectedThreat" 
      @close="selectedThreat = null" 
    />
  </div>
</template>

<script setup>
// Vue and Utilities
import { ref, computed, onMounted, watch } from 'vue'
import { format, subDays } from 'date-fns'
import { toast } from 'vue-sonner'

// UI Components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select'
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription, 
  DialogFooter 
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'

// Custom Components
import DateRangePicker from '@/components/common/DateRangePicker.vue'
import StatCard from '@/components/ui/stat-card/StatCard.vue'
import ThreatCard from '@/components/threats/ThreatCard.vue'
import ThreatDetails from '@/components/threats/ThreatDetails.vue'
import ThreatSeverityDistribution from '@/components/charts/ThreatSeverityDistribution.vue'
import ThreatTrendChart from '@/components/charts/ThreatTrendChart.vue'
import ThreatGeographyMap from '@/components/charts/ThreatGeographyMap.vue'
import ThreatNetworkGraph from '@/components/charts/ThreatNetworkGraph.vue'

// Composable
import { useAnalytics } from '~/composables/useAnalytics'

// Icons
import { Icon } from '@iconify/vue'

const selectedNode = ref(null)
const selectedThreat = ref(null)
const paginatedThreats = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalPages = ref(1)

// Network graph data
const networkData = ref({
  nodes: [],
  links: []
})

// Time range for trend data
const trendTimeRange = ref('7d') // Default to last 7 days

// Initialize analytics composable
const {
  loading,
  error,
  lastUpdated,
  filters,
  stats,
  severityData,
  trendData,
  geoData,
  typeData,
  recentThreats,
  fetchAnalyticsData,
  handleFilterChange
} = useAnalytics()

// Initialize date range in filters if not already set
if (!filters.value.dateRange) {
  filters.value = {
    ...filters.value,
    dateRange: {
      from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
      to: new Date() // Today
    }
  }
}

// Format date range for display
const formattedDateRange = computed(() => {
  if (!filters.value?.dateRange?.from || !filters.value?.dateRange?.to) return ''
  return `${format(new Date(filters.value.dateRange.from), 'MMM d, yyyy')} - ${format(new Date(filters.value.dateRange.to), 'MMM d, yyyy')}`
})

// Filtered threats based on search and filters
const filteredThreats = computed(() => {
  // Return empty array if no threats data is available yet
  if (!recentThreats.value) return []
  
  let result = [...recentThreats.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(threat => 
      threat.title.toLowerCase().includes(query) ||
      (threat.description && threat.description.toLowerCase().includes(query))
    )
  }
  
  // Apply severity filter
  if (filters.value.severity && filters.value.severity !== 'all') {
    result = result.filter(threat => threat.severity === filters.value.severity)
  }
  
  // Apply type filter
  if (filters.value.type && filters.value.type !== 'all') {
    result = result.filter(threat => threat.type === filters.value.type)
  }
  
  // Apply source filter
  if (filters.value.source && filters.value.source !== 'all') {
    result = result.filter(threat => threat.source === filters.value.source)
  }
  
  return result
})

// Group threats by severity for the stats cards
const threatsBySeverity = computed(() => {
  const counts = {
    critical: 0,
    high: 0,
    medium: 0,
    low: 0
  }
  
  if (!filteredThreats.value.length) return counts
  
  filteredThreats.value.forEach(threat => {
    if (threat.severity && counts.hasOwnProperty(threat.severity)) {
      counts[threat.severity]++
    }
  })
  
  return counts
})

// Count active campaigns (threats with status 'active' or 'in_progress')
const activeCampaigns = computed(() => {
  if (!filteredThreats.value.length) return 0
  return filteredThreats.value.filter(threat => 
    threat.status === 'active' || threat.status === 'in_progress'
  ).length
})

// Convert severity data to chart format
const severityChartData = computed(() => {
  return severityData.value.map(item => ({
    name: item.name,
    value: item.value,
    itemStyle: { color: item.color }
  }))
})

// Convert type data to chart format
const typeChartData = computed(() => {
  return typeData.value.map(item => ({
    name: item.name,
    value: item.value,
    itemStyle: { color: item.color }
  }))
})

// Convert trend data to chart format
const formattedTrendData = computed(() => {
  return trendData.value.map(item => ({
    date: item.date,
    [item.severity]: item.value
  }))
})

// Convert geo data to map format
const mapData = computed(() => {
  return geoData.value.map(item => ({
    name: item.name,
    value: item.value[2],
    coords: [item.value[0], item.value[1]]
  }))
})

// Chart options for ECharts components
const typeChartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const { name, value, percent } = params
        return `${name}: ${value} (${percent}%)`
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: isDark ? '#e2e8f0' : '#1e293b',
        fontSize: 12
      },
      formatter: (name) => {
        const item = typeData.value.find(item => item.name === name)
        return item ? `${name}: ${item.value}` : name
      },
      pageTextStyle: {
        color: isDark ? '#e2e8f0' : '#1e293b'
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: isDark ? '#1e293b' : '#ffffff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center',
          color: isDark ? '#e2e8f0' : '#1e293b'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: typeData.value.malware, name: 'Malware' },
          { value: typeData.value.phishing, name: 'Phishing' },
          { value: typeData.value.vulnerability, name: 'Vulnerability' },
          { value: typeData.value.apt, name: 'APT' },
          { value: typeData.value.ransomware, name: 'Ransomware' },
          { value: typeData.value.other, name: 'Other' }
        ]
      }
    ]
  }
})

const hourlyChartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  
  // Generate mock hourly data
  const hours = Array.from({ length: 24 }, (_, i) => i)
  const mockData = hours.map(hour => {
    // Generate a pattern that shows higher activity during business hours
    let value = Math.floor(Math.random() * 10) + 5
    if (hour >= 9 && hour <= 17) {
      value += 15 // Higher during business hours
    }
    if (hour >= 0 && hour <= 5) {
      value = Math.floor(value / 2) // Lower during early morning
    }
    return value
  })
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const hour = params[0].dataIndex
        const value = params[0].value
        return `${hour}:00 - ${hour+1}:00: ${value} threats`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: hours.map(h => `${h}:00`),
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          color: isDark ? '#e2e8f0' : '#1e293b',
          interval: 3 // Show every 3 hours to avoid crowding
        },
        axisLine: {
          lineStyle: {
            color: isDark ? '#475569' : '#cbd5e1'
          }
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          color: isDark ? '#e2e8f0' : '#1e293b'
        },
        axisLine: {
          lineStyle: {
            color: isDark ? '#475569' : '#cbd5e1'
          }
        },
        splitLine: {
          lineStyle: {
            color: isDark ? '#334155' : '#e2e8f0'
          }
        }
      }
    ],
    series: [
      {
        name: 'Threats',
        type: 'bar',
        barWidth: '60%',
        data: mockData,
        itemStyle: {
          color: function(params) {
            // Color gradient based on time of day
            const hour = params.dataIndex
            if (hour >= 9 && hour <= 17) return '#3b82f6' // Business hours - blue
            if (hour >= 18 && hour <= 23) return '#8b5cf6' // Evening - purple
            return '#64748b' // Night/early morning - slate
          }
        }
      }
    ]
  }
})

const flowChartOption = computed(() => {
  // Safe check for SSR - only access document on client side
  const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false
  
  // Generate mock flow data
  const countries = ['United States', 'China', 'Russia', 'Brazil', 'India', 'United Kingdom', 'Germany']
  const mockLinks = []
  
  // Generate some random links between countries
  for (let i = 0; i < countries.length; i++) {
    for (let j = 0; j < countries.length; j++) {
      if (i !== j && Math.random() > 0.7) {
        mockLinks.push({
          source: countries[i],
          target: countries[j],
          value: Math.floor(Math.random() * 50) + 10
        })
      }
    }
  }
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b} -> {c}'
    },
    series: [
      {
        type: 'sankey',
        layout: 'none',
        emphasis: {
          focus: 'adjacency'
        },
        data: countries.map(country => ({ name: country })),
        links: mockLinks,
        lineStyle: {
          color: 'source',
          curveness: 0.5
        },
        itemStyle: {
          color: isDark ? '#475569' : '#cbd5e1',
          borderColor: isDark ? '#1e293b' : '#ffffff'
        },
        label: {
          color: isDark ? '#e2e8f0' : '#1e293b'
        }
      }
    ]
  }
})

// Data fetching with loading states
const fetchData = async () => {
  loading.value = true
  error.value = null
  loading.value = true
  
  try {
    // Simulate API call with timeout
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // Update last updated timestamp
    lastUpdated.value = new Date()
    
    // In a real app, this would be an API call:
    // const response = await api.analytics.getData({
    //   ...filters.value,
    //   startDate: dateRange.value.from.toISOString(),
    //   endDate: dateRange.value.to.toISOString()
    // })
    
    // toast({
    //   title: 'Data refreshed',
    //   description: 'Analytics data has been updated',
    //   variant: 'default'
    // })
  } catch (err) {
    console.error('Error in fetchData:', err)
    error.value = err.message || 'Failed to fetch data'
    // toast({
    //   title: 'Error',
    //   description: error.value,
    //   variant: 'destructive'
    // })
  } finally {
    loading.value = false
  }
}

// Fetch data on component mount
onMounted(() => {
  fetchData()
})

// Handle node click in network graph
function handleNodeClick(node) {
  selectedNode.value = node
  // Show a toast notification
  toast(`Selected: ${node.name}`, {
    description: node.type ? `Type: ${node.type}` : '',
    action: {
      label: 'View Details',
      onClick: () => {
        // Handle view details action
      },
    },
  })
}

// Format date for display
function formatDate(dateString) {
  return format(new Date(dateString), 'MMM d, yyyy')
}

// Open threat details
const openThreatDetails = (threat) => {
  // Implementation for opening threat details
  console.log('Opening threat details:', threat)
}

// Refresh data with error handling
const refreshData = async () => {
  loading.value = true
  try {
    await fetchData()
    toast.success('Data refreshed successfully')
  } catch (error) {
    console.error('Error refreshing data:', error)
    toast.error('Failed to refresh data')
  } finally {
    loading.value = false
  }
}

// Watchers
watch(trendTimeRange, () => {
  // Refetch data when time range changes
  fetchData();
});

watch(
  () => filters.value.dateRange,
  () => {
    // Refetch data when date range changes
    currentPage.value = 1; // Reset to first page
    fetchData();
  },
  { deep: true }
);

// Initialize
onMounted(() => {
  fetchData();
})

// Watch for filter changes
watch(
  () => [filters.value.severity, filters.value.type, filters.value.source, filters.value.status, filters.value.dateRange],
  () => {
    handleFilterChange()
  },
  { deep: true }
)

// Handle errors
watch(error, (newError) => {
  if (newError) {
    // toast({
    //   title: 'Error',
    //   description: newError,
    //   variant: 'destructive'
    // })
  }
})
</script>
