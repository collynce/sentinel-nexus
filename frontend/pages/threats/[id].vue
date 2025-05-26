<template>
    <div class="space-y-6">
      <!-- Error Alert -->
      <Alert v-if="error" variant="destructive" class="mb-4">
        <AlertTitle class="flex items-center">
          <Icon name="lucide:alert-circle" class="mr-2 h-4 w-4" />
          Error Loading Threat Details
        </AlertTitle>
        <AlertDescription>{{ error }}</AlertDescription>
        <Button variant="outline" size="sm" class="mt-2" @click="fetchThreatDetails">
          Try Again
        </Button>
      </Alert>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center p-8">
        <div class="flex flex-col items-center space-y-4">
          <Icon name="lucide:loader-2" class="h-8 w-8 animate-spin" />
          <p class="text-muted-foreground">Loading threat details...</p>
        </div>
      </div>
      
      <!-- Content -->
      <div v-else>
      <!-- Header with back button -->
      <div class="flex items-center gap-4">
        <Button variant="outline" size="icon" @click="navigateTo('/threats')">
          <Icon name="lucide:arrow-left" class="h-4 w-4" />
        </Button>
        <div>
          <h1 class="text-3xl font-bold tracking-tight">{{ threat.name }}</h1>
          <p class="text-muted-foreground">Detailed threat intelligence</p>
        </div>
      </div>

      <!-- Threat Overview -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Left Column: Basic Info -->
        <Card>
          <CardHeader>
            <CardTitle class="text-lg flex items-center gap-2">
              <Icon name="lucide:info" class="h-5 w-5" />
              Threat Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-sm font-medium text-muted-foreground">Severity</p>
                  <Badge :variant="getSeverityVariant(threat.severity)" class="mt-1">
                    {{ threat.severity }}
                  </Badge>
                </div>
                <div>
                  <p class="text-sm font-medium text-muted-foreground">Type</p>
                  <p class="text-sm mt-1">{{ threat.type }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-muted-foreground">First Detected</p>
                  <p class="text-sm mt-1">{{ formatDate(threat.detectedAt) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-muted-foreground">Last Updated</p>
                  <p class="text-sm mt-1">{{ formatDate(threat.updatedAt || threat.detectedAt) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-muted-foreground">Source</p>
                  <p class="text-sm mt-1">{{ threat.source }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-muted-foreground">Status</p>
                  <Badge variant="outline" class="mt-1">
                    {{ threat.status || 'Active' }}
                  </Badge>
                </div>
              </div>

              <div>
                <p class="text-sm font-medium text-muted-foreground">Description</p>
                <p class="text-sm mt-1">{{ threat.description }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Right Column: Technical Details -->
        <Card>
          <CardHeader>
            <CardTitle class="text-lg flex items-center gap-2">
              <Icon name="lucide:code" class="h-5 w-5" />
              Technical Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <!-- Attack Vectors -->
              <div>
                <p class="text-sm font-medium text-muted-foreground">Attack Vectors</p>
                <div class="flex flex-wrap gap-2 mt-1">
                  <Badge v-for="vector in threat.attackVectors" :key="vector" variant="secondary">
                    {{ vector }}
                  </Badge>
                </div>
              </div>

              <!-- IOCs -->
              <div>
                <p class="text-sm font-medium text-muted-foreground">Indicators of Compromise</p>
                <div class="mt-1 space-y-2">
                  <div v-for="(ioc, index) in threat.iocs" :key="index" class="flex items-center gap-2">
                    <Badge variant="outline" class="text-xs">
                      {{ ioc.type }}
                    </Badge>
                    <code class="text-xs bg-muted px-1 py-0.5 rounded">{{ ioc.value }}</code>
                    <Button variant="ghost" size="icon" class="h-5 w-5">
                      <Icon name="lucide:copy" class="h-3 w-3" />
                    </Button>
                  </div>
                  <p v-if="!threat.iocs || threat.iocs.length === 0" class="text-sm text-muted-foreground">
                    No indicators of compromise available
                  </p>
                </div>
              </div>

              <!-- TTPs -->
              <div>
                <p class="text-sm font-medium text-muted-foreground">Tactics, Techniques & Procedures</p>
                <div class="flex flex-wrap gap-2 mt-1">
                  <Badge v-for="ttp in threat.ttps" :key="ttp" variant="outline">
                    {{ ttp }}
                  </Badge>
                  <p v-if="!threat.ttps || threat.ttps.length === 0" class="text-sm text-muted-foreground">
                    No TTPs available
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Evidence & Sources -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg flex items-center gap-2">
            <Icon name="lucide:link" class="h-5 w-5" />
            Evidence & Sources
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-2">
            <div v-for="(source, index) in threat.sources" :key="index" class="flex items-start gap-2 p-2 rounded-md hover:bg-accent">
              <Icon name="lucide:external-link" class="h-4 w-4 mt-0.5" />
              <div>
                <a :href="source.url" target="_blank" rel="noopener noreferrer" class="text-sm font-medium hover:underline">
                  {{ source.title }}
                </a>
                <p class="text-xs text-muted-foreground">{{ source.source }} - {{ formatDate(source.date) }}</p>
              </div>
            </div>
            <p v-if="!threat.sources || threat.sources.length === 0" class="text-sm text-muted-foreground">
              No sources available
            </p>
          </div>
        </CardContent>
      </Card>

      <!-- Recommendations -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg flex items-center gap-2">
            <Icon name="lucide:shield-check" class="h-5 w-5" />
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div v-if="threat.recommendations && threat.recommendations.immediateActions">
              <p class="text-sm font-medium">Immediate Actions</p>
              <ul class="mt-1 space-y-1 list-disc list-inside text-sm">
                <li v-for="action in threat.recommendations.immediateActions" :key="action.action">
                  <span class="font-medium">{{ action.action }}:</span> {{ action.details }}
                </li>
              </ul>
            </div>
            <div v-if="threat.recommendations && threat.recommendations.mitigationStrategies">
              <p class="text-sm font-medium">Mitigation Strategies</p>
              <ul class="mt-1 space-y-1 list-disc list-inside text-sm">
                <li v-for="strategy in threat.recommendations.mitigationStrategies" :key="strategy.strategy">
                  <span class="font-medium">{{ strategy.strategy }}:</span> {{ strategy.details }}
                </li>
              </ul>
            </div>
            <p v-if="!threat.recommendations" class="text-sm text-muted-foreground">
              No recommendations available
            </p>
          </div>
        </CardContent>
      </Card>
      </div>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import { useBackendApi } from '~/composables/useBackendApi'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const api = useBackendApi()
const loading = ref(true)
const error = ref(null)
const threat = ref({
  id: '',
  name: '',
  title: '',
  description: '',
  severity: 'medium',
  type: 'other',
  source: '',
  source_url: '',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  detectedAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  status: 'Active',
  iocs: [],
  ttps: [],
  attackVectors: [],
  sources: [],
  recommendations: {
    immediateActions: [],
    mitigationStrategies: []
  },
  extra_metadata: {}
})

// Fetch threat details from API
const fetchThreatDetails = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await api.threats.getById(id)
    
    // Map API response to component's expected structure
    threat.value = {
      ...threat.value, // Keep existing values
      ...data, // Spread API data
      // Map API fields to component fields
      name: data.title, // Use title as name for the header
      type: data.threat_type || 'other',
      source: data.source_url ? new URL(data.source_url).hostname : 'Unknown',
      detectedAt: data.created_at,
      updatedAt: data.updated_at || data.created_at,
      status: data.extra_metadata?.status || 'Active',
      attackVectors: data.extra_metadata?.attack_vectors || [],
      sources: data.source_url ? [{
        url: data.source_url,
        title: data.title,
        source: data.source_url ? new URL(data.source_url).hostname : 'Unknown',
        date: data.created_at
      }] : [],
      recommendations: data.extra_metadata?.recommendations || {
        immediateActions: [],
        mitigationStrategies: []
      },
      iocs: data.iocs || [],
      ttps: data.ttps || []
    }
  } catch (err) {
    console.error('Error fetching threat details:', err)
    error.value = err.message || 'Failed to fetch threat details'
  } finally {
    loading.value = false
  }
}

// Navigate back to threats list
const navigateTo = (path) => {
  router.push(path)
}

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// Get badge variant based on severity
const getSeverityVariant = (severity) => {
  const map = {
    'critical': 'destructive',
    'high': 'destructive',
    'medium': 'warning',
    'low': 'outline',
    'info': 'secondary'
  }
  return map[severity.toLowerCase()] || 'outline'
}

// Fetch threat details when component mounts
onMounted(() => {
  fetchThreatDetails()
})
</script>