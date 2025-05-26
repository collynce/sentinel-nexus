<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold tracking-tight">Reports</h1>
          <p class="text-muted-foreground">Threat intelligence reports and analysis</p>
        </div>
        <div class="flex items-center gap-2">
          <Button variant="outline">
            <Icon name="lucide:filter" class="mr-2 h-4 w-4" />
            Filter
          </Button>
          <Button>
            <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
            New Report
          </Button>
        </div>
      </div>

      <!-- Search and Filter -->
      <div class="flex items-center space-x-2">
        <div class="relative flex-1">
          <Icon name="lucide:search" class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search reports..."
            class="pl-8"
            v-model="searchQuery"
          />
        </div>
        <Select v-model="typeFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All Types" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="incident">Incident</SelectItem>
            <SelectItem value="threat-actor">Threat Actor</SelectItem>
            <SelectItem value="campaign">Campaign</SelectItem>
            <SelectItem value="vulnerability">Vulnerability</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <!-- Reports Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <ReportCard v-for="report in filteredReports" :key="report.id" :report="report" />
      </div>

      <!-- Empty State -->
      <div v-if="filteredReports.length === 0" class="text-center py-12">
        <Icon name="lucide:file-text" class="h-12 w-12 mx-auto text-muted-foreground" />
        <h3 class="mt-4 text-lg font-medium">No reports found</h3>
        <p class="text-muted-foreground mt-2">Create a new report or adjust your search filters</p>
        <Button class="mt-4">
          <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
          New Report
        </Button>
      </div>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import ReportCard from '@/components/reports/ReportCard.vue'

// Search and filter state
const searchQuery = ref('')
const typeFilter = ref('all')

// Mock reports data
const reports = ref([
  {
    id: '1',
    title: 'DanaBot Malware Campaign Analysis',
    type: 'campaign',
    summary: 'Comprehensive analysis of the recent DanaBot malware campaign targeting financial institutions. Includes IOCs, TTPs, and mitigation recommendations.',
    createdAt: '2025-05-23T10:30:00Z',
    author: {
      name: 'Alex Chen',
      avatar: '/avatars/user.png'
    },
    tags: ['malware', 'banking', 'danabot']
  },
  {
    id: '2',
    title: 'Kettering Health Ransomware Incident',
    type: 'incident',
    summary: 'Detailed breakdown of the Kettering Health ransomware incident. Includes timeline, attack vectors, and lessons learned.',
    createdAt: '2025-05-21T15:45:00Z',
    author: {
      name: 'Sarah Johnson',
      avatar: '/avatars/user.png'
    },
    tags: ['ransomware', 'healthcare', 'incident-response']
  },
  {
    id: '3',
    title: 'APT29 Updated TTPs (2025)',
    type: 'threat-actor',
    summary: 'Updated analysis of APT29 tactics, techniques, and procedures observed in recent campaigns. Includes new tooling and infrastructure details.',
    createdAt: '2025-05-20T09:15:00Z',
    author: {
      name: 'Michael Torres',
      avatar: '/avatars/user.png'
    },
    tags: ['apt29', 'nation-state', 'espionage']
  },
  {
    id: '4',
    title: 'GitLab Duo Authentication Bypass Vulnerability',
    type: 'vulnerability',
    summary: 'Analysis of the recently disclosed authentication bypass vulnerability in GitLab Duo integration (CVE-2025-1234). Includes exploitation details and patching guidance.',
    createdAt: '2025-05-19T14:30:00Z',
    author: {
      name: 'Emma Wilson',
      avatar: '/avatars/user.png'
    },
    tags: ['gitlab', 'authentication', 'cve-2025-1234']
  },
  {
    id: '5',
    title: 'Emerging Ransomware-as-a-Service: BlackCat 2.0',
    type: 'campaign',
    summary: 'Investigation into the new version of BlackCat ransomware being offered as a service on dark web forums. Includes technical details and defensive recommendations.',
    createdAt: '2025-05-18T11:20:00Z',
    author: {
      name: 'David Park',
      avatar: '/avatars/user.png'
    },
    tags: ['ransomware', 'raas', 'blackcat']
  },
  {
    id: '6',
    title: 'Supply Chain Attack: Compromised NPM Packages',
    type: 'incident',
    summary: 'Analysis of recent supply chain attack involving compromised NPM packages. Includes affected packages, IOCs, and remediation steps.',
    createdAt: '2025-05-17T16:45:00Z',
    author: {
      name: 'Olivia Martinez',
      avatar: '/avatars/user.png'
    },
    tags: ['supply-chain', 'npm', 'javascript']
  }
])

// Filter reports based on search and type filter
const filteredReports = computed(() => {
  return reports.value.filter(report => {
    // Search filter
    const matchesSearch = searchQuery.value === '' || 
      report.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      report.summary.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      report.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    // Type filter
    const matchesType = typeFilter.value === 'all' || report.type === typeFilter.value
    
    return matchesSearch && matchesType
  })
})
</script>
