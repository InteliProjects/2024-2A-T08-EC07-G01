<script setup lang="ts">
import { AreaChart } from '@/components/ui/chart-area'
import ChartTooltip from '../ChartTooltip.vue';
import { getAreaChart, type testAreaChart } from './AreaData';

const data = ref<testAreaChart[]>([])

data.value = getAreaChart()
</script>

<template>
  <AreaChart :data="data" index="name" :categories="['total', 'predicted']" :custom-tooltip="ChartTooltip"/>
</template>