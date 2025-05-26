<template>
  <Dialog :open="!!threat" @update:open="handleClose">
    <DialogContent class="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle class="text-2xl">{{ threat?.title }}</DialogTitle>
        <DialogDescription>
          <div class="flex items-center gap-4 mt-2">
            <Badge :variant="getSeverityVariant(threat?.severity)" class="text-sm">
              {{ threat?.severity?.toUpperCase() }}
            </Badge>
            <div class="text-sm text-muted-foreground">
              Created: {{ formatDate(threat?.created_at) }}
            </div>
            <div v-if="threat?.updated_at" class="text-sm text-muted-foreground">
              Updated: {{ formatDate(threat.updated_at) }}
            </div>
          </div>
        </DialogDescription>
      </DialogHeader>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Description -->
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-foreground">{{ threat?.description || 'No description available' }}</p>
            </CardContent>
          </Card>

          <!-- Threat Assessment -->
          <Card v-if="parsedContent?.threat_assessment">
            <CardHeader>
              <CardTitle>Threat Assessment</CardTitle>
            </CardHeader>
            <CardContent class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <h4 class="font-medium">Status</h4>
                <p class="text-muted-foreground capitalize">
                  {{ parsedContent.threat_assessment.status || 'N/A' }}
                </p>
              </div>
              <div class="space-y-2">
                <h4 class="font-medium">Confidence</h4>
                <p class="text-muted-foreground capitalize">
                  {{ parsedContent.threat_assessment.confidence || 'N/A' }}
                </p>
              </div>
              <div class="space-y-2">
                <h4 class="font-medium">First Seen</h4>
                <p class="text-muted-foreground">
                  {{ formatDate(parsedContent.threat_assessment.first_seen) }}
                </p>
              </div>
              <div class="space-y-2">
                <h4 class="font-medium">Last Updated</h4>
                <p class="text-muted-foreground">
                  {{ formatDate(parsedContent.threat_assessment.last_updated) }}
                </p>
              </div>
              <div class="space-y-2 md:col-span-2">
                <h4 class="font-medium">Affected Sectors</h4>
                <div class="flex flex-wrap gap-2">
                  <Badge 
                    v-for="(sector, index) in parsedContent.threat_assessment.affected_sectors" 
                    :key="index"
                    variant="secondary"
                    class="capitalize"
                  >
                    {{ sector }}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Evidence -->
          <Card v-if="parsedContent?.evidence?.social_media?.length">
            <CardHeader>
              <CardTitle>Evidence from Social Media</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div 
                v-for="(post, index) in parsedContent.evidence.social_media" 
                :key="index"
                class="border rounded-lg p-4"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <div class="font-medium">{{ post.author }}</div>
                    <div class="text-sm text-muted-foreground">
                      {{ formatDate(post.timestamp) }} · {{ post.platform }}
                    </div>
                  </div>
                  <Badge variant="outline">
                    {{ post.reliability }}
                  </Badge>
                </div>
                <p class="mt-2">{{ post.content_summary }}</p>
                <div v-if="post.threat_keywords_found?.length" class="mt-2">
                  <span class="text-sm text-muted-foreground">Keywords: </span>
                  <span class="text-sm">
                    {{ post.threat_keywords_found.join(', ') }}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Right Column -->
        <div class="space-y-6">
          <!-- Impact Assessment -->
          <Card>
            <CardHeader>
              <CardTitle>Impact Assessment</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div class="space-y-2">
                <h4 class="font-medium">Technical Severity</h4>
                <div class="flex items-center gap-2">
                  <div 
                    class="h-2 rounded-full flex-1 bg-muted overflow-hidden"
                    :title="parsedContent?.impact_assessment?.technical_severity || 'N/A'"
                  >
                    <div 
                      class="h-full bg-primary"
                      :style="{
                        width: getSeverityWidth(parsedContent?.impact_assessment?.technical_severity)
                      }"
                    ></div>
                  </div>
                  <span class="text-sm text-muted-foreground">
                    {{ parsedContent?.impact_assessment?.technical_severity || 'N/A' }}
                  </span>
                </div>
              </div>
              
              <div class="space-y-2">
                <h4 class="font-medium">Business Impact</h4>
                <Badge variant="outline" class="capitalize">
                  {{ parsedContent?.impact_assessment?.business_impact || 'N/A' }}
                </Badge>
              </div>

              <div v-if="parsedContent?.impact_assessment?.affected_systems?.length" class="space-y-2">
                <h4 class="font-medium">Affected Systems</h4>
                <div class="flex flex-wrap gap-1">
                  <Badge 
                    v-for="(system, idx) in parsedContent.impact_assessment.affected_systems" 
                    :key="idx"
                    variant="secondary"
                    class="text-xs"
                  >
                    {{ system }}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Recommendations -->
          <Card v-if="parsedContent?.recommendations?.mitigation_strategies?.length">
            <CardHeader>
              <CardTitle>Recommendations</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div 
                v-for="(strategy, idx) in parsedContent.recommendations.mitigation_strategies" 
                :key="idx"
                class="space-y-1"
              >
                <h4 class="font-medium">{{ strategy.strategy.split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ') }}</h4>
                <p class="text-sm text-muted-foreground">{{ strategy.details }}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <DialogFooter>
        <Button @click="handleClose">Close</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// UI Components
import { 
  Dialog, 
  DialogContent, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription 
} from '@/components/ui/dialog';
import Button from '@/components/ui/button/Button.vue';
import Badge from '@/components/ui/badge/Badge.vue';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import CardTitle from '@/components/ui/card/CardTitle.vue';

const props = defineProps({
  threat: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close']);

const parsedContent = computed(() => {
  if (!props.threat?.raw_content) return {};
  try {
    return typeof props.threat.raw_content === 'string' 
      ? JSON.parse(props.threat.raw_content) 
      : props.threat.raw_content;
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

const getSeverityWidth = (severity) => {
  const widths = {
    critical: '100%',
    high: '75%',
    medium: '50%',
    low: '25%',
    info: '10%'
  };
  return widths[severity?.toLowerCase()] || '0%';
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

const handleClose = () => {
  emit('close');
};
</script>
