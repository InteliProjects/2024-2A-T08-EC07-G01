<script setup lang="ts">
import { defineProps } from 'vue';

// Define the props for icon name and label text

interface Props {
    iconName: string;
    label: string;
    redirect: string;
}

const props = defineProps<Props>();

function redirect(route: string) {
    navigateTo(route);
};

</script>

<template>
    <Button
        class="relative group bg-transparent transition duration-300 ease-in-out overflow-hidden text-black hover:text-white hover:scale-[107%]" @click="redirect(props.redirect)">
        <span
            class="absolute inset-0 w-full h-full bg-customBlue transform scale-y-0 group-hover:scale-y-100 origin-bottom transition duration-300 ease-in-out"></span>
        <span class="relative z-10 flex items-center">
            <Icon :name="props.iconName"
                class="mr-2 text-xl text-customBlue group-hover:text-white transition duration-300 ease-in-out" />
            {{ props.label }}
        </span>
    </Button>
</template>
