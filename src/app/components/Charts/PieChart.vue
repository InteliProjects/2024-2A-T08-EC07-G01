<script setup lang="ts">
import { DonutChart } from '@/components/ui/chart-donut'
import { ref, onMounted, onUpdated } from 'vue'
import { type TestPieChart, fetchChartData } from './PieData';


// Props
const props = defineProps<{
  isFromFails: boolean
}>()

const data = await fetchChartData(props.isFromFails);

// Definindo as cores manualmente para sincronizar com o gráfico
const chartColors = ['#025159', '#027373', '#38b2ac', '#67d9d5', '#2b2d2f', '#414345', '#6b6d70', '#a0a2a5']

const showCenter = ref(false) // False vai remover o centro


// Call fetchChartData when the component is mounted or props.isFromFails changes

</script>

<template>
  <div class="flex flex-col items-center">
    <!-- Gráfico de Donut com as cores passadas -->
    <DonutChart index="name" :category="'total'" :data="data" :colors="chartColors" :show-center="showCenter" />

    <!-- Legenda dinâmica abaixo do gráfico -->
    <div class="flex flex-wrap justify-center mt-4">
      <div v-for="(item, index) in data" :key="index" class="flex items-center m-2">
        <!-- Círculo colorido representando a cor no gráfico -->
        <div class="w-4 h-4 rounded-full mr-2" :style="{ backgroundColor: chartColors[index] }"></div>
        <span>{{ item.name }}: {{ item.total }}</span>
      </div>
    </div>
  </div>
</template>
