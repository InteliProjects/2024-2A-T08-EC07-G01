<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg shadow-lg max-w-4xl w-full">
      <h3 class="text-customBlue text-2xl font-bold mb-4">Escolha do Modelo {{ selectedModel.name }}</h3>
      <h4 class="text-customBlue text-xl font-semibold mb-4">Escolhas recomendadas</h4>

      <table class="border-collapse border border-gray-300 w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="border border-gray-300 px-4 py-2">Modelos</th>
            <th class="border border-gray-300 px-4 py-2">Acurácia</th>
            <th class="border border-gray-300 px-4 py-2">Recall</th>
            <th class="border border-gray-300 px-4 py-2">F1</th>
            <th class="border border-gray-300 px-4 py-2">Precisão</th>
            <th class="border border-gray-300 px-4 py-2">Escolha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(model, index) in models" :key="index">
            <td class="border border-gray-300 px-4 py-2">{{ model.model_name }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ model.accuracy }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ model.recall }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ model.f1_score }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ model.precision }}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">
              <input type="radio" name="modelSelect" @click="selectModel(model)" :checked="model.using" :value="model"
                v-model="currentModel" />
            </td>
          </tr>
        </tbody>
      </table>
      <div class="flex flex justify-between">
        <button
          class="mt-4 bg-customBlue text-white px-4 py-2 rounded-lg flex items-center space-x-2 cursor-pointer transition-all duration-300 hover:bg-customGreen hover:border-2 hover:border-customGreen"
          @click="updateModel">
          Enviar
        </button>
        <button
          class="mt-4 bg-white border-customBlue border text-customBlue px-4 py-2 rounded-lg flex items-center space-x-2 cursor-pointer transition-all duration-300 hover:bg-customGreen hover:border-2 hover:border-customGreen"
          @click="closeModal">
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;

const baseURL = `${apiURL}/api/`;

import axios from 'axios';

export default {
  props: {
    selectedModel: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      models: [],
      currentModel: null
    };
  },
  methods: {
    updateModel() {
      if (!this.currentModel) {
        console.error("Nenhum modelo foi selecionado.");
        return;
      }
      console.log(this.currentModel)
      const body = {
        model_name: this.currentModel.model_name,
        model_type: this.selectedModel.type,
      };

      console.log(body);
      console.log(`${baseURL}train/select_model`);
      axios.post(`${baseURL}train/select_model`, body)
        .then((response) => {
          alert('Modelo atualizado com sucesso!');
          this.closeModal();
        })
        .catch((error) => {
          console.error('Erro ao atualizar o modelo:', error);
        });
    },

    closeModal() {
      this.$emit('close');
    },
    selectModel(model) {
      this.selectedModel = model; // Atualiza o modelo diretamente
      this.$emit('model-selected', model);
    },
    fetchModels() {
      const endpoint = this.selectedModel.apiEndpoint;
      const body = {
        accuracy: 1,
        precision: 1,
        recall: 1,
        f1_score: 1
      }
      axios.post(`${baseURL}${endpoint}`, body)
        .then((response) => {
          this.models = response.data;
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

<style scoped>
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
