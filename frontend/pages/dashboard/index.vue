<template>
  <div class="space-y-6">
    <!-- Error Alert -->
    <Alert v-if="error" variant="destructive" class="mb-4">
      <AlertTitle class="flex items-center">
        <Icon name="lucide:alert-circle" class="mr-2 h-4 w-4" />
        Error Loading Dashboard Data
      </AlertTitle>
      <AlertDescription>{{ error }}</AlertDescription>
      <Button variant="outline" size="sm" class="mt-2" @click="handleRefresh">
        Try Again
      </Button>
    </Alert>
    
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p class="text-muted-foreground">Real-time threat intelligence overview</p>
      </div>
      <div class="flex items-center gap-2">
        <Select v-model="timeRange" class="w-[180px]">
          <SelectTrigger>
            <SelectValue placeholder="Time Range" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="24h">Last 24 Hours</SelectItem>
            <SelectItem value="7d">Last 7 Days</SelectItem>
            <SelectItem value="30d">Last 30 Days</SelectItem>
            <SelectItem value="90d">Last 90 Days</SelectItem>
          </SelectContent>
        </Select>
        <Button @click="handleRefresh" :disabled="loading">
          <Icon v-if="loading" name="lucide:loader-2" class="mr-2 h-4 w-4 animate-spin" />
          <Icon v-else name="lucide:refresh-cw" class="mr-2 h-4 w-4" />
          {{ loading ? 'Loading...' : 'Refresh Data' }}
        </Button>
      </div>
    </div>

      <!-- Summary Cards -->
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <ThreatSummaryCard 
          title="Critical Threats" 
          :count="criticalThreats" 
          trend="+12%" 
          color="red"
          icon="lucide:shield-alert"
          description="Active critical severity threats"
        />
        <ThreatSummaryCard 
          title="New IOCs" 
          :count="newIocs" 
          trend="+5%" 
          color="amber"
          icon="lucide:file-search"
          description="Indicators of compromise in last 24h"
        />
        <ThreatSummaryCard 
          title="Active Campaigns" 
          :count="activeCampaigns" 
          trend="-3%" 
          color="blue"
          icon="lucide:target"
          description="Ongoing threat campaigns"
        />
        <ThreatSummaryCard 
          title="Data Sources" 
          :count="dataSources" 
          trend="+1" 
          color="green"
          icon="lucide:database"
          description="Active intelligence sources"
        />
      </div>

      <!-- Chart Section 1: Trend and Distribution -->
      <div class="grid gap-6 md:grid-cols-2">
        <ThreatTrendChart 
          title="Threat Trend" 
          description="Threats detected over time by severity"
          :data="threatTrendData"
          height="300px"
        />
        <ThreatSeverityDistribution
          title="Severity Distribution"
          description="Current threats by severity level"
          :data="severityDistribution"
          height="300px"
        />
      </div>

      <!-- Recent Threats Table -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg flex items-center gap-2">
            <Icon name="lucide:shield-alert" class="h-5 w-5" />
            Recent Threats
          </CardTitle>
          <CardDescription>Latest detected threats and indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <ThreatTable :threats="recentThreats" />
        </CardContent>
      </Card>

      <!-- Chart Section 2: Geography and Activity -->
      <div class="grid gap-6 md:grid-cols-3">
        <div class="md:col-span-2">
          <ThreatGeographyMap
            title="Threat Geography"
            description="Global distribution of active threats"
            :data="geographyData"
            height="400px"
          />
        </div>
        <ThreatHeatmapCalendar
          title="Daily Activity"
          description="Threat detections by day"
          :data="calendarData"
          height="400px"
        />
      </div>

      <!-- Activity and Network Graph -->
      <div class="grid gap-6 md:grid-cols-3">
        <div class="md:col-span-12">
          <ThreatNetworkGraph
            title="Threat Relationship Network"
            description="Connections between threats, actors, and campaigns"
            :data="networkData"
            height="400px"
            @node-click="handleNetworkNodeClick"
          />
        </div>
      </div>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import ThreatSummaryCard from '@/components/dashboard/ThreatSummaryCard.vue'
import ThreatTable from '@/components/threats/ThreatTable.vue'
import RecentActivity from '@/components/dashboard/RecentActivity.vue'

// Import chart components
import ThreatTrendChart from '@/components/charts/ThreatTrendChart.vue'
import ThreatSeverityDistribution from '@/components/charts/ThreatSeverityDistribution.vue'
import ThreatGeographyMap from '@/components/charts/ThreatGeographyMap.vue'
import ThreatNetworkGraph from '@/components/charts/ThreatNetworkGraph.vue'
import ThreatHeatmapCalendar from '@/components/charts/ThreatHeatmapCalendar.vue'

// Dashboard state
const timeRange = ref('7d')

// Use the dashboard data composable
const { 
  loading, 
  error, 
  criticalThreats, 
  newIocs, 
  activeCampaigns, 
  dataSources,
  threats: recentThreats,
  activities: recentActivities,
  trendData: threatTrendData,
  severityData: severityDistribution,
  geographyData,
  networkData,
  calendarData,
  fetchDashboardData,
  refreshData
} = useDashboardData()

// Initial data fetch
onMounted(async () => {
  await fetchDashboardData(timeRange.value)
})

// Watch for time range changes and refresh data
watch(timeRange, async (newRange) => {
  await refreshData(newRange)
})

// Handle refresh button click
async function handleRefresh() {
  await refreshData(timeRange.value)
}

// Handle node click in network graph
function handleNetworkNodeClick(node) {
  // In a real implementation, you might show details or navigate to a related page
  const { $toast } = useNuxtApp()
  $toast.info(`Selected: ${node.name}`, {
    description: `Type: ${node.category}`,
    action: {
      label: 'View Details',
      onClick: () => {}
    }
  })
}

// In a real implementation, we would fetch this data from the API
// onMounted(async () => {
//   const data = await fetchDashboardData(timeRange.value)
//   // Update refs with real data
// })

// Watch for time range changes
watch(timeRange, (newRange) => {
  // In a real implementation, we would fetch new data based on the time range
  console.log(`Time range changed to ${newRange}`)
})
</script>
