<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { BarChart } from '@/components/ui/chart-bar'

// Define the structure for your response data
interface ModelMetrics {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
}

// State for your chart data and models
const data = ref<any[]>([]);
const filteredData = ref<any[]>([]); // To hold the filtered chart data
const models = ref<string[]>([]);
const selectedSet = ref<string | null>(null); // Store the selected model

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;

// Function to fetch data from API
const fetchData = async () => {
  try {
    const response = await fetch(`${apiURL}/api/models/current-models`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const apiData: ModelMetrics[] = await response.json();
    console.log("apiData", apiData);

    // Transform the API data into a transposed format
    const transformedData: any[] = [
      { metric: 'accuracy', ...apiData.reduce((acc, model) => ({ ...acc, [model.model_name]: model.accuracy }), {}) },
      { metric: 'precision', ...apiData.reduce((acc, model) => ({ ...acc, [model.model_name]: model.precision }), {}) },
      { metric: 'recall', ...apiData.reduce((acc, model) => ({ ...acc, [model.model_name]: model.recall }), {}) },
      { metric: 'f1_score', ...apiData.reduce((acc, model) => ({ ...acc, [model.model_name]: model.f1_score }), {}) }
    ];

    data.value = transformedData;
    models.value = apiData.map((model) => model.model_name);

    // Initially display all data until a model is selected
    filteredData.value = transformedData;
  } catch (error) {
    console.error("Error fetching data", error);
  }
};

// Watch for changes in selectedSet and filter data accordingly
watch(selectedSet, (newModel) => {
  if (newModel) {
    // Filter data to only include the selected model
    filteredData.value = data.value.map(item => ({
      metric: item.metric,
      [newModel]: item[newModel] // Only keep data for the selected model
    }));
  } else {
    // If no model is selected, show all models (default behavior)
    filteredData.value = data.value;
  }
});

// Fetch data when the component is mounted
onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="flex flex-col items-start w-full">
    <!-- Dropdown to select a specific model -->
    <div class="mb-4">
      <label for="modelSelect" class="block mb-1 font-medium text-gray-700">
        Selecione o Modelo
      </label>
      <select id="modelSelect"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        v-model="selectedSet">
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
        <option value="">Mostrar Todos</option> <!-- Option to show all models -->
      </select>
    </div>

    <!-- Bar Chart -->
    <BarChart :data="filteredData" index="metric" :categories="selectedSet ? [selectedSet] : models" :y-formatter="(tick) => {
      return typeof tick === 'number'
        ? tick.toFixed(2)
        : ''
    }" />
  </div>
</template>
