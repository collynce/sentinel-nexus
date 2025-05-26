<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold tracking-tight">Data Sources</h1>
          <p class="text-muted-foreground">Manage and monitor threat intelligence sources</p>
        </div>
        <div class="flex items-center gap-2">
          <Button variant="outline">
            <Icon name="lucide:filter" class="mr-2 h-4 w-4" />
            Filter
          </Button>
          <Button>
            <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
            Add Source
          </Button>
        </div>
      </div>

      <!-- Source Stats -->
      <div class="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader class="pb-2">
            <CardTitle class="text-sm font-medium">Total Sources</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ sources.length }}</div>
            <p class="text-xs text-muted-foreground">Across {{ uniqueSourceTypes.length }} different types</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader class="pb-2">
            <CardTitle class="text-sm font-medium">Active Sources</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ activeSources }}</div>
            <p class="text-xs text-muted-foreground">{{ Math.round((activeSources / sources.length) * 100) }}% of total sources</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader class="pb-2">
            <CardTitle class="text-sm font-medium">Items Collected (24h)</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ totalItemsCollected.toLocaleString() }}</div>
            <p class="text-xs text-muted-foreground">{{ threatsFound.toLocaleString() }} potential threats identified</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader class="pb-2">
            <CardTitle class="text-sm font-medium">Next Scheduled Fetch</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ nextFetchTime }}</div>
            <p class="text-xs text-muted-foreground">{{ nextFetchSource }} source</p>
          </CardContent>
        </Card>
      </div>

      <!-- Source Cards -->
      <div>
        <Tabs defaultValue="all" class="w-full">
          <TabsList>
            <TabsTrigger value="all">All Sources</TabsTrigger>
            <TabsTrigger value="news">News</TabsTrigger>
            <TabsTrigger value="social">Social Media</TabsTrigger>
            <TabsTrigger value="dark_web">Dark Web</TabsTrigger>
            <TabsTrigger value="other">Other</TabsTrigger>
          </TabsList>
          <TabsContent value="all" class="mt-6">
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <SourceCard v-for="source in sources" :key="source.id" :source="source" />
            </div>
          </TabsContent>
          <TabsContent v-for="type in ['news', 'social', 'dark_web', 'other']" :key="type" :value="type" class="mt-6">
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <SourceCard 
                v-for="source in filteredSources(type)" 
                :key="source.id" 
                :source="source" 
              />
            </div>
            <div v-if="filteredSources(type).length === 0" class="text-center py-12">
              <Icon name="lucide:database" class="h-12 w-12 mx-auto text-muted-foreground" />
              <h3 class="mt-4 text-lg font-medium">No sources found</h3>
              <p class="text-muted-foreground mt-2">Add a new source to start collecting threat intelligence</p>
              <Button class="mt-4">
                <Icon name="lucide:plus" class="mr-2 h-4 w-4" />
                Add Source
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
</template>

<script setup>
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import SourceCard from '@/components/sources/SourceCard.vue'

// Mock data for sources
const sources = ref([
  {
    id: '1',
    name: 'The Hacker News',
    type: 'news',
    description: 'Cybersecurity news and analysis',
    status: 'active',
    lastFetch: '2025-05-23T14:30:00Z',
    itemsCollected: 42,
    threatsFound: 3
  },
  {
    id: '2',
    name: 'Krebs on Security',
    type: 'news',
    description: 'In-depth security news and investigation',
    status: 'active',
    lastFetch: '2025-05-23T13:15:00Z',
    itemsCollected: 18,
    threatsFound: 2
  },
  {
    id: '3',
    name: 'Twitter Security Feed',
    type: 'social',
    description: 'Monitoring security researchers and organizations',
    status: 'fetching',
    lastFetch: '2025-05-23T12:45:00Z',
    itemsCollected: 156,
    threatsFound: 5
  },
  {
    id: '4',
    name: 'Dark Web Forum Monitor',
    type: 'dark_web',
    description: 'Monitoring criminal forums and marketplaces',
    status: 'active',
    lastFetch: '2025-05-23T10:00:00Z',
    itemsCollected: 87,
    threatsFound: 12
  },
  {
    id: '5',
    name: 'Pastebin Monitor',
    type: 'paste',
    description: 'Monitoring for leaked credentials and code',
    status: 'error',
    lastFetch: '2025-05-22T22:15:00Z',
    itemsCollected: 203,
    threatsFound: 8
  },
  {
    id: '6',
    name: 'CVE Feed',
    type: 'vulnerability',
    description: 'Common Vulnerabilities and Exposures feed',
    status: 'active',
    lastFetch: '2025-05-23T11:30:00Z',
    itemsCollected: 31,
    threatsFound: 4
  }
])

// Computed properties for stats
const activeSources = computed(() => {
  return sources.value.filter(source => source.status === 'active').length
})

const totalItemsCollected = computed(() => {
  return sources.value.reduce((total, source) => total + source.itemsCollected, 0)
})

const threatsFound = computed(() => {
  return sources.value.reduce((total, source) => total + source.threatsFound, 0)
})

const uniqueSourceTypes = computed(() => {
  return [...new Set(sources.value.map(source => source.type))]
})

// Next fetch time (mock data)
const nextFetchTime = ref('15 minutes')
const nextFetchSource = ref('Twitter Security Feed')

// Filter sources by type
function filteredSources(type) {
  if (type === 'other') {
    return sources.value.filter(source => !['news', 'social', 'dark_web'].includes(source.type))
  }
  return sources.value.filter(source => source.type === type)
}
</script>
