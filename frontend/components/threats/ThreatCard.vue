<template>
  <Card class="h-full flex flex-col">
    <CardHeader>
      <div class="flex justify-between items-start">
        <div>
          <CardTitle class="text-lg font-semibold">{{ threat.title }}</CardTitle>
          <div class="flex items-center gap-2 mt-1">
            <Badge :variant="getSeverityVariant(threat.severity)" class="capitalize">
              {{ threat.severity }}
            </Badge>
            <Badge variant="outline" class="capitalize">
              {{ threat.threat_type || 'Unknown' }}
            </Badge>
          </div>
        </div>
        <div class="text-sm text-muted-foreground">
          {{ formatDate(threat.created_at) }}
        </div>
      </div>
    </CardHeader>
    <CardContent class="flex-1">
      <p class="text-sm text-muted-foreground line-clamp-3 mb-4">
        {{ threat.description || 'No description available' }}
      </p>
      
      <div v-if="threat.raw_content" class="space-y-4">
        <div v-if="parsedContent?.threat_assessment">
          <h4 class="text-sm font-medium mb-2">Threat Assessment</h4>
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span class="text-muted-foreground">Status:</span>
              <span class="ml-2 capitalize">{{ parsedContent.threat_assessment.status }}</span>
            </div>
            <div>
              <span class="text-muted-foreground">Confidence:</span>
              <span class="ml-2 capitalize">{{ parsedContent.threat_assessment.confidence }}</span>
            </div>
            <div>
              <span class="text-muted-foreground">First Seen:</span>
              <span class="ml-2">{{ formatDate(parsedContent.threat_assessment.first_seen) }}</span>
            </div>
            <div>
              <span class="text-muted-foreground">Last Updated:</span>
              <span class="ml-2">{{ formatDate(parsedContent.threat_assessment.last_updated) }}</span>
            </div>
          </div>
        </div>

        <div v-if="parsedContent?.impact_assessment" class="mt-4">
          <h4 class="text-sm font-medium mb-2">Impact Assessment</h4>
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span class="text-muted-foreground">Technical Severity:</span>
              <span class="ml-2 capitalize">{{ parsedContent.impact_assessment.technical_severity }}</span>
            </div>
            <div>
              <span class="text-muted-foreground">Business Impact:</span>
              <span class="ml-2 capitalize">{{ parsedContent.impact_assessment.business_impact }}</span>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
    <CardFooter class="flex justify-between items-center pt-0">
      <Button variant="outline" size="sm" @click="$emit('view-details', threat)">
        View Details
      </Button>
      <div v-if="threat.confidence_score" class="text-sm text-muted-foreground">
        Confidence: {{ Math.round(threat.confidence_score * 100) }}%
      </div>
    </CardFooter>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

const props = defineProps({
  threat: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['view-details']);

const parsedContent = computed(() => {
  try {
    if (typeof props.threat.raw_content === 'string') {
      return JSON.parse(props.threat.raw_content);
    }
    return props.threat.raw_content || {};
  } catch (e) {
    console.error('Error parsing threat content:', e);
    return {};
  }
});

const getSeverityVariant = (severity) => {
  const variants = {
    critical: 'destructive',
    high: 'destructive',
    medium: 'warning',
    low: 'default',
    info: 'secondary'
  };
  return variants[severity?.toLowerCase()] || 'default';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return dateString;
  }
};
</script>
