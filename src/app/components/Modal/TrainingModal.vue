<template>
  <transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-4xl shadow-lg">
        <div class="flex justify-end">
          <button class="top-4 hover:scale-[110%]" @click="close">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <h2 class="text-center text-2xl font-semibold mb-10">Arquivo adicionado com sucesso</h2>

        <div class="grid grid-cols-2 gap-6">
          <div>
            <h3 class="text-center font-medium mb-4">Métricas do Modelo Anterior</h3>
            <div class="space-y-2">
              <div class="bg-gray-200 p-4 rounded-md text-center">Acurácia: {{ previousMetrics.accuracy }}</div>
              <div class="bg-gray-200 p-4 rounded-md text-center">Precisão: {{ previousMetrics.precision }}</div>
              <div class="bg-gray-200 p-4 rounded-md text-center">Recall: {{ previousMetrics.recall }}</div>
              <div class="bg-gray-200 p-4 rounded-md text-center">F1-score: {{ previousMetrics.f1_score }}</div>
            </div>
          </div>

          <div>
            <h3 class="text-center font-medium mb-4">Métricas do Modelo Atual</h3>
            <div class="space-y-2">
              <div class="bg-green-200 p-4 rounded-md text-center">Acurácia: {{ currentMetrics.accuracy }}</div>
              <div class="bg-green-200 p-4 rounded-md text-center">Precisão: {{ currentMetrics.precision }}</div>
              <div class="bg-green-200 p-4 rounded-md text-center">Recall: {{ currentMetrics.recall }}</div>
              <div class="bg-green-200 p-4 rounded-md text-center">F1-score: {{ currentMetrics.f1_score }}</div>
            </div>
          </div>
        </div>

        <div class="flex justify-center mt-6">
          <Button
            class="w-1/6 mr-3 relative group bg-red-600 transition duration-300 ease-in-out overflow-hidden text-white hover:scale-[107%]"
            @click="revert"
            :disabled="false"
          >
            <span class="absolute inset-0 w-full h-full bg-red-950 transform scale-y-0 group-hover:scale-y-100 origin-bottom transition duration-300 ease-in-out"></span>
            <span class="relative z-10 flex items-center">
              <Icon :name="'mdi-file-revert'" class="mr-2 text-xl text-white group-hover:text-white transition duration-300 ease-in-out" />
              {{ "Reverter" }}
            </span>
          </Button>
          <Button
            class="w-1/6 ml-3 relative group bg-teal-500 transition duration-300 ease-in-out overflow-hidden text-white hover:scale-[107%]"
            @click="aproved"
            :disabled="false"
          >
            <span class="absolute inset-0 w-full h-full bg-customBlue transform scale-y-0 group-hover:scale-y-100 origin-bottom transition duration-300 ease-in-out"></span>
            <span class="relative z-10 flex items-center">
              <Icon :name="'mdi-approval'" class="mr-2 text-xl text-white group-hover:text-white transition duration-300 ease-in-out" />
              {{ "Aprovar" }}
            </span>
          </Button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: Boolean,
  previousMetrics: {
    type: Object,
    default: () => ({
      accuracy: 0,
      precision: 0,
      recall: 0,
      f1_score: 0,
    }),
  },
  currentMetrics: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['close', 'revert', 'aproved']);

const close = () => emit('close');
const revert = () => emit('revert');
const aproved = () => emit('aproved');
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
