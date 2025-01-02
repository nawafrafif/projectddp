import streamlit as st
import pandas as pd
import random
import plotly.express as px

# ----------- Class Rumah ----------- 
class Rumah:
    def __init__(self, id, lokasi, harga, ukuran, kamar_tidur, kamar_mandi, gambar, bahan_bangunan, tahun_pembangunan, kondisi, furnitur):
        self.id = id
        self.lokasi = lokasi
        self.harga = harga
        self.ukuran = ukuran
        self.kamar_tidur = kamar_tidur
        self.kamar_mandi = kamar_mandi
        self.gambar = gambar
        self.bahan_bangunan = bahan_bangunan
        self.tahun_pembangunan = tahun_pembangunan
        self.kondisi = kondisi
        self.furnitur = furnitur

    def harga_per_meter(self):
        """Menghitung harga per meter persegi rumah"""
        return self.harga / self.ukuran

    def simulasi_cicilan(self, bunga_persen, tahun):
        """Menghitung simulasi cicilan per bulan"""
        bunga = bunga_persen / 100
        total_harga = self.harga * (1 + bunga)
        cicilan = total_harga / (tahun * 12)
        return cicilan

    def tampilkan_info(self):
        """Menampilkan informasi rumah dalam format yang mudah dibaca"""
        return f"""
        ID: {self.id}
        Lokasi: {self.lokasi}
        Harga: {self.harga} juta
        Ukuran: {self.ukuran} m²
        Kamar Tidur: {self.kamar_tidur}
        Kamar Mandi: {self.kamar_mandi}
        Harga per meter persegi: {self.harga_per_meter():.2f} juta/m²
        Bahan Bangunan: {self.bahan_bangunan}
        Tahun Pembangunan: {self.tahun_pembangunan}
        Kondisi: {self.kondisi}
        Furnitur: {', '.join(self.furnitur)}
        📞 Kontak: +62 123 456 789
        """

# ----------- Daftar Gambar Rumah (Folder 'image/') ----------- 
gambar_list = [
    "image/rumah1.jpg", "image/rumah2.jpg", "image/rumah3.jpg", "image/rumah4.jpg", "image/rumah5.jpg",
    "image/rumah6.jpg", "image/rumah7.jpg", "image/rumah8.jpg", "image/rumah9.jpg", "image/rumah10.jpg"
]

# ----------- Fungsi Membuat Data Rumah ----------- 
def generate_rumah_data(jumlah):
    lokasi_list = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang", "Medan"]
    bahan_list = ["Beton", "Kayu", "Batu Bata"]
    kondisi_list = ["Baru", "Bekas Terawat", "Butuh Renovasi"]
    furnitur_list = [
        ["Sofa", "Meja Makan", "Lemari Baju"],
        ["Tempat Tidur", "Meja Belajar", "Kursi Santai"],
        ["Kitchen Set", "TV Stand", "Rak Buku"]
    ]
    rumah_data = []
    for i in range(jumlah):
        rumah = Rumah(
            id=i + 1,
            lokasi=random.choice(lokasi_list),
            harga=random.randint(200, 2000),
            ukuran=random.randint(30, 300),
            kamar_tidur=random.randint(1, 5),
            kamar_mandi=random.randint(1, 3),
            gambar=random.choice(gambar_list),
            bahan_bangunan=random.choice(bahan_list),
            tahun_pembangunan=random.randint(2000, 2023),
            kondisi=random.choice(kondisi_list),
            furnitur=random.choice(furnitur_list)
        )
        rumah_data.append(rumah)
    return rumah_data

# ----------- Data Rumah ----------- 
data_rumah = generate_rumah_data(20)

