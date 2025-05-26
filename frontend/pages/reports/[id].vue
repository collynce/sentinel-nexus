<template>
    <div class="space-y-6">
      <!-- Header with back button -->
      <div class="flex items-center gap-4">
        <Button variant="outline" size="icon" @click="navigateTo('/reports')">
          <Icon name="lucide:arrow-left" class="h-4 w-4" />
        </Button>
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <h1 class="text-3xl font-bold tracking-tight">{{ report.title }}</h1>
            <div class="flex items-center gap-2">
              <Button variant="outline">
                <Icon name="lucide:download" class="mr-2 h-4 w-4" />
                Export
              </Button>
              <Button variant="outline">
                <Icon name="lucide:edit" class="mr-2 h-4 w-4" />
                Edit
              </Button>
            </div>
          </div>
          <div class="flex items-center gap-4 mt-2">
            <Badge>{{ report.type }}</Badge>
            <p class="text-sm text-muted-foreground">Created {{ formatDate(report.createdAt) }}</p>
            <div class="flex items-center gap-2">
              <Avatar class="h-6 w-6">
                <AvatarImage :src="report.author.avatar" />
                <AvatarFallback>{{ getInitials(report.author.name) }}</AvatarFallback>
              </Avatar>
              <span class="text-sm">{{ report.author.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Report Content -->
      <div class="grid gap-6 md:grid-cols-3">
        <!-- Main Content -->
        <div class="md:col-span-2 space-y-6">
          <!-- Executive Summary -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Executive Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-sm">{{ report.summary }}</p>
            </CardContent>
          </Card>

          <!-- Key Findings -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Key Findings</CardTitle>
            </CardHeader>
            <CardContent>
              <ul class="space-y-2">
                <li v-for="(finding, index) in report.keyFindings" :key="index" class="flex items-start gap-2">
                  <Icon name="lucide:check-circle" class="h-5 w-5 text-primary mt-0.5" />
                  <p class="text-sm">{{ finding }}</p>
                </li>
              </ul>
            </CardContent>
          </Card>

          <!-- Technical Details -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Technical Details</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <div v-if="report.technicalDetails.attackVectors">
                  <h3 class="text-sm font-medium mb-2">Attack Vectors</h3>
                  <div class="flex flex-wrap gap-2">
                    <Badge v-for="vector in report.technicalDetails.attackVectors" :key="vector" variant="outline">
                      {{ vector }}
                    </Badge>
                  </div>
                </div>

                <div v-if="report.technicalDetails.iocs">
                  <h3 class="text-sm font-medium mb-2">Indicators of Compromise</h3>
                  <div class="space-y-2">
                    <div v-for="(iocGroup, type) in groupedIocs" :key="type">
                      <h4 class="text-xs font-medium text-muted-foreground mb-1">{{ type }}</h4>
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                        <div v-for="(ioc, index) in iocGroup" :key="index" class="flex items-center gap-2 bg-muted/50 rounded p-2">
                          <code class="text-xs">{{ ioc.value }}</code>
                          <Button variant="ghost" size="icon" class="h-6 w-6 ml-auto">
                            <Icon name="lucide:copy" class="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="report.technicalDetails.ttps">
                  <h3 class="text-sm font-medium mb-2">Tactics, Techniques & Procedures</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                    <div v-for="ttp in report.technicalDetails.ttps" :key="ttp.id" class="flex items-center gap-2 bg-muted/50 rounded p-2">
                      <Badge variant="outline">{{ ttp.id }}</Badge>
                      <span class="text-xs">{{ ttp.name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Timeline -->
          <Card v-if="report.timeline && report.timeline.length > 0">
            <CardHeader>
              <CardTitle class="text-lg">Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="relative border-l pl-6 space-y-6">
                <div v-for="(event, index) in report.timeline" :key="index" class="relative">
                  <div class="absolute -left-[25px] mt-1.5 h-3 w-3 rounded-full border border-primary bg-background"></div>
                  <div class="text-sm font-medium">{{ formatTimelineDate(event.date) }}</div>
                  <div class="text-sm mt-1">{{ event.description }}</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Recommendations -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <div>
                  <h3 class="text-sm font-medium mb-2">Immediate Actions</h3>
                  <ul class="space-y-2">
                    <li v-for="(action, index) in report.recommendations.immediateActions" :key="index" class="flex items-start gap-2">
                      <Badge :variant="getPriorityVariant(action.priority)" class="mt-0.5">{{ action.priority }}</Badge>
                      <div>
                        <p class="text-sm font-medium">{{ action.action }}</p>
                        <p class="text-sm text-muted-foreground">{{ action.details }}</p>
                      </div>
                    </li>
                  </ul>
                </div>

                <div>
                  <h3 class="text-sm font-medium mb-2">Mitigation Strategies</h3>
                  <ul class="space-y-2">
                    <li v-for="(strategy, index) in report.recommendations.mitigationStrategies" :key="index" class="flex items-start gap-2">
                      <Badge :variant="getPriorityVariant(strategy.priority)" class="mt-0.5">{{ strategy.priority }}</Badge>
                      <div>
                        <p class="text-sm font-medium">{{ strategy.strategy }}</p>
                        <p class="text-sm text-muted-foreground">{{ strategy.details }}</p>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Related Threats -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Related Threats</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-2">
                <div v-for="threat in report.relatedThreats" :key="threat.id" class="flex items-start gap-2 p-2 rounded-md hover:bg-accent">
                  <Badge :variant="getSeverityVariant(threat.severity)" class="mt-0.5">{{ threat.severity }}</Badge>
                  <div>
                    <NuxtLink :to="`/threats/${threat.id}`" class="text-sm font-medium hover:underline">
                      {{ threat.name }}
                    </NuxtLink>
                    <p class="text-xs text-muted-foreground">{{ formatDate(threat.detectedAt) }}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Tags -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">Tags</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="flex flex-wrap gap-2">
                <Badge v-for="tag in report.tags" :key="tag" variant="secondary">
                  {{ tag }}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <!-- References -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">References</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-2">
                <div v-for="(reference, index) in report.references" :key="index" class="flex items-start gap-2">
                  <Icon name="lucide:external-link" class="h-4 w-4 mt-0.5" />
                  <a :href="reference.url" target="_blank" rel="noopener noreferrer" class="text-sm hover:underline">
                    {{ reference.title }}
                  </a>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

// Get the report ID from the route
const route = useRoute()
const id = route.params.id

// Mock report data (would be fetched from API)
const report = ref({
  id: '1',
  title: 'DanaBot Malware Campaign Analysis',
  type: 'campaign',
  summary: 'The U.S. Department of Justice (DoJ) disrupted the online infrastructure associated with DanaBot malware and unsealed charges against 16 individuals. The malware infected more than 300,000 computers worldwide, facilitated fraud and ransomware, and caused at least $50 million in damages. This report provides a comprehensive analysis of the campaign, including technical details, IOCs, and mitigation recommendations.',
  createdAt: '2025-05-23T10:30:00Z',
  author: {
    name: 'Alex Chen',
    avatar: '/avatars/user.png'
  },
  keyFindings: [
    'DanaBot malware infected over 300,000 computers worldwide, causing at least $50 million in damages.',
    'The campaign primarily targeted financial institutions and their customers through phishing emails with malicious attachments.',
    'The malware uses a modular architecture allowing for flexible functionality, including credential theft, keylogging, and form grabbing.',
    'The DoJ has disrupted the infrastructure and charged 16 individuals associated with the operation.',
    'Organizations should implement the recommended mitigations to protect against similar attacks.'
  ],
  technicalDetails: {
    attackVectors: ['Phishing', 'Malicious Documents', 'Drive-by Download'],
    iocs: [
      { type: 'domain', value: 'malicious-domain.example.com' },
      { type: 'domain', value: 'danabot-c2.example.net' },
      { type: 'domain', value: 'update-server.example.org' },
      { type: 'hash', value: '5f4dcc3b5aa765d61d8327deb882cf99' },
      { type: 'hash', value: 'e10adc3949ba59abbe56e057f20f883e' },
      { type: 'hash', value: '25d55ad283aa400af464c76d713c07ad' },
      { type: 'ip', value: '192.0.2.1' },
      { type: 'ip', value: '198.51.100.1' },
      { type: 'file', value: 'invoice_may2025.docx' },
      { type: 'file', value: 'payment_details.xlsx' }
    ],
    ttps: [
      { id: 'T1566.001', name: 'Phishing: Spearphishing Attachment' },
      { id: 'T1204.002', name: 'User Execution: Malicious File' },
      { id: 'T1027', name: 'Obfuscated Files or Information' },
      { id: 'T1055', name: 'Process Injection' },
      { id: 'T1056.001', name: 'Input Capture: Keylogging' },
      { id: 'T1083', name: 'File and Directory Discovery' },
      { id: 'T1573.001', name: 'Encrypted Channel: Symmetric Cryptography' }
    ]
  },
  timeline: [
    {
      date: '2025-01-15T00:00:00Z',
      description: 'First observations of the new DanaBot campaign targeting financial institutions.'
    },
    {
      date: '2025-02-10T00:00:00Z',
      description: 'Campaign expands to target healthcare and government sectors.'
    },
    {
      date: '2025-03-22T00:00:00Z',
      description: 'Security researchers publish initial analysis of the campaign.'
    },
    {
      date: '2025-04-18T00:00:00Z',
      description: 'Law enforcement begins investigation into the DanaBot operation.'
    },
    {
      date: '2025-05-22T00:00:00Z',
      description: 'DoJ announces takedown of DanaBot infrastructure and charges against 16 individuals.'
    }
  ],
  recommendations: {
    immediateActions: [
      {
        action: 'Update Antivirus',
        details: 'Ensure all systems have updated antivirus definitions that can detect DanaBot variants.',
        priority: 'critical'
      },
      {
        action: 'Network Monitoring',
        details: 'Monitor for communication with known DanaBot C2 servers.',
        priority: 'high'
      },
      {
        action: 'Block IOCs',
        details: 'Block all identified IOCs at network and endpoint levels.',
        priority: 'high'
      }
    ],
    mitigationStrategies: [
      {
        strategy: 'Email Filtering',
        details: 'Implement strict email filtering to block malicious attachments.',
        priority: 'high'
      },
      {
        strategy: 'User Training',
        details: 'Conduct phishing awareness training for all employees.',
        priority: 'medium'
      },
      {
        strategy: 'Application Control',
        details: 'Implement application whitelisting to prevent execution of unauthorized code.',
        priority: 'medium'
      },
      {
        strategy: 'Network Segmentation',
        details: 'Segment networks to limit lateral movement in case of compromise.',
        priority: 'medium'
      }
    ]
  },
  relatedThreats: [
    {
      id: '1',
      name: 'DanaBot Malware Campaign',
      severity: 'critical',
      detectedAt: '2025-05-23T10:30:00Z'
    },
    {
      id: '7',
      name: 'Banking Trojan Surge',
      severity: 'high',
      detectedAt: '2025-05-20T08:45:00Z'
    }
  ],
  tags: ['malware', 'banking', 'danabot', 'trojan', 'financial'],
  references: [
    {
      title: 'U.S. DoJ Press Release: DanaBot Takedown',
      url: 'https://www.justice.gov/example/danabot-takedown'
    },
    {
      title: 'Technical Analysis of DanaBot Malware',
      url: 'https://example-security-blog.com/danabot-analysis'
    },
    {
      title: 'MITRE ATT&CK: Banking Trojans',
      url: 'https://attack.mitre.org/example/banking-trojans'
    }
  ]
})

// Group IOCs by type for better display
const groupedIocs = computed(() => {
  const grouped = {}
  report.value.technicalDetails.iocs.forEach(ioc => {
    if (!grouped[ioc.type]) {
      grouped[ioc.type] = []
    }
    grouped[ioc.type].push(ioc)
  })
  return grouped
})

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

function formatTimelineDate(dateString) {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

function getInitials(name) {
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
}

function getSeverityVariant(severity) {
  const map = {
    'critical': 'destructive',
    'high': 'destructive',
    'medium': 'warning',
    'low': 'outline',
    'info': 'secondary'
  }
  return map[severity.toLowerCase()] || 'outline'
}

function getPriorityVariant(priority) {
  const map = {
    'critical': 'destructive',
    'high': 'destructive',
    'medium': 'warning',
    'low': 'outline'
  }
  return map[priority.toLowerCase()] || 'outline'
}
</script>
