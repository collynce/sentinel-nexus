<template>
  <div class="container py-6 space-y-6">
    <!-- Header with title and filters -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Threat Intelligence Analytics</h1>
        <p class="text-muted-foreground">Analyze and visualize threat data patterns</p>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
        <div class="flex-1">
          <Input 
            v-model="searchQuery" 
            placeholder="Search threats..." 
            class="w-full md:w-[300px]"
          >
            <template #left>
              <Icon name="lucide:search" class="h-4 w-4 text-muted-foreground" />
            </template>
          </Input>
        </div>
        <div class="flex gap-2">
          <DateRangePicker v-model="dateRange" />
          <Button variant="outline" size="icon" @click="refreshData">
            <Icon name="lucide:refresh-cw" class="h-4 w-4" />
          </Button>
        </div>
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
        variant="default"
      />
    </div>

    <!-- Main Content -->
    <div class="grid gap-6">
      <!-- Charts Row 1 -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Severity Distribution -->
        <Card>
          <CardHeader>
            <CardTitle>Threat Distribution by Severity</CardTitle>
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
import { ref, computed, onMounted, watch } from 'vue';
import { format, subDays } from 'date-fns';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import DateRangePicker from '@/components/common/DateRangePicker.vue';
import StatCard from '@/components/ui/StatCard.vue';
import ThreatCard from '@/components/threats/ThreatCard.vue';
import ThreatDetails from '@/components/threats/ThreatDetails.vue';
import ThreatSeverityDistribution from '@/components/charts/ThreatSeverityDistribution.vue';
import ThreatTrendChart from '@/components/charts/ThreatTrendChart.vue';
import ThreatGeographyMap from '@/components/charts/ThreatGeographyMap.vue';

// Sample data - replace with actual API calls
const threats = ref([
  // Your threat data will be loaded here
]);

// UI State
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 6;
const selectedThreat = ref(null);
const trendTimeRange = ref('30d');
const dateRange = ref({
  from: subDays(new Date(), 30),
  to: new Date()
});

// Computed properties
const filteredThreats = computed(() => {
  if (!searchQuery.value) return threats.value;
  const query = searchQuery.value.toLowerCase();
  return threats.value.filter(threat => 
    (threat.title?.toLowerCase().includes(query)) ||
    (threat.description?.toLowerCase().includes(query)) ||
    (threat.threat_type?.toLowerCase().includes(query)) ||
    (threat.raw_content?.toLowerCase().includes(query))
  );
});

const paginatedThreats = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredThreats.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => 
  Math.ceil(filteredThreats.value.length / itemsPerPage)
);

const threatsBySeverity = computed(() => {
  const counts = { critical: 0, high: 0, medium: 0, low: 0 };
  threats.value.forEach(threat => {
    const severity = threat.severity?.toLowerCase();
    if (severity in counts) {
      counts[severity]++;
    }
  });
  return counts;
});

const activeCampaigns = computed(() => {
  // This would come from your actual data
  return threats.value.filter(t => 
    t.raw_content && 
    JSON.parse(t.raw_content).threat_assessment?.status === 'active'
  ).length;
});

// Chart data
const severityData = computed(() => ({
  labels: Object.keys(threatsBySeverity.value).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
  datasets: [{
    data: Object.values(threatsBySeverity.value),
    backgroundColor: [
      'hsl(0, 72%, 51%)', // critical
      'hsl(30, 100%, 50%)', // high
      'hsl(45, 93%, 47%)', // medium
      'hsl(142, 76%, 36%)' // low
    ]
  }]
}));

const trendData = computed(() => {
  // Generate sample trend data - replace with actual data
  const days = trendTimeRange.value === '7d' ? 7 : 
               trendTimeRange.value === '90d' ? 90 : 
               trendTimeRange.value === '1y' ? 365 : 30;
  
  const labels = [];
  const data = [];
  
  for (let i = days - 1; i >= 0; i--) {
    const date = subDays(new Date(), i);
    labels.push(format(date, 'MMM d'));
    // Random data for demo - replace with actual data
    data.push(Math.floor(Math.random() * 20) + 5);
  }
  
  return {
    labels,
    datasets: [
      {
        label: 'Threats',
        data,
        borderColor: 'hsl(199, 89%, 48%)',
        backgroundColor: 'hsla(199, 89%, 48%, 0.1)',
        tension: 0.3,
        fill: true
      }
    ]
  };
});

const geoData = computed(() => {
  // Sample geo data - replace with actual data
  return [
    { name: 'United States', value: [ -95.7129, 37.0902, 120 ] },
    { name: 'China', value: [ 104.1954, 35.8617, 85 ] },
    { name: 'Russia', value: [ 105.3188, 61.5240, 65 ] },
    { name: 'Germany', value: [ 10.4515, 51.1657, 45 ] },
    { name: 'United Kingdom', value: [ -3.4360, 55.3781, 40 ] },
    { name: 'India', value: [ 78.9629, 20.5937, 35 ] },
    { name: 'Brazil', value: [ -51.9253, -14.2350, 30 ] },
    { name: 'Japan', value: [ 138.2529, 36.2048, 25 ] },
    { name: 'Australia', value: [ 133.7751, -25.2744, 20 ] },
    { name: 'South Africa', value: [ 22.9375, -30.5595, 15 ] }
  ];
});

// Methods
const openThreatDetails = (threat) => {
  selectedThreat.value = threat;
};

const refreshData = async () => {
  // Implement data refresh logic here
  console.log('Refreshing data...');
  // await fetchThreats();
};

// Watchers
watch(trendTimeRange, () => {
  // Refetch data when time range changes
  // fetchThreats();
});

watch(dateRange, () => {
  // Refetch data when date range changes
  currentPage.value = 1; // Reset to first page
  // fetchThreats();
}, { deep: true });

// Lifecycle hooks
onMounted(async () => {
  // Initial data fetch
  // await fetchThreats();
});

// Sample data loading - replace with actual API call
// async function fetchThreats() {
//   try {
//     const response = await fetch('/api/threats');
//     threats.value = await response.json();
//   } catch (error) {
//     console.error('Error fetching threats:', error);
//   }
// }
</script>
