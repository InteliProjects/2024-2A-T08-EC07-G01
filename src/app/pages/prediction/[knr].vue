<!--TODO: Type component-->

<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <!-- Tela de resultado com falha -->
        <div class="w-full max-w-7xl p-8 bg-white border-2 rounded-lg shadow-lg" :class="resultStyle.border">
            <div class="flex items-center gap-4 mb-6">
                <span class="text-2xl font-bold text-center " :class="resultStyle.title">Carro {{ styles.text }} </span>
            </div>
            <p class="text-center text-gray-700 text-xl font-medium mb-6">KNR: {{ knr }}</p>
            <div class="grid grid-cols-5 grid-flow-row gap-4 mt-2">
                <template v-for="(failType, index) in failTypes" :key="index">
                    <div :class="[
                        'border w-40 h-24 text-center flex flex-col justify-center items-center',
                        styles[failType.status].bg,
                        styles[failType.status].border,
                        styles[failType.status].text,
                    ]">
                        <p :class="['font-bold', styles[failType.status].text]">{{ failType.title }}</p>
                        <p :class="['font-normal break-normal', styles[failType.status].text]">{{ failType.description
                            }}</p>
                    </div>
                </template>
            </div>
            <!-- Botão de Voltar -->
            <div class="flex float-end">
                <button @click="voltar" class="mt-4 px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600">
                    Voltar
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { failTypes } from './knrsData.ts';

import Axios from 'axios';

const config = useRuntimeConfig();
const apiURL = config.public.backendUrl;

const knr = useRoute().params.knr;

const styles = {
    text: 'sem falha prevista',
    default: {
        border: 'border-gray-300',
        bg: '',
        title: 'text-gray-800',
        text: 'text-gray-800'
    },
    success: {
        border: 'border-green-400',
        bg: 'bg-green-500',
        title: 'text-green-600',
        text: 'text-white'
    },
    fail: {
        border: 'border-red-400',
        bg: 'bg-rose-500',
        title: 'text-red-600',
        text: 'text-white'
    }
};

const res = await Axios.get(`${apiURL}/api/predictions/details/${knr}`);

const failType = res.data.predicted_fail_codes;


onMounted(() => {
    failTypes.value.forEach((fail) => {
        failType.forEach((type) => {
            if (fail.failType === type) {
                fail.status = 'fail';
                styles.text = "com falha prevista";
            }
        });
    });
});


const result = computed(() => (failType[0] !== -1 && failType.length != 0 ? 'fail' : 'success'));
const resultStyle = computed(() => styles[result.value]);
const resultText = computed(() => (result.value === 'fail' ? 'Falha prevista' : 'Sem falha prevista'));



const voltar = () => {
    // Reset the variables
    failTypes.value.forEach((fail) => {
        fail.status = 'default';
    });
    styles.text = 'sem falha prevista';
    result.value = 'default';
    navigateTo(`/prediction`);
};

</script>