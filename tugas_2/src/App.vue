<script setup>
import { ref, computed, watch } from 'vue'
import UserCard from './components/UserCard.vue'

const users = ref([])
const keadaan = ref('idle')
const queryPencarian = ref('')
const riwayatPencarian = ref([])
const arahUrutan = ref('asc')

const namaIndonesia = [
  'Agus Setiawan', 'Rina Wulandari', 'Dedi Kurniawan', 'Sari Puspita',
  'Fajar Hidayat', 'Nita Rahmawati', 'Rizky Maulana', 'Wulan Sari',
  'Bayu Prasetyo', 'Tika Lestari'
]

async function muatPengguna() {
  keadaan.value = 'loading'
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users')
    if (!response.ok) throw new Error('Gagal memuat data')
    const data = await response.json()
    users.value = data.map((u, i) => {
      const nama = namaIndonesia[i] || `Pengguna ${i + 1}`
      return {
        ...u,
        name: nama,
        username: nama.toLowerCase().replace(/\s+/g, ''),
        email: 'dharma@jiep.co.id'
      }
    })
    keadaan.value = users.value.length === 0 ? 'empty' : 'success'
  } catch {
    keadaan.value = 'error'
  }
}

const penggunaTersaring = computed(() => {
  const q = queryPencarian.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(u => u.username.toLowerCase().includes(q))
})

const penggunaTerurut = computed(() => {
  const salinan = [...penggunaTersaring.value]
  salinan.sort((a, b) => {
    const hasil = a.name.localeCompare(b.name)
    return arahUrutan.value === 'asc' ? hasil : -hasil
  })
  return salinan
})

const jumlahHasil = computed(() => penggunaTersaring.value.length)

watch(queryPencarian, (nilai) => {
  const q = nilai.trim()
  if (q) {
    riwayatPencarian.value.push(q)
  }
})
</script>

<template>
  <div class="app">
    <header>
      <h1>Dashboard Pengguna</h1>
      <p>Dharma Satriadi | 25120300030</p>
    </header>

    <main>
      <section class="controls">
        <button @click="muatPengguna" :disabled="keadaan === 'loading'">
          Muat Pengguna
        </button>
        <div class="cari">
          <label for="pencarian">Cari username</label>
          <input id="pencarian" v-model="queryPencarian" type="text" placeholder="contoh: agus" />
        </div>
      </section>

      <p v-if="keadaan === 'idle'" role="status">Klik Muat Pengguna untuk menampilkan daftar.</p>
      <p v-else-if="keadaan === 'loading'" role="status">Sedang memuat data...</p>
      <p v-else-if="keadaan === 'error'" role="alert">Terjadi kesalahan saat memuat data. Coba lagi.</p>
      <p v-else-if="keadaan === 'empty'" role="status">Data pengguna kosong.</p>

      <section v-else-if="keadaan === 'success'" class="hasil">
        <div class="urutan">
          <button :class="{ aktif: arahUrutan === 'asc' }" :aria-pressed="arahUrutan === 'asc'" @click="arahUrutan = 'asc'">
            Urutkan A-Z
          </button>
          <button :class="{ aktif: arahUrutan === 'desc' }" :aria-pressed="arahUrutan === 'desc'" @click="arahUrutan = 'desc'">
            Urutkan Z-A
          </button>
        </div>

        <p role="status">Jumlah hasil: {{ jumlahHasil }}</p>

        <p v-if="jumlahHasil === 0">Tidak ada pengguna yang cocok dengan pencarian.</p>

        <ul v-else class="daftar">
          <li v-for="user in penggunaTerurut" :key="user.id">
            <UserCard :user="user" />
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>
