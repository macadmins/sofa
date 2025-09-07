<template>
  <div class="sofa-logo" :class="{ 'sofa-logo-center': center }">
    <div class="inline-flex items-start gap-4">
      <div class="relative">
        <img 
          src="/custom_logo.png" 
          alt="SOFA Logo" 
          :class="logoSize"
          class="drop-shadow-sm"
        />
      </div>
      <div class="flex flex-col">
        <h1 :class="titleSize" class="font-bold text-gray-900 dark:text-white leading-tight">
          SOFA
        </h1>
        <p :class="subtitleSize" class="text-gray-500 dark:text-gray-400 mt-1">
          by Mac Admins Open Source
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: 'large', // large, medium, small
      validator: value => ['large', 'medium', 'small'].includes(value)
    },
    center: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    logoSize() {
      const sizes = {
        large: 'h-16 w-auto',
        medium: 'h-12 w-auto', 
        small: 'h-8 w-auto'
      }
      return sizes[this.size]
    },
    titleSize() {
      const sizes = {
        large: 'text-5xl md:text-6xl',
        medium: 'text-3xl md:text-4xl',
        small: 'text-xl md:text-2xl'
      }
      return sizes[this.size]
    },
    subtitleSize() {
      const sizes = {
        large: 'text-base md:text-lg',
        medium: 'text-sm md:text-base',
        small: 'text-xs md:text-sm'
      }
      return sizes[this.size]
    }
  }
}
</script>

<style scoped>
.sofa-logo-center {
  display: flex;
  justify-content: center;
}

.sofa-logo {
  margin-bottom: 3rem;
}

.sofa-logo.sofa-logo-center {
  margin-bottom: 3rem;
}
</style>