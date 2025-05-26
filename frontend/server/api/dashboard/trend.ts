import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Generate dates based on time range
  const dates = generateDates(timeRange)
  
  // Mock data for threat trend
  const trendData = dates.map(date => {
    return {
      date,
      critical: Math.floor(Math.random() * 12) + 1,
      high: Math.floor(Math.random() * 20) + 5,
      medium: Math.floor(Math.random() * 30) + 10,
      low: Math.floor(Math.random() * 15) + 5
    }
  })
  
  return trendData
})

// Helper function to generate dates based on time range
function generateDates(timeRange) {
  const dates = []
  const today = new Date()
  let daysToGoBack = 7
  
  switch (timeRange) {
    case '24h':
      daysToGoBack = 1
      break
    case '7d':
      daysToGoBack = 7
      break
    case '30d':
      daysToGoBack = 30
      break
    case '90d':
      daysToGoBack = 90
      break
    default:
      daysToGoBack = 7
  }
  
  // Generate dates
  for (let i = daysToGoBack; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(today.getDate() - i)
    dates.push(date.toISOString().split('T')[0])
  }
  
  return dates
}
