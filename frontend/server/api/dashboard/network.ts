import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock data for network graph
  return {
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
  }
})
