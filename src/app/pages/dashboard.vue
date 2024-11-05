<script setup>
import { ref } from 'vue';  // ref para criar uma variável reativa
import LineChart from '@/components/Charts/LineChart.vue';
import FullLineChart from '~/components/Charts/AreaChart.vue';
import PieChart from '@/components/Charts/PieChart.vue';
import BarChart from '~/components/Charts/BarChart.vue';
import Button from '~/components/ui/button/Button.vue';

// Variável reativa para controlar a visualização (falhas ou modelos)
const currentView = ref('falhas');  // 'falhas' será o valor inicial

// Função para alterar a visualização
const handleViewChange = (view) => {
  currentView.value = view;  // Atualiza a visualização com o novo valor
};
</script>

<template>
  <div class="text-center">
    <h1 class="text-center mt-10 mb-12 font-semibold text-4xl">Dashboard</h1>

    <!-- Botões para alternar entre Falhas e Modelos -->
    <div class="flex justify-center gap-3">
      <Button class="bg-transparent text-customBlue transition-all duration-300" :class="{
        'bg-customGreen border-2 border-customGreen text-white': currentView === 'falhas',
        'hover:bg-transparent hover:border-2 hover:border-customGreen hover:text-customGreen': currentView !== 'falhas'
      }" @click="handleViewChange('falhas')">
        Falhas
      </Button>

      <Button class="bg-transparent text-customBlue transition-all duration-300" :class="{
        'bg-customGreen border-2 border-customGreen text-white': currentView === 'modelos',
        'hover:bg-transparent hover:border-2 hover:border-customGreen hover:text-customGreen': currentView !== 'modelos'
      }" @click="handleViewChange('modelos')">
        Modelos
      </Button>
    </div>

    <!-- Gráficos -->
    <div class="flex mt-12 px-8 flex-col items-center">
      <!-- Exibe os gráficos com base no valor de currentView -->
      <template v-if="currentView === 'falhas'">
        <!-- Container for pie charts side by side -->
        <div class="flex gap-6 w-full justify-center mb-8">
          <div class="flex flex-col gap-3 items-center">
            <h2>Quantidade de Falhas por Carros analisados</h2>
            <PieChart :is-from-fails="true" :show-center="true" class="w-80 h-80" />
          </div>

          <div class="flex flex-col gap-3 items-center">
            <h2>Classes de Falhas por Total de falhas</h2>
            <PieChart :is-from-fails="false" class="w-80 h-80" />
          </div>
        </div>

        <div class="flex flex-col gap-3 items-center w-full mt-12 mb-6">
          <h2 class="text-2xl font-semibold mb-4">Quantidade de Falhas por tempo</h2>
          <LineChart class="w-2/3" />
        </div>
      </template>

      <template v-if="currentView === 'modelos'">
        <div class="flex flex-col items-center w-full gap-8">
          <div class="flex flex-col gap-3 w-full">
            <div>
              <h1 class=" text-2xl font-bold text-customGreen">Metricas do Modelo</h1>
              <h2 class=" text-xl font-bold">Modelo X</h2>
            </div>
            <BarChart class="flex w-full" />
          </div>

          <Button class="bg-customGreen text-white transition-all duration-300 w-full">Trocar Modelos</Button>
        </div>
      </template>
    </div>
  </div>
</template>
