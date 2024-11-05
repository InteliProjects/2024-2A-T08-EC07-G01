<template>
  <div class="flex flex-col justify-center items-center mt-10">
    <h1 class="text-center mt-10 mb-12 font-semibold text-4xl">Escolha dos Modelos</h1>

    <div class="space-y-4 w-full flex flex-col max-w-4xl">
      <div v-for="(modelClass, index) in modelClasses" :key="index"
        class="flex items-center space-x-2 bg-customBlue rounded-lg px-4 py-3 cursor-pointer transition-colors duration-300 hover:bg-customGreen  hover:text-customGreen"
        @click="openModal(modelClass)">
        <p class="text-white flex-grow">{{ modelClass.name }}</p>
        <p class="flex w-7/12 align-baseline justify-end bg-white text-customBlue rounded-lg p-2">
          {{ selectedModels[modelClass.type]?.model_name || 'Selecione um modelo' }}
          <Icon :name="'mdi:arrow-down-drop-circle-outline'" class="ml-3 pt-6 text-2xl" />
        </p>
      </div>
    </div>

    <choose-model-modal v-if="isModalOpen" :selectedModel="selectedModel" @model-selected="updateSelectedModel"
      @close="closeModal" />
  </div>
</template>

<script>
import axios from 'axios';
import ChooseModelModal from '@/components/Modal/chooseModelModal.vue';

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;

const baseURL = `${apiURL}/api/models/current-models`;

export default {
  components: {
    ChooseModelModal,
  },
  data() {
    return {
      isModalOpen: false,
      selectedModel: null,
      selectedModels: {},
      modelClasses: [
        { name: "Modelo Y/N", apiEndpoint: "models/best-metrics/type0", type: "type0" },
        { name: "Classe 1", apiEndpoint: "models/best-metrics/type1", type: "type1" },
        { name: "Classe 2", apiEndpoint: "models/best-metrics/type2", type: "type2" },
        { name: "Classe 3", apiEndpoint: "models/best-metrics/type4", type: "type4" },
        { name: "Classe 4", apiEndpoint: "models/best-metrics/type5", type: "type5" },
        { name: "Classe 5", apiEndpoint: "models/best-metrics/type133", type: "type133" },
        { name: "Classe 6", apiEndpoint: "models/best-metrics/type137", type: "type137" },
        { name: "Classe 7", apiEndpoint: "models/best-metrics/type140", type: "type140" },
        { name: "Classe 8", apiEndpoint: "models/best-metrics/type9830946", type: "type9830946" },
      ],
    };
  },
  methods: {
    openModal(modelClass) {
      this.selectedModel = { ...modelClass };
      this.isModalOpen = true;
    },
    updateSelectedModel(model) {
      this.$set(this.selectedModels, model.type_model, model);
    },
    closeModal() {
      this.isModalOpen = false;
      this.fetchModels();
    },
    fetchModels() {
      axios.get(`${baseURL}`)
        .then((response) => {
          this.selectedModels = {};
          response.data.forEach((model) => {
            this.selectedModels[model.type_model] = model;
          });
          console.log('Modelos carregados:', this.selectedModels);
        })
        .catch((error) => {
          console.error('Erro ao buscar os modelos:', error);
        });
    }
  },
  mounted() {
    this.fetchModels();
  },
};
</script>

<style scoped></style>
