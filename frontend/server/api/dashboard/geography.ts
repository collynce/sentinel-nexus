import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock data for geography distribution
  return [
    { name: 'United States', value: 120 },
    { name: 'China', value: 80 },
    { name: 'Russia', value: 95 },
    { name: 'Germany', value: 42 },
    { name: 'Brazil', value: 35 },
    { name: 'United Kingdom', value: 47 },
    { name: 'India', value: 58 },
    { name: 'Canada', value: 39 },
    { name: 'Australia', value: 28 },
    { name: 'Japan', value: 45 }
  ]
})
