import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  const limit = parseInt(query.limit as string) || 5
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock data for recent activities
  const activities = [
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
    },
    {
      type: 'threat',
      title: 'Threat Escalated',
      description: 'Kettering Health Ransomware escalated to high severity',
      timestamp: '2025-05-21T15:50:00Z'
    },
    {
      type: 'ioc',
      title: 'New IOCs Added',
      description: '12 new indicators of compromise added to database',
      timestamp: '2025-05-21T14:20:00Z'
    }
  ]
  
  // Return limited number of activities
  return activities.slice(0, limit)
})
