<template>
    <div class="flex items-center justify-center mt-10">
        <div class="w-full max-w-md p-8 space-y-4">
            <p class="bold text-3xl text-center mx-5 mt-10">Digite o KNR</p>

            <input v-model="knr" type="text"
                class="w-full h-16 px-3 py-2 text-3xl text-center border-2 border-gray-300 rounded-lg focus:outline-none focus:border-customBlue"
                @keydown.enter="goToPrediction" />

            <Button class="w-full" @click="goToPrediction">
                Ver previsão
            </Button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const knr = ref('');

const goToPrediction = () => {
    if (knr.value.trim()) {
        navigateTo(`/prediction/${knr.value}`);
    }
};
</script>