<template>
  <div class="rounded-md border">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead class="w-[80px]">Severity</TableHead>
          <TableHead>Title</TableHead>
          <TableHead>Type</TableHead>
          <TableHead>Source</TableHead>
          <TableHead>Detected</TableHead>
          <TableHead class="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="threat in threats" :key="threat.id">
          <TableCell>
            <Badge :variant="getSeverityVariant(threat.severity || 'medium')">
              {{ threat.severity || 'N/A' }}
            </Badge>
          </TableCell>
          <TableCell class="font-medium">{{ threat.title || 'Untitled' }}</TableCell>
          <TableCell>{{ threat.threat_type || 'other' }}</TableCell>
          <TableCell>{{ getSourceHostname(threat.source_url) }}</TableCell>
          <TableCell>{{ formatDate(threat.created_at) }}</TableCell>
          <TableCell class="text-right">
            <Button variant="ghost" size="icon" @click="viewThreat(threat.id)">
              <Icon name="lucide:eye" class="h-4 w-4" />
            </Button>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<script setup>
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const props = defineProps({
  threats: {
    type: Array,
    required: true,
    default: () => []
  }
})

function getSourceHostname(url) {
  if (!url) return 'Unknown'
  try {
    // Handle both http and https URLs
    const urlObj = new URL(url.startsWith('http') ? url : `https://${url}`)
    return urlObj.hostname.replace('www.', '')
  } catch (e) {
    console.error('Error parsing URL:', e)
    return 'Invalid URL'
  }
}

function getSeverityVariant(severity) {
  const severityValue = (severity || '').toLowerCase()
  const map = {
    'critical': 'destructive',
    'high': 'destructive',
    'medium': 'warning',
    'low': 'outline',
    'info': 'secondary'
  }
  return map[severityValue] || 'outline'
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'Invalid date'
    
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  } catch (e) {
    console.error('Error formatting date:', e)
    return 'Invalid date'
  }
}

function viewThreat(id) {
  navigateTo(`/threats/${id}`)
}
</script>