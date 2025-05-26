import { defineEventHandler, getQuery } from 'h3'

export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const timeRange = query.timeRange || '7d'
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Generate calendar data
  return generateCalendarData(timeRange)
})

// Helper function to generate calendar data
function generateCalendarData(timeRange) {
  const data = []
  const end = new Date()
  const start = new Date()
  
  // Determine how far back to go based on time range
  let daysBack = 180 // Default to 6 months
  switch (timeRange) {
    case '24h':
      daysBack = 1
      break
    case '7d':
      daysBack = 7
      break
    case '30d':
      daysBack = 30
      break
    case '90d':
      daysBack = 90
      break
  }
  
  start.setDate(end.getDate() - daysBack)
  
  // Generate data for each day
  for (let time = new Date(start); time <= end; time.setDate(time.getDate() + 1)) {
    // Generate random threat count (higher probability of low numbers)
    let count = Math.floor(Math.random() * 10)
    // Add some spikes for visual interest
    if (Math.random() > 0.9) count += Math.floor(Math.random() * 20)
    
    data.push([
      time.toISOString().split('T')[0],
      count
    ])
  }
  
  return data
}
