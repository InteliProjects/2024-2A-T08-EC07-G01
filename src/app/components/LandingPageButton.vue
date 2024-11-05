<script setup lang="ts">
import { defineProps } from 'vue';

interface Props {
    iconName: string;
    label: string;
    bgColor: string | undefined;
    redirect: string;
}

const props = defineProps<Props>();

function redirect(route: string) {
    console.log(route);
    navigateTo(route);
};

</script>

<template>
    <div class="w-2/6">
        <!-- Componente do botão, é passado na hora de chamá-lo o prop = bgColor como classe -->
        <Button
            :class="['text-base relative group transition duration-300 ease-in-out overflow-hidden text-white hover:text-white hover:scale-[107%] w-full py-[32px]', props.bgColor]"
            @click="redirect(props.redirect)">
            <span
                class="absolute inset-0 w-full h-full bg-transparent transform scale-y-0 group-hover:scale-y-100 origin-bottom transition duration-300 ease-in-out"></span>
            <span class="relative z-10 flex items-center">
                <Icon :name="props.iconName"
                    class="mr-2 text-xl text-white group-hover:text-white transition duration-300 ease-in-out" />
                {{ props.label }}
            </span>
        </Button>
    </div>
</template>
