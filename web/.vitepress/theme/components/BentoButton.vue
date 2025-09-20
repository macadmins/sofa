<template>
  <component 
    :is="tag" 
    :href="href" 
    :to="to"
    :target="target"
    :rel="rel"
    :class="[
      'bento-button',
      `bento-button-${variant}`,
      'group/btn'
    ]"
    @click="handleClick"
  >
    <div v-if="$slots.default" class="bento-version-entry">
      <slot />
    </div>
    <div v-if="details" class="bento-version-details">
      {{ details }}
    </div>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'macos' | 'ios' | 'green' | 'orange' | 'emerald'
  href?: string
  to?: string
  target?: string
  rel?: string
  details?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'macos',
  target: '_self'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const tag = computed(() => {
  if (props.href) return 'a'
  if (props.to) return 'router-link'
  return 'button'
})

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>