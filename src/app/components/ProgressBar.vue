<script setup lang="ts">
import { Progress } from '@/components/ui/progress'
import { ref } from 'vue'

const progressValue = ref(24)
</script>

<template>
    <div class="relative">
      <!-- Progress Bar with custom green for filled section -->
      <Progress :model-value="progressValue" class="bg-gray-200" filled-class="bg-customGreen" />
  
      <!-- Percentage Text Overlay -->
      <div class="absolute inset-0 flex items-center justify-center text-black font-semibold">
        {{ progressValue }}%
      </div>
    </div>
  </template>