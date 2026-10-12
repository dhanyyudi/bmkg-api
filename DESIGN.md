# DESIGN.md

Arah desain situs BMKG API (`web/`). Isinya keputusan pemilik proyek, dicatat
pada 12 Oktober 2026. Berkas ini adalah arah; `antislop` hanya penyaring di
atasnya.

## Identitas

Situs ini adalah **lembar peta**. Rujukannya Peta Rupabumi Indonesia (RBI):
muka peta dengan garis tepi, angka koordinat di tepi lembar, kotak keterangan,
skala, dan catatan tepi tentang sumber data.

Alasannya: produk ini menyajikan data kebumian Indonesia (gempa, cuaca,
wilayah). Peta adalah bentuk asli data itu, jadi peta menjadi isi halaman,
bukan hiasan.

## Kesan

Kartografi / atlas. Peta sebagai identitas: garis pantai, grid koordinat,
warna peta cetak.

## Palet

Mengikuti konvensi Peta Rupabumi Indonesia. Setiap warna punya satu peran.

| Warna | Peran |
|---|---|
| Putih kertas | Latar halaman dan muka peta |
| Hitam | Teks, nama tempat, garis tepi |
| Biru | Perairan: isi laut dan nama perairan. Juga tautan dan tombol |
| Hijau | Daratan (vegetasi) pada peta |
| Cokelat | Relief: jejak seismogram dan angka kedalaman |
| Merah | Hal penting: episentrum gempa, peringatan aktif, galat |

Tiga warna inti (biru, hijau, cokelat) dan satu aksen (merah). Hitam dan putih
netral.

## Tipografi

Mengikuti konvensi kartografi:

- Nama perairan: serif miring, biru.
- Nama tempat, judul, dan teks: huruf tegak.
- Angka koordinat dan kode: huruf berlebar tetap.

Keluarga huruf: Source Sans 3, Source Serif 4 (miring), Source Code Pro.
Alasannya: satu keluarga besar menyediakan ketiga suara label peta dengan
proporsi yang serasi.

## Suara

Netral tanpa kata ganti. Kalimat menyatakan apa yang dilakukan API dan datanya,
tanpa menyapa pembaca. Berlaku untuk versi Indonesia dan Inggris.

## Bahasa

Indonesia dan Inggris. Indonesia di `/`, Inggris di `/en/`. Tombol bahasa di
kepala halaman berpindah ke halaman yang sama dalam bahasa lain.

Versi Indonesia tidak menerjemahkan semuanya. Istilah teknis yang lazim dipakai
dalam bahasa Inggris tetap bahasa Inggris: explorer, request, response, rate
limit, API key, client, default, error, envelope, preview, read-only, container,
environment variable, open source, source code. Istilah BMKG (gempa bumi,
prakiraan cuaca, peringatan dini) tetap bahasa Indonesia.

## Logo

Logo yang sudah ada di repo (`web/static/logo.svg`, bola dunia biru dengan
gelombang seismik), dipakai apa adanya.

## Tema

Terang saja. Alasannya: identitasnya lembar peta cetak di atas kertas putih.

## Dial

Dial: ENERGY 2 / RHYTHM 2 / MOTION 2

- ENERGY 2: peta mengisi banner dan menjadi titik fokus; selebihnya tenang.
- RHYTHM 2: tiap bagian punya bentuk sesuai isinya (peta, tabel, alat, catatan
  tepi), dengan kerangka lembar yang sama.
- MOTION 2: gerak hanya untuk menunjukkan urutan waktu dan perpindahan
  pandangan peta.

## Motif identitas

Garis tepi peta dengan angka koordinat, dan kotak **Keterangan** (legenda).
Keduanya muncul di setiap peta pada situs ini.
