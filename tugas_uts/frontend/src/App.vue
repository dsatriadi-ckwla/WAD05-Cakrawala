<script setup>
import { computed, onMounted, ref } from 'vue'

const apiUrl = 'http://127.0.0.1:8001/barang'
const batasMenipis = 5
const barang = ref([])
const pencarian = ref('')
const urutan = ref('asc')
const loading = ref(true)
const menyimpan = ref(false)
const menghapus = ref(null)
const konfirmasiHapus = ref(null)
const formulirTerbuka = ref(false)
const error = ref('')
const pesan = ref('')
const gagalMemuat = ref(false)
const form = ref({ nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' })

const hasilPencarian = computed(() => {
  const kata = pencarian.value.trim().toLocaleLowerCase('id')
  return barang.value.filter((item) =>
    item.nama.toLocaleLowerCase('id').includes(kata) ||
    item.kategori.toLocaleLowerCase('id').includes(kata)
  )
})

const barangTerurut = computed(() => [...hasilPencarian.value].sort((a, b) =>
  urutan.value === 'asc'
    ? a.nama.localeCompare(b.nama, 'id')
    : b.nama.localeCompare(a.nama, 'id')
))

const totalBarang = computed(() => barang.value.reduce((jumlah) => jumlah + 1, 0))
const perluPerhatian = computed(() => barang.value.filter((item) => item.jumlah_stok <= batasMenipis).length)
const jumlahKategori = computed(() => new Set(barang.value.map((item) => item.kategori)).size)
const totalUnit = computed(() => barang.value.reduce((jumlah, item) => jumlah + item.jumlah_stok, 0))

function statusStok(stok) {
  if (stok === 0) return 'Habis'
  if (stok <= batasMenipis) return 'Menipis'
  return 'Aman'
}

function kelasStok(stok) {
  if (stok === 0) return 'habis'
  if (stok <= batasMenipis) return 'menipis'
  return 'aman'
}

async function muatBarang() {
  loading.value = true
  error.value = ''
  gagalMemuat.value = false
  try {
    const respons = await fetch(apiUrl)
    if (!respons.ok) throw new Error('Gagal memuat barang')
    barang.value = await respons.json()
  } catch {
    gagalMemuat.value = true
    error.value = 'Data belum bisa dimuat. Periksa apakah backend sudah berjalan, lalu coba lagi.'
  } finally {
    loading.value = false
  }
}

async function tambahBarang() {
  menyimpan.value = true
  error.value = ''
  pesan.value = ''
  try {
    const respons = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (!respons.ok) throw new Error('Gagal menambah barang')
    form.value = { nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' }
    formulirTerbuka.value = false
    await muatBarang()
    if (!error.value) pesan.value = 'Barang berhasil ditambahkan.'
  } catch {
    error.value = 'Barang belum bisa ditambahkan. Periksa data dan koneksi backend.'
  } finally {
    menyimpan.value = false
  }
}

async function hapusBarang(item) {
  menghapus.value = item.id
  error.value = ''
  pesan.value = ''
  try {
    const respons = await fetch(`${apiUrl}/${item.id}`, { method: 'DELETE' })
    if (!respons.ok) throw new Error('Gagal menghapus barang')
    await muatBarang()
    if (!error.value) pesan.value = `${item.nama} berhasil dihapus.`
  } catch {
    error.value = 'Barang belum bisa dihapus. Coba lagi.'
  } finally {
    menghapus.value = null
    konfirmasiHapus.value = null
  }
}

onMounted(muatBarang)
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="topbar-inner">
        <span class="brand-mark" aria-hidden="true">DS</span>
        <span class="brand-name">Inventaris Klinik Estetika</span>
        <span class="topbar-label">Dashboard UTS</span>
      </div>
    </header>

    <main class="container">
      <div class="page-heading">
        <div>
          <p class="eyebrow">SIMULASI DATA · DHARMA SATRIADI</p>
          <h1>Stok klinik bedah plastik estetika</h1>
          <p class="intro">Pantau perlengkapan konsultasi, tindakan, dan perawatan pascatindakan.</p>
        </div>
        <button class="primary-button heading-action" type="button" @click="formulirTerbuka = !formulirTerbuka">
          {{ formulirTerbuka ? 'Tutup formulir' : '+ Tambah barang' }}
        </button>
      </div>

      <section class="stats" aria-label="Ringkasan inventaris">
        <div class="stat"><span>Total barang</span><strong>{{ totalBarang }}</strong><small>jenis barang</small></div>
        <div class="stat stat-alert"><span>Perlu perhatian</span><strong>{{ perluPerhatian }}</strong><small>menipis atau habis</small></div>
        <div class="stat"><span>Kategori</span><strong>{{ jumlahKategori }}</strong><small>kelompok barang</small></div>
        <div class="stat"><span>Total unit</span><strong>{{ totalUnit }}</strong><small>seluruh stok</small></div>
      </section>

      <section v-if="formulirTerbuka" class="panel form-panel" aria-labelledby="form-title">
        <div class="section-heading">
          <div>
            <h2 id="form-title">Tambah barang</h2>
            <p>Isi data barang yang akan masuk daftar.</p>
          </div>
        </div>
        <form class="barang-form" @submit.prevent="tambahBarang">
          <label>Nama barang<input v-model.trim="form.nama" type="text" maxlength="100" required placeholder="Contoh: Kasa steril" /></label>
          <label>Kategori<input v-model.trim="form.kategori" type="text" maxlength="60" required placeholder="Contoh: Tindakan" /></label>
          <label>Jumlah stok<input v-model.number="form.jumlah_stok" type="number" min="0" step="1" required /></label>
          <label>Lokasi gudang<input v-model.trim="form.lokasi_gudang" type="text" maxlength="100" required placeholder="Contoh: Gudang Klinik" /></label>
          <div class="form-actions"><button class="primary-button" type="submit" :disabled="menyimpan">{{ menyimpan ? 'Menyimpan…' : 'Simpan barang' }}</button></div>
        </form>
      </section>

      <div v-if="error" class="notice notice-error" role="alert">{{ error }} <button v-if="gagalMemuat" type="button" @click="muatBarang">Coba lagi</button></div>
      <div v-if="pesan" class="notice notice-success" role="status">{{ pesan }}</div>

      <section class="panel list-panel" aria-labelledby="list-title">
        <div class="section-heading list-heading">
          <div>
            <h2 id="list-title">Daftar barang</h2>
            <p>Data contoh untuk tugas UTS, bukan catatan stok resmi.</p>
          </div>
          <span class="count">{{ hasilPencarian.length }} dari {{ totalBarang }} barang</span>
        </div>

        <div class="toolbar">
          <label class="search-label">Cari nama atau kategori
            <input v-model="pencarian" type="search" placeholder="Cari barang…" />
          </label>
          <div class="sort-controls" aria-label="Urutkan nama barang">
            <button type="button" :class="{ active: urutan === 'asc' }" :aria-pressed="urutan === 'asc'" @click="urutan = 'asc'">A–Z</button>
            <button type="button" :class="{ active: urutan === 'desc' }" :aria-pressed="urutan === 'desc'" @click="urutan = 'desc'">Z–A</button>
          </div>
        </div>

        <div v-if="loading" class="state" role="status">Memuat daftar barang…</div>
        <div v-else-if="error && barang.length === 0" class="state">Daftar belum tersedia.</div>
        <div v-else-if="barangTerurut.length === 0" class="state">{{ pencarian ? 'Tidak ada barang yang cocok dengan pencarian.' : 'Belum ada barang.' }}</div>
        <div v-else class="table-scroll">
          <table>
            <thead><tr><th scope="col">Nama barang</th><th scope="col">Kategori</th><th scope="col">Lokasi gudang</th><th scope="col">Stok</th><th scope="col">Status</th><th scope="col">Tindakan</th></tr></thead>
            <tbody>
              <tr v-for="item in barangTerurut" :key="item.id">
                <td class="item-name">{{ item.nama }}</td>
                <td>{{ item.kategori }}</td>
                <td>{{ item.lokasi_gudang }}</td>
                <td class="stock-number">{{ item.jumlah_stok }}</td>
                <td><span class="badge" :class="kelasStok(item.jumlah_stok)">{{ statusStok(item.jumlah_stok) }}</span></td>
                <td class="action-cell">
                  <div v-if="konfirmasiHapus === item.id" class="delete-confirm">
                    <span>Hapus?</span>
                    <button type="button" :disabled="menghapus === item.id" @click="konfirmasiHapus = null">Batal</button>
                    <button class="delete-button" type="button" :disabled="menghapus === item.id" :aria-label="`Ya, hapus ${item.nama}`" @click="hapusBarang(item)">{{ menghapus === item.id ? 'Menghapus…' : 'Ya' }}</button>
                  </div>
                  <button v-else class="delete-button" type="button" :aria-label="`Hapus ${item.nama}`" @click="konfirmasiHapus = item.id">Hapus</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
      <p class="footer-note">Ambang stok: 0 habis · 1–5 menipis · lebih dari 5 aman</p>
    </main>
  </div>
</template>
