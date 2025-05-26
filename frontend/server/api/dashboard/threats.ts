import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  const limit = parseInt(query.limit as string) || 5
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock data for recent threats
  const threats = [
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
    },
    {
      id: '6',
      name: 'Microsoft Exchange Zero-Day',
      severity: 'critical',
      type: 'Vulnerability',
      source: 'CISA',
      detectedAt: '2025-05-19T09:30:00Z'
    }
  ]
  
  // Return limited number of threats
  return threats.slice(0, limit)
})
