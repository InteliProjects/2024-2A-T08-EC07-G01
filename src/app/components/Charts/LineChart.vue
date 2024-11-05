<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { LineChart } from '@/components/ui/chart-line';
import { fetchChartData } from './lineData';
import type { LineChartData } from './lineData';

const selectedClass = ref<number>(1); // Start with class 1
const chartData = ref<LineChartData | null>(null);

const updateData = async (event: Event) => {
  try {
    const target = event.target as HTMLSelectElement;
    selectedClass.value = parseInt(target.value, 10);
    await loadChartData();
  } catch (error) {
    console.error("Error updating data:", error);
  }
};

const loadChartData = async () => {
  chartData.value = await fetchChartData(selectedClass.value);
};

onMounted(async () => {
  await loadChartData();
});
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <!-- Dropdown to select dataset, centered horizontally -->
    <div class="mb-4 w-2/3">
      <label for="dataSelect" class="block mb-1 font-medium text-gray-700 text-center">
        Selecione o Conjunto de Dados
      </label>
      <select
        id="dataSelect"
        @change="updateData"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      >
        <option value="1"> Falhas Classe 1</option>
        <option value="2"> Falhas Classe 2</option>
        <option value="3"> Falhas Classe 3</option>
        <option value="4"> Falhas Classe 4</option>
        <option value="5"> Falhas Classe 5</option>
        <option value="6"> Falhas Classe 6</option>
        <option value="7"> Falhas Classe 7</option>
        <option value="8"> Falhas Classe 8</option>
        <option value="9"> Falhas Classe 9</option>
      </select>
    </div>

    <!-- Line Chart, centered horizontally -->
    <div v-if="chartData" class="w-2/3 mb-5 mt-5">
      <LineChart :data="chartData" index="name" :categories="['Predito', 'Real']" />
    </div>
  </div>
</template>
