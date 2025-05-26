<template>
  <div class="space-y-6">
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
        <Button>
          <Icon name="lucide:refresh-cw" class="mr-2 h-4 w-4" />
          Refresh Data
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
      <div class="space-y-6 md:col-span-1">
        <RecentActivity :activities="recentActivities" />
      </div>
      <div class="md:col-span-2">
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

// Mock data for initial development
const criticalThreats = ref(12)
const newIocs = ref(78)
const activeCampaigns = ref(5)
const dataSources = ref(16)

// Mock data for charts
const severityDistribution = ref({
critical: 12,
high: 25,
medium: 40,
low: 15,
info: 8
})

const threatTrendData = ref([
{ date: '2025-05-16', critical: 5, high: 10, medium: 15, low: 8 },
{ date: '2025-05-17', critical: 7, high: 12, medium: 14, low: 10 },
{ date: '2025-05-18', critical: 6, high: 15, medium: 18, low: 12 },
{ date: '2025-05-19', critical: 8, high: 13, medium: 20, low: 9 },
{ date: '2025-05-20', critical: 10, high: 18, medium: 22, low: 11 },
{ date: '2025-05-21', critical: 9, high: 20, medium: 25, low: 13 },
{ date: '2025-05-22', critical: 11, high: 22, medium: 28, low: 14 },
{ date: '2025-05-23', critical: 12, high: 25, medium: 30, low: 15 }
])

const geographyData = ref([
{ name: 'United States', value: 120 },
{ name: 'China', value: 80 },
{ name: 'Russia', value: 95 },
{ name: 'Germany', value: 42 },
{ name: 'Brazil', value: 35 },
{ name: 'United Kingdom', value: 47 },
{ name: 'India', value: 58 },
{ name: 'Canada', value: 39 },
{ name: 'Australia', value: 28 },
{ name: 'Japan', value: 45 }
])

const calendarData = ref(generateCalendarData())

const networkData = ref({
nodes: [
  { id: '1', name: 'DanaBot', category: 'malware', value: 20, symbolSize: 30 },
  { id: '2', name: 'APT29', category: 'actor', value: 15, symbolSize: 25 },
  { id: '3', name: 'Kettering Incident', category: 'campaign', value: 12, symbolSize: 22 },
  { id: '4', name: 'CVE-2025-1234', category: 'vulnerability', value: 10, symbolSize: 20 },
  { id: '5', name: 'Healthcare Sector', category: 'target', value: 8, symbolSize: 18 },
  { id: '6', name: 'BlackCat Ransomware', category: 'malware', value: 18, symbolSize: 28 },
  { id: '7', name: 'malicious-domain.example.com', category: 'ioc', value: 5, symbolSize: 15 },
  { id: '8', name: '192.0.2.1', category: 'ioc', value: 5, symbolSize: 15 },
  { id: '9', name: 'APT28', category: 'actor', value: 14, symbolSize: 24 },
  { id: '10', name: 'Financial Sector', category: 'target', value: 9, symbolSize: 19 }
],
links: [
  { source: '1', target: '7', value: 5 },
  { source: '1', target: '8', value: 5 },
  { source: '1', target: '10', value: 8 },
  { source: '2', target: '4', value: 6 },
  { source: '2', target: '9', value: 4 },
  { source: '3', target: '5', value: 7 },
  { source: '3', target: '6', value: 9 },
  { source: '4', target: '5', value: 5 },
  { source: '6', target: '3', value: 8 },
  { source: '9', target: '2', value: 6 },
  { source: '9', target: '4', value: 5 }
]
})

// Recent threats mock data
const recentThreats = ref([
{
  id: '1',
  name: 'DanaBot Malware Campaign',
  severity: 'critical',
  type: 'Malware',
  source: 'News',
  detectedAt: '2025-05-23T10:30:00Z'
},
{
  id: '2',
  name: 'Kettering Health Ransomware',
  severity: 'high',
  type: 'Ransomware',
  source: 'News',
  detectedAt: '2025-05-21T15:45:00Z'
},
{
  id: '3',
  name: 'Coinbase Data Breach',
  severity: 'high',
  type: 'Data Breach',
  source: 'News',
  detectedAt: '2025-05-21T08:15:00Z'
},
{
  id: '4',
  name: 'GitLab Duo Vulnerability',
  severity: 'medium',
  type: 'Vulnerability',
  source: 'News',
  detectedAt: '2025-05-23T11:20:00Z'
},
{
  id: '5',
  name: 'KrebsOnSecurity DDoS Attack',
  severity: 'medium',
  type: 'DDoS',
  source: 'News',
  detectedAt: '2025-05-20T14:10:00Z'
}
])

// Recent activities mock data
const recentActivities = ref([
{
  type: 'threat',
  title: 'New Critical Threat Detected',
  description: 'DanaBot Malware Campaign identified from multiple sources',
  timestamp: '2025-05-23T10:30:00Z'
},
{
  type: 'source',
  title: 'Data Source Added',
  description: 'New dark web monitoring source activated',
  timestamp: '2025-05-23T09:15:00Z'
},
{
  type: 'system',
  title: 'System Update',
  description: 'Threat detection algorithms updated to version 2.4',
  timestamp: '2025-05-22T16:40:00Z'
},
{
  type: 'user',
  title: 'User Login',
  description: 'Security analyst logged in from new location',
  timestamp: '2025-05-22T08:05:00Z'
}
])

// Helper function to generate calendar data
function generateCalendarData() {
const data = []
const end = new Date()
const start = new Date()
start.setDate(end.getDate() - 180) // Last 6 months

for (let time = start; time <= end; time.setDate(time.getDate() + 1)) {
  // Generate random threat count (higher probability of low numbers)
  let count = Math.floor(Math.random() * 10)
  // Add some spikes for visual interest
  if (Math.random() > 0.9) count += Math.floor(Math.random() * 20)
  
  data.push([
    time.toISOString().split('T')[0],
    count
  ])
}

return data
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
