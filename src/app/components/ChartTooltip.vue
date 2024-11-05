<script setup lang="ts">

// Define the props for the tooltip, similar to how it was done in your example
defineProps<{
  title?: string
  data: {
    name: string
    color: string
    value: any
  }[]
}>()
</script>

<template>
  <Card class="text-sm">
    <!-- Optional title for the tooltip -->
    <CardHeader v-if="title" class="p-3 border-b">
      <CardTitle>
        {{ title }}
      </CardTitle>
    </CardHeader>
    
    <!-- Content of the tooltip -->
    <CardContent class="p-3 min-w-[180px] flex flex-col gap-1">
      <!-- Iterate over the data to display each item -->
      <div v-for="(item, key) in data" :key="key" class="flex justify-between">
        <div class="flex items-center">
          <!-- Circle with the color specified in the data -->
          <span class="w-2.5 h-2.5 mr-2">
            <svg width="100%" height="100%" viewBox="0 0 30 30">
              <path
                d="M 15 15 m -14, 0 a 14,14 0 1,1 28,0 a 14,14 0 1,1 -28,0"
                :stroke="item.color"
                :fill="item.color"
                stroke-width="1"
              />
            </svg>
          </span>
          <!-- Name of the data point -->
          <span>{{ item.name }}</span>
        </div>
        <!-- Value of the data point -->
        <span class="font-semibold ml-4">{{ item.value }}</span>
      </div>
    </CardContent>
  </Card>
</template>
