<script setup lang="ts">
import { type TableData, type Prediction, convertPredictionToTableData } from '../components/table/testData'
import DataTable from '../components/table/data-table.vue'
import { ref, onMounted } from 'vue'
import { columns } from '../components/table/columns'
import axios from 'axios'

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;
const baseURL = `${apiURL}/api/predictions`;

const data = ref<TableData[]>([]);

onMounted(async () => {
    const response = await axios.get<Prediction[]>(`${baseURL}`)
    data.value = convertPredictionToTableData(response.data);
})
</script>

<template>
    <div class="container py-10 mx-auto">
        <DataTable :columns="columns" :data="data" />
    </div>
</template>
