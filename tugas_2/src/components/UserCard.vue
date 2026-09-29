<script setup>
import { ref } from 'vue'

defineProps({
  user: { type: Object, required: true }
})

const terbuka = ref(false)
</script>

<template>
  <div class="kartu">
    <h2>{{ user.name }}</h2>
    <p class="username">@{{ user.username }}</p>
    <p class="email">{{ user.email }}</p>

    <button
      :aria-expanded="terbuka"
      :aria-controls="`detail-${user.id}`"
      @click="terbuka = !terbuka"
    >
      {{ terbuka ? 'Sembunyikan' : 'Lihat Detail' }}
    </button>

    <div v-if="terbuka" :id="`detail-${user.id}`" class="detail">
      <p>Telepon: {{ user.phone }}</p>
      <p>Perusahaan: {{ user.company.name }}</p>
      <p>Kota: {{ user.address.city }}</p>
    </div>
  </div>
</template>
