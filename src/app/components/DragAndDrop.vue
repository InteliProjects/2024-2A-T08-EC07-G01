<template>
  <div
    class="relative flex flex-col items-center justify-center border-4 border-dashed border-gray-300 rounded-xl p-8 w-full max-w-lg mx-auto cursor-pointer hover:border-lightGreen transition duration-300 ease-in-out bg-white shadow-lg"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
    :class="{ 'opacity-50 pointer-events-none': isLoading }"
  >
    <div v-if="isLoading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
      <div class="flex flex-col items-center">
        <svg
          class="animate-spin h-10 w-10 text-blue-500 mb-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v8H4z"
          ></path>
        </svg>
        <p class="text-blue-500 text-lg">Processando...</p>
      </div>
    </div>

    <div v-if="isDragging" class="absolute inset-0 bg-green-100 opacity-50 rounded-xl pointer-events-none"></div>

    <div class="text-center z-10" :class="{ 'text-lightGreen': isDragging }" v-if="!file">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v4a1 1 0 001 1h3m10 0h3a1 1 0 001-1V7m-4 10l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      <h2 class="text-2xl font-semibold text-gray-700">Arraste & jogue arquivos aqui</h2>
      <p class="mt-1 text-gray-500">Ou clique para upload</p>
    </div>

    <input ref="fileInput" type="file" class="file-input" @change="handleFileUpload" />

    <div v-if="file" class="w-full mt-4">
      <p class="text-gray-600 font-semibold">{{ file.name }} ({{ formatFileSize(file.size) }})</p>

      <!-- Progress bar removed due to fetch limitations -->
      <!-- <Progress
        class="mt-2"
        :modelValue="uploadProgress"
        aria-label="File Upload Progress"
      /> -->

      <div class="flex justify-center mt-4">
        <Button
          class="w-3/4 relative group bg-black transition duration-300 ease-in-out overflow-hidden text-white hover:scale-[107%]"
          @click="handleContinue"
          :disabled="isLoading"
        >
          <span class="absolute inset-0 w-full h-full bg-customBlue transform scale-y-0 group-hover:scale-y-100 origin-bottom transition duration-300 ease-in-out"></span>
          <span class="relative z-10 flex items-center">
            <Icon :name="'mdi-arrow-down-bold-circle'" class="mr-2 text-xl text-white group-hover:text-white transition duration-300 ease-in-out" />
            {{ "Upload" }}
          </span>
        </Button>
      </div>
    </div>
  </div>

  <TrainingModal
    :show="showModal"
    :previousMetrics="previousMetrics"
    :currentMetrics="currentMetrics"
    @close="closeModal"
    @revert="handleRevert"
    @aproved="handleAproved"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import TrainingModal from '@/components/Modal/TrainingModal.vue';

const file = ref<File | null>(null);
const uploadProgress = ref<number>(0);
const showModal = ref(false);
const isLoading = ref(false); 

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;

const isDragging = ref(false);
const handleDragOver = () => (isDragging.value = true);
const handleDragLeave = () => (isDragging.value = false);

const previousMetrics = ref({
  accuracy: '',
  precision: '',
  recall: '',
  f1_score: '',
});

const currentMetrics = ref({
  accuracy: '',
  precision: '',
  recall: '',
  f1_score: '',
});

const responseData = ref<any>(null);

const handleDrop = (event: DragEvent) => {
  event.preventDefault();
  isDragging.value = false;
  const droppedFiles = Array.from(event.dataTransfer?.files || []);
  if (droppedFiles.length > 0) {
    file.value = droppedFiles[0];
    // Remove uploadFile() call here
  }
};

const triggerFileInput = () => {
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
  if (fileInput) {
    fileInput.click();
  }
};

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  const uploadedFiles = Array.from(input.files || []);
  if (uploadedFiles.length > 0) {
    file.value = uploadedFiles[0];
    // Remove uploadFile() call here
  }
};

const uploadFile = async () => {
  isLoading.value = true; 

  const formData = new FormData();
  formData.append('df_falhas', file.value as Blob);

  try {
    const response = await fetch(`${apiURL}/api/train/retrain`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || response.statusText);
    }

    const data = await response.json();
    responseData.value = data;
    console.log("Retrain Response:", data); 

    currentMetrics.value = {
      accuracy: data.new_model_metrics.accuracy.toFixed(4),
      precision: data.new_model_metrics.precision.toFixed(4),
      recall: data.new_model_metrics.recall.toFixed(4),
      f1_score: data.new_model_metrics.f1_score.toFixed(4),
    };

    previousMetrics.value = data.last_model_metrics
      ? {
          accuracy: data.last_model_metrics.accuracy.toFixed(4),
          precision: data.last_model_metrics.precision.toFixed(4),
          recall: data.last_model_metrics.recall.toFixed(4),
          f1_score: data.last_model_metrics.f1_score.toFixed(4),
        }
      : {
          accuracy: '',
          precision: '',
          recall: '',
          f1_score: '',
        };

    // Show the modal
    showModal.value = true;
  } catch (error: any) {
    console.error('Upload failed:', error);
    alert(`Upload failed: ${error.message}`);
  } finally {
    isLoading.value = false; 
  }
};

const formatFileSize = (size: number) => {
  const kb = size / 1024;
  return kb > 1024 ? `${(kb / 1024).toFixed(2)} MB` : `${kb.toFixed(2)} KB`;
};

const handleContinue = (event: Event) => {
  event.stopPropagation();
  if (file.value) {
    uploadFile();
  }
};

const closeModal = () => {
  showModal.value = false;
  file.value = null;
};

const handleRevert = () => {
  alert('Changes reverted. The previous model remains active.');
  closeModal();
};

const handleAproved = async () => {
  try {
    const modelName = responseData.value?.new_model_metrics?.model_name;
    console.log("Approving model:", modelName); 
    if (!modelName) {
      throw new Error('Model name is undefined.');
    }

    const response = await fetch(`${apiURL}/api/train/select_model`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ model_name: modelName, model_type: 'type0' }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || response.statusText);
    }

    alert('Changes approved. The new model is now in use.');
    closeModal();
  } catch (error: any) {
    console.error('Failed to approve the model:', error);
    alert(`Approval failed: ${error.message}`);
  }
};
</script>

<style scoped>
input[type="file"]::file-selector-button {
  display: none;
}

input[type="file"] {
  display: none;
}
</style>