# ----------- Fitur Pencarian Rumah ----------- 
def fitur_pencarian():
    st.header("Pencarian Rumah")
    lokasi = st.selectbox("Pilih Lokasi", options=["Semua"] + list(set([rumah.lokasi for rumah in data_rumah])))
    min_harga = st.slider("Harga Minimum (juta)", 200, 2000, step=100)
    max_harga = st.slider("Harga Maximum (juta)", 200, 2000, step=100, value=2000)
    min_kamar = st.number_input("Jumlah Kamar Tidur Minimum", 1, 5, value=1)
    cari_button = st.button("Cari Rumah")

    if cari_button:
        rumah_terfilter = [
            rumah for rumah in data_rumah
            if (lokasi == "Semua" or rumah.lokasi == lokasi) and
               min_harga <= rumah.harga <= max_harga and
               rumah.kamar_tidur >= min_kamar
        ]
        if rumah_terfilter:
            st.success(f"Ditemukan {len(rumah_terfilter)} rumah:")
            for rumah in rumah_terfilter:
                st.image(rumah.gambar, caption=f"Rumah ID {rumah.id}", use_container_width=True)
                st.write(rumah.tampilkan_info())
        else:
            st.warning("Tidak ada rumah yang sesuai.")

# ----------- Fitur Sistem Cicilan Rumah ----------- 
def fitur_sistem_cicilan():
    st.header("Sistem Cicilan Rumah")
    rumah_id = st.selectbox("Pilih ID Rumah", options=[rumah.id for rumah in data_rumah])
    rumah = next(rumah for rumah in data_rumah if rumah.id == rumah_id)

    bunga = st.slider("Bunga (%)", 1, 10, value=5)
    tahun = st.slider("Cicilan (Tahun)", 1, 30, value=15)
    st.image(rumah.gambar, caption=f"Rumah ID {rumah.id}", use_container_width=True)
    st.write(rumah.tampilkan_info())
    st.write(f"Simulasi Cicilan: {rumah.simulasi_cicilan(bunga, tahun):.2f} juta/bulan")

# ----------- Fitur Detail Rumah ----------- 
def fitur_detail():
    st.header("Detail Rumah")
    rumah_id = st.selectbox("Pilih ID Rumah", options=[rumah.id for rumah in data_rumah])
    rumah = next(rumah for rumah in data_rumah if rumah.id == rumah_id)

    st.image(rumah.gambar, caption=f"Rumah ID {rumah.id}", use_container_width=True)
    st.write(rumah.tampilkan_info())

# ----------- Fitur Perbandingan Rumah ----------- 
def fitur_perbandingan():
    st.header("Perbandingan Rumah")
    selected_ids = st.multiselect("Pilih Rumah untuk Dibandingkan", options=[rumah.id for rumah in data_rumah])
    if len(selected_ids) > 1:
        rumah_terpilih = [rumah for rumah in data_rumah if rumah.id in selected_ids]
        cols = st.columns(len(rumah_terpilih))
        for i, rumah in enumerate(rumah_terpilih):
            with cols[i]:
                st.image(rumah.gambar, caption=f"Rumah ID {rumah.id}", use_container_width=True)
                st.write(rumah.tampilkan_info())
    else:
        st.info("Pilih minimal 2 rumah untuk dibandingkan.")

# ----------- Fitur Ganti Background ----------- 
def fitur_ganti_background():
    st.sidebar.subheader("Pilih Warna Latar")
    warna = st.sidebar.color_picker("Pilih Warna", "#ff0000", label_visibility="collapsed")
    st.sidebar.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {warna};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------- Navigasi dengan Sidebar ----------- 
st.sidebar.title("Navigasi")
fitur_ganti_background()
fitur = st.sidebar.radio(
    "Pilih Fitur",
    options=["Pencarian Rumah", "Sistem Cicilan Rumah", "Detail Rumah", "Perbandingan Rumah"]
)

# ----------- Menjalankan Fitur Berdasarkan Pilihan ----------- 
if fitur == "Pencarian Rumah":
    fitur_pencarian()
elif fitur == "Sistem Cicilan Rumah":
    fitur_sistem_cicilan()
elif fitur == "Detail Rumah":
    fitur_detail()
elif fitur == "Perbandingan Rumah":
    fitur_perbandingan()
