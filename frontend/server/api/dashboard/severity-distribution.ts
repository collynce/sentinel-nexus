import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock data for severity distribution
  // In a real implementation, this would be calculated from actual threat data
  return {
    critical: 12,
    high: 25,
    medium: 40,
    low: 15,
    info: 8
  }
})
