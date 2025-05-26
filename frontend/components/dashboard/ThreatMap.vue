<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Icon name="lucide:globe" class="h-5 w-5" />
        Threat Geography
      </CardTitle>
      <CardDescription>Global distribution of active threats</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="h-[300px] w-full">
        <!-- Map visualization would go here -->
        <!-- For now, using a placeholder -->
        <div class="h-full w-full flex items-center justify-center bg-muted/20 rounded-md border border-dashed">
          <div class="text-center">
            <Icon name="lucide:map" class="h-10 w-10 mx-auto text-muted-foreground" />
            <p class="text-sm text-muted-foreground mt-2">Interactive threat map will be displayed here</p>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

// In a real implementation, we would use a mapping library like Leaflet or MapLibre
// and render the threat data on the map
</script>
