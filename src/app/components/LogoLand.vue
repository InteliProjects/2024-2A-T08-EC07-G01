<script setup>
import { defineProps } from 'vue';
import defaultLogo from '@/assets/static/whitelogo.png'; // Default logo

const props = defineProps({
  width: {
    type: String,
    default: 'w-10', 
  },

  logo: {
    type: String,
    default: defaultLogo, // Use the default logo as the fallback
  },
});
</script>

<template>
  <div :class="[props.width, 'overflow-hidden', 'rounded-lg']">
    <img :src="props.logo" alt="logo" class="block"/>
  </div>
</template>
