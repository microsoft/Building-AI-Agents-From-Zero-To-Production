<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:40:08+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "id"
}
-->
# Langkah Selanjutnya setelah `azd init`

## Daftar Isi

1. [Langkah Selanjutnya](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Menyediakan infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Memodifikasi infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Menuju siap produksi](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Penagihan](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Pemecahan Masalah](../../../../lesson-4-agentdeployment/hosted-agent)

## Langkah Selanjutnya

### Menyediakan infrastruktur dan menerapkan kode aplikasi

Jalankan `azd up` untuk menyediakan infrastruktur Anda dan menerapkan ke Azure dalam satu langkah (atau jalankan `azd provision` lalu `azd deploy` untuk menyelesaikan tugas secara terpisah). Kunjungi endpoint layanan yang tercantum untuk melihat aplikasi Anda berjalan!

Untuk memecahkan masalah apa pun, lihat [pemecahan masalah](../../../../lesson-4-agentdeployment/hosted-agent).

### Memodifikasi infrastruktur

Untuk mendeskripsikan infrastruktur dan aplikasi, `azure.yaml` telah ditambahkan. File ini berisi semua layanan dan sumber daya yang mendeskripsikan aplikasi Anda.

Untuk menambahkan layanan atau sumber daya baru, jalankan `azd add`. Anda juga dapat mengedit file `azure.yaml` secara langsung jika diperlukan.

### Menuju siap produksi

Jika diperlukan, `azd` menghasilkan infrastruktur sebagai kode yang dibutuhkan di memori dan menggunakannya. Jika Anda ingin melihat atau memodifikasi infrastruktur yang digunakan `azd`, jalankan `azd infra gen` untuk menyimpannya ke disk.

Jika Anda melakukan ini, beberapa direktori tambahan akan dibuat:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Catatan*: Setelah Anda menghasilkan infrastruktur ke disk, file-file tersebut menjadi sumber kebenaran untuk azd. Setiap perubahan yang dibuat pada `azure.yaml` (seperti melalui `azd add`) tidak akan tercermin dalam infrastruktur sampai Anda menghasilkan ulang dengan `azd infra gen` lagi. Ini akan meminta konfirmasi sebelum menimpa file. Anda dapat menggunakan `--force` untuk memaksa `azd infra gen` menimpa file tanpa meminta konfirmasi.

Terakhir, jalankan `azd pipeline config` untuk mengonfigurasi pipeline deployment CI/CD.

## Penagihan

Kunjungi halaman *Cost Management + Billing* di Azure Portal untuk melacak pengeluaran saat ini. Untuk informasi lebih lanjut tentang bagaimana Anda ditagih, dan bagaimana Anda dapat memantau biaya yang terjadi di langganan Azure Anda, kunjungi [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Pemecahan Masalah

T: Saya mengunjungi endpoint layanan yang tercantum, dan saya melihat halaman kosong, halaman sambutan umum, atau halaman kesalahan.

J: Layanan Anda mungkin gagal untuk memulai, atau mungkin kehilangan beberapa pengaturan konfigurasi. Untuk menyelidiki lebih lanjut:

1. Jalankan `azd show`. Klik tautan di bawah "View in Azure Portal" untuk membuka grup sumber daya di Azure Portal.
2. Navigasikan ke layanan Container App spesifik yang gagal diterapkan.
3. Klik pada revisi yang gagal di bawah "Revisions with Issues".
4. Tinjau "Status details" untuk informasi lebih lanjut tentang jenis kegagalan.
5. Amati keluaran log dari Console log stream dan System log stream untuk mengidentifikasi kesalahan.
6. Jika log ditulis ke disk, gunakan *Console* di navigasi untuk terhubung ke shell dalam container yang berjalan.

Untuk informasi pemecahan masalah lebih lanjut, kunjungi [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Informasi tambahan

Untuk informasi tambahan tentang menyiapkan proyek `azd` Anda, kunjungi [dokumentasi resmi kami](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diingat bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sahih. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau salah tafsir yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->