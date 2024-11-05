<script setup lang="ts">
import { type HTMLAttributes, computed } from 'vue'
import {
  ProgressIndicator,
  ProgressRoot,
  type ProgressRootProps,
} from 'radix-vue'
import { ref, watch } from 'vue'
import { useMotion } from '@vueuse/motion'
import { cn } from '@/lib/utils'

const props = withDefaults(
  defineProps<ProgressRootProps & { class?: HTMLAttributes['class'] }>(),
  {
    modelValue: 0,
  },
)

// Compute delegated props
const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props
  return delegated
})

const motionProps = ref({
  initial: { x: '-100%' },
  enter: { x: `-${100 - (props.modelValue ?? 0)}%` },
})

watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue != null) { // Check if newValue is not null or undefined
      motionProps.value.enter = {
        x: `-${100 - newValue}%`,
        transition: { duration: 2, ease: 'easeInOut' },
      }
    }
  },
)

</script>

<template>
  <ProgressRoot
    v-bind="delegatedProps"
    :class="
      cn(
        'relative h-4 w-full overflow-hidden rounded-full bg-secondary',
        props.class,
      )
    "
  >
    <div
      v-motion="motionProps"
      class="h-full bg-customGreen"
      style="transform-origin: left;"
    >
      <ProgressIndicator class="h-full flex-1" />
    </div>
  </ProgressRoot>
</template>
