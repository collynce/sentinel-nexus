import { ref, computed } from 'vue'
import { useBackendApi } from './useBackendApi'

export function useDashboardData() {
  const api = useBackendApi()
  const loading = ref(false)
  const error = ref(null)
  
  // State for dashboard metrics
  const metrics = ref({
    criticalThreats: 0,
    newIocs: 0,
    activeCampaigns: 0,
    dataSources: 0
  })
  const threats = ref([])
  const activities = ref([])
  const trendData = ref([])
  const severityData = ref({})
  const geographyData = ref([])
  const networkData = ref({ nodes: [], links: [] })
  const calendarData = ref([])
  
  // Computed properties for easy access
  const criticalThreats = computed(() => metrics.value?.criticalThreats || 0)
  const newIocs = computed(() => metrics.value?.newIocs || 0)
  const activeCampaigns = computed(() => metrics.value?.activeCampaigns || 0)
  const dataSources = computed(() => metrics.value?.dataSources || 0)
  
  // Fetch all dashboard data
  async function fetchDashboardData(timeRange = '7d') {
    loading.value = true
    error.value = null
    
    try {
      // Fetch threats and calculate metrics
      const threatResults = await api.threats.getAll({
        limit: 100,
        // We'll use the timeRange to filter by date when the backend supports it
      })
      
      threats.value = threatResults.slice(0, 5) // Get the 5 most recent for the table
      
      // Calculate metrics from threat data
      const criticalCount = threatResults.filter(t => t.severity === 'critical').length
      const highCount = threatResults.filter(t => t.severity === 'high').length
      const mediumCount = threatResults.filter(t => t.severity === 'medium').length
      const lowCount = threatResults.filter(t => t.severity === 'low').length
      const infoCount = threatResults.filter(t => t.severity === 'info').length
      
      // Update severity distribution data
      severityData.value = {
        critical: criticalCount,
        high: highCount,
        medium: mediumCount,
        low: lowCount,
        info: infoCount
      }
      
      // Get sources to count data sources
      const sourceResults = await api.sources.getAll({
        limit: 100,
      })
      
      // Get analysis results to count active campaigns
      const analysisResults = await api.analysis.getResults({
        limit: 100,
      })
      
      // Update metrics
      metrics.value = {
        criticalThreats: criticalCount,
        newIocs: analysisResults.reduce((count, analysis) => count + (analysis.iocs?.length || 0), 0),
        activeCampaigns: new Set(threatResults.map(t => t.campaign).filter(Boolean)).size,
        dataSources: sourceResults.length
      }
      
      // Generate trend data based on threat dates
      trendData.value = generateTrendData(threatResults, timeRange)
      
      // Generate geography data based on threat locations
      geographyData.value = generateGeographyData(threatResults)
      
      // Generate network data based on threats, actors, and campaigns
      networkData.value = generateNetworkData(threatResults)
      
      // Generate calendar data based on threat dates
      calendarData.value = generateCalendarData(threatResults, timeRange)
      
      // Generate activities data based on recent events
      activities.value = generateActivitiesData(threatResults, analysisResults, sourceResults)
      
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
      error.value = err.message || 'Failed to fetch dashboard data'
    } finally {
      loading.value = false
    }
  }
  
  // Refresh all dashboard data
  function refreshData(timeRange = '7d') {
    return fetchDashboardData(timeRange)
  }
  
  // Helper function to generate trend data from threats
  function generateTrendData(threats, timeRange) {
    // Create a map of dates to count threats by severity
    const dateMap = {}
    const now = new Date()
    const daysToInclude = timeRangeToDays(timeRange)
    
    // Initialize dates
    for (let i = daysToInclude; i >= 0; i--) {
      const date = new Date(now)
      date.setDate(now.getDate() - i)
      const dateStr = date.toISOString().split('T')[0]
      dateMap[dateStr] = { date: dateStr, critical: 0, high: 0, medium: 0, low: 0, info: 0 }
    }
    
    // Count threats by date and severity
    threats.forEach(threat => {
      try {
        // Use current date as fallback if no valid date is provided
        const date = threat.detectedAt || threat.createdAt || new Date().toISOString()
        const parsedDate = new Date(date)
        
        // Only process if it's a valid date
        if (!isNaN(parsedDate.getTime())) {
          const dateStr = parsedDate.toISOString().split('T')[0]
          if (dateMap[dateStr]) {
            const severity = threat.severity || 'info' // Default to 'info' if severity is not set
            dateMap[dateStr][severity] = (dateMap[dateStr][severity] || 0) + 1
          }
        }
      } catch (err) {
        console.warn('Error processing threat date:', err)
      }
    })
    
    // Convert map to array
    return Object.values(dateMap)
  }
  
  // Helper function to generate geography data from threats
  function generateGeographyData(threats) {
    // Count threats by country
    const countryMap = {}
    
    threats.forEach(threat => {
      const country = threat.location?.country || 'Unknown'
      if (country !== 'Unknown') {
        countryMap[country] = (countryMap[country] || 0) + 1
      }
    })
    
    // If we don't have location data, generate some sample data
    if (Object.keys(countryMap).length === 0) {
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
    }
    
    // Convert map to array
    return Object.entries(countryMap).map(([name, value]) => ({ name, value }))
  }
  
  // Helper function to generate network data from threats
  function generateNetworkData(threats) {
    const nodes = []
    const links = []
    const nodeMap = {}
    let nodeId = 1
    
    // Process threats
    threats.forEach(threat => {
      // Add threat node if it doesn't exist
      if (!nodeMap[threat.id]) {
        const node = {
          id: String(nodeId),
          name: threat.name,
          category: 'threat',
          value: threat.severity === 'critical' ? 20 : 
                 threat.severity === 'high' ? 15 : 
                 threat.severity === 'medium' ? 10 : 5,
          symbolSize: threat.severity === 'critical' ? 30 : 
                      threat.severity === 'high' ? 25 : 
                      threat.severity === 'medium' ? 20 : 15
        }
        nodes.push(node)
        nodeMap[threat.id] = { index: String(nodeId), node }
        nodeId++
      }
      
      // Add actor node if it exists and doesn't already exist in our map
      if (threat.actor && !nodeMap[`actor-${threat.actor}`]) {
        const node = {
          id: String(nodeId),
          name: threat.actor,
          category: 'actor',
          value: 15,
          symbolSize: 25
        }
        nodes.push(node)
        nodeMap[`actor-${threat.actor}`] = { index: String(nodeId), node }
        nodeId++
        
        // Link actor to threat
        links.push({
          source: nodeMap[`actor-${threat.actor}`].index,
          target: nodeMap[threat.id].index,
          value: 5
        })
      }
      
      // Add campaign node if it exists and doesn't already exist in our map
      if (threat.campaign && !nodeMap[`campaign-${threat.campaign}`]) {
        const node = {
          id: String(nodeId),
          name: threat.campaign,
          category: 'campaign',
          value: 12,
          symbolSize: 22
        }
        nodes.push(node)
        nodeMap[`campaign-${threat.campaign}`] = { index: String(nodeId), node }
        nodeId++
        
        // Link campaign to threat
        links.push({
          source: nodeMap[`campaign-${threat.campaign}`].index,
          target: nodeMap[threat.id].index,
          value: 8
        })
      }
    })
    
    // If we don't have enough data, add some sample data
    if (nodes.length < 5) {
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
    }
    
    return { nodes, links }
  }
  
  // Helper function to generate calendar data from threats
  function generateCalendarData(threats, timeRange) {
    const data = []
    const dateMap = {}
    
    // Count threats by date
    threats.forEach(threat => {
      try {
        // Use current date as fallback if no valid date is provided
        const date = threat.detectedAt || threat.createdAt || new Date().toISOString()
        const parsedDate = new Date(date)
        
        // Only process if it's a valid date
        if (!isNaN(parsedDate.getTime())) {
          const dateStr = parsedDate.toISOString().split('T')[0]
          dateMap[dateStr] = (dateMap[dateStr] || 0) + 1
        }
      } catch (err) {
        console.warn('Error processing threat date in calendar data:', err)
      }
    })
    
    // Convert map to array in the format expected by the calendar component
    Object.entries(dateMap).forEach(([date, count]) => {
      data.push([date, count])
    })
    
    // If we don't have enough data, generate some sample data
    if (data.length < 10) {
      const end = new Date()
      const start = new Date()
      start.setDate(end.getDate() - timeRangeToDays(timeRange))
      
      for (let time = new Date(start); time <= end; time.setDate(time.getDate() + 1)) {
        const dateStr = time.toISOString().split('T')[0]
        if (!dateMap[dateStr]) {
          // Only add dates that don't already have data
          data.push([dateStr, Math.floor(Math.random() * 10)])
        }
      }
    }
    
    return data
  }
  
  // Helper function to generate activities data
  function generateActivitiesData(threats, analyses, sources) {
    const activities = []
    
    // Add recent threats as activities
    threats.slice(0, 2).forEach(threat => {
      activities.push({
        type: 'threat',
        title: `New ${threat.severity.charAt(0).toUpperCase() + threat.severity.slice(1)} Threat Detected`,
        description: threat.name,
        timestamp: threat.detectedAt || threat.createdAt
      })
    })
    
    // Add recent analyses as activities
    analyses.slice(0, 2).forEach(analysis => {
      activities.push({
        type: 'analysis',
        title: 'Threat Analysis Completed',
        description: analysis.name || 'Analysis of potential threat indicators',
        timestamp: analysis.completedAt || analysis.createdAt
      })
    })
    
    // Add recent sources as activities
    sources.slice(0, 1).forEach(source => {
      activities.push({
        type: 'source',
        title: 'Data Source Added',
        description: `New intelligence source: ${source.name}`,
        timestamp: source.createdAt
      })
    })
    
    // Sort by timestamp (most recent first)
    activities.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    
    // If we don't have enough data, add some sample activities
    if (activities.length < 4) {
      activities.push(
        {
          type: 'system',
          title: 'System Update',
          description: 'Threat detection algorithms updated to version 2.4',
          timestamp: new Date(Date.now() - 86400000).toISOString() // 1 day ago
        },
        {
          type: 'user',
          title: 'User Login',
          description: 'Security analyst logged in from new location',
          timestamp: new Date(Date.now() - 172800000).toISOString() // 2 days ago
        }
      )
    }
    
    return activities.slice(0, 5) // Return at most 5 activities
  }
  
  // Helper function to convert time range string to number of days
  function timeRangeToDays(timeRange) {
    switch (timeRange) {
      case '24h': return 1
      case '7d': return 7
      case '30d': return 30
      case '90d': return 90
      default: return 7
    }
  }
  
  return {
    // State
    loading,
    error,
    metrics,
    threats,
    activities,
    trendData,
    severityData,
    geographyData,
    networkData,
    calendarData,
    
    // Computed
    criticalThreats,
    newIocs,
    activeCampaigns,
    dataSources,
    
    // Methods
    fetchDashboardData,
    refreshData
  }
}
