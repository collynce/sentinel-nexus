<template>
    <div class="space-y-6">
      <!-- Error Alert -->
      <Alert v-if="error" variant="destructive" class="mb-4">
        <div class="flex items-center">
          <Icon name="lucide:alert-circle" class="mr-2 h-4 w-4" />
          <AlertDescription>{{ error }}</AlertDescription>
        </div>
      </Alert>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center p-8">
        <div class="flex flex-col items-center space-y-4">
          <Icon name="lucide:loader-2" class="h-8 w-8 animate-spin" />
          <p class="text-muted-foreground">Loading threats...</p>
        </div>
      </div>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold tracking-tight">Threats</h1>
          <p class="text-muted-foreground">Comprehensive threat intelligence database</p>
        </div>
        <div class="flex items-center gap-2">
          <Button variant="outline">
            <Icon name="lucide:filter" class="mr-2 h-4 w-4" />
            Filter
          </Button>
          <Button @click="fetchThreats" :disabled="loading">
            <Icon name="lucide:refresh-cw" class="mr-2 h-4 w-4" :class="{ 'animate-spin': loading }" />
            {{ loading ? 'Refreshing...' : 'Refresh' }}
          </Button>
        </div>
      </div>

      <!-- Search and Filter -->
      <div class="flex items-center space-x-2">
        <div class="relative flex-1">
          <Icon name="lucide:search" class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search threats..."
            class="pl-8"
            v-model="searchQuery"
          />
        </div>
        <Select v-model="severityFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All Severities" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Severities</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="low">Low</SelectItem>
          </SelectContent>
        </Select>
        <Select v-model="typeFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All Types" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="malware">Malware</SelectItem>
            <SelectItem value="ransomware">Ransomware</SelectItem>
            <SelectItem value="phishing">Phishing</SelectItem>
            <SelectItem value="vulnerability">Vulnerability</SelectItem>
            <SelectItem value="data_breach">Data Breach</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <!-- Threats Table -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg flex items-center gap-2">
            <Icon name="lucide:shield-alert" class="h-5 w-5" />
            Threat Intelligence
          </CardTitle>
          <CardDescription>{{ totalItems }} threats found • Page {{ page }}</CardDescription>
        </CardHeader>
        <CardContent>
          <ThreatTable :threats="mappedThreats" />
        </CardContent>
      </Card>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useBackendApi } from '~/composables/useBackendApi'
import ThreatTable from '@/components/threats/ThreatTable.vue'

const api = useBackendApi()

// State
const searchQuery = ref('')
const severityFilter = ref('all')
const typeFilter = ref('all')
const page = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)
const loading = ref(false)
const error = ref(null)
const threats = ref([])

// Fetch threats from API
const fetchThreats = async () => {
  try {
    loading.value = true
    error.value = null
    
    const params = {
      page: page.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      severity: severityFilter.value !== 'all' ? severityFilter.value : undefined,
      type: typeFilter.value !== 'all' ? typeFilter.value : undefined
    }
    
    const response = await api.threats.getAll(params)
    threats.value = response || []
    totalItems.value = response.total || 0

    console.log({response})
  } catch (err) {
    console.error('Error fetching threats:', err)
    error.value = err.message || 'Failed to load threats. Please try again.'
  } finally {
    loading.value = false
  }
}

// Debounced fetch function
const debouncedFetch = useDebounceFn(() => {
  fetchThreats()
}, 300)

// Watch for filter changes and refetch
watch([searchQuery, severityFilter, typeFilter], () => {
  // Reset to first page when filters change
  if (page.value !== 1) {
    page.value = 1
  } else {
    debouncedFetch()
  }
})

watch(page, () => {
  fetchThreats()
})

onMounted(() => {
  fetchThreats()
})

const mappedThreats = computed(() => {
  return threats.value.map(threat => {
    let parsedContent = {}
    try {
      if (threat.raw_content) {
        parsedContent = JSON.parse(threat.raw_content)
      }
    } catch (e) {
      console.error('Error parsing threat raw_content:', e)
    }
    
    const threatData = parsedContent.threat_assessment || {}
    
    return {
      id: threat.id,
      title: threat.title,
      name: threat.title || threatData.name || 'Unnamed Threat',
      severity: threat.severity || threatData.severity?.toLowerCase() || 'medium',
      type: threat.threat_type || threatData.threat_type || 'other',
      source: threat.source_url 
        ? new URL(threat.source_url).hostname 
        : (threatData.source || 'Unknown'),
      detectedAt: threat.created_at,
      confidence: threat.confidence_score || (threatData.confidence === 'high' ? 0.8 : threatData.confidence === 'medium' ? 0.5 : 0.3),
      status: threatData.status || 'active',
      description: threat.description || threatData.summary || '',
      _raw: threat
    }
  })
})


</script>
