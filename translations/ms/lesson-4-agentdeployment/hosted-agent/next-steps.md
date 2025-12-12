<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:40:38+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "ms"
}
-->
# Langkah Seterusnya selepas `azd init`

## Jadual Kandungan

1. [Langkah Seterusnya](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Menyediakan infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Mengubah suai infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Mendapatkan kesediaan produksi](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Pengebilan](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Penyelesaian Masalah](../../../../lesson-4-agentdeployment/hosted-agent)

## Langkah Seterusnya

### Menyediakan infrastruktur dan melaksanakan kod aplikasi

Jalankan `azd up` untuk menyediakan infrastruktur anda dan melaksanakan ke Azure dalam satu langkah (atau jalankan `azd provision` kemudian `azd deploy` untuk melaksanakan tugasan secara berasingan). Lawati titik akhir perkhidmatan yang disenaraikan untuk melihat aplikasi anda berfungsi!

Untuk menyelesaikan sebarang isu, lihat [penyelesaian masalah](../../../../lesson-4-agentdeployment/hosted-agent).

### Mengubah suai infrastruktur

Untuk menerangkan infrastruktur dan aplikasi, `azure.yaml` telah ditambah. Fail ini mengandungi semua perkhidmatan dan sumber yang menerangkan aplikasi anda.

Untuk menambah perkhidmatan atau sumber baru, jalankan `azd add`. Anda juga boleh mengedit fail `azure.yaml` secara langsung jika perlu.

### Mendapatkan kesediaan produksi

Apabila diperlukan, `azd` menjana infrastruktur sebagai kod yang diperlukan dalam memori dan menggunakannya. Jika anda ingin melihat atau mengubah suai infrastruktur yang digunakan oleh `azd`, jalankan `azd infra gen` untuk menyimpannya ke cakera.

Jika anda melakukan ini, beberapa direktori tambahan akan dibuat:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Nota*: Setelah anda menjana infrastruktur anda ke cakera, fail-fail tersebut adalah sumber kebenaran untuk azd. Sebarang perubahan yang dibuat pada `azure.yaml` (seperti melalui `azd add`) tidak akan tercermin dalam infrastruktur sehingga anda menjana semula dengan `azd infra gen` sekali lagi. Ia akan meminta pengesahan sebelum menulis ganti fail. Anda boleh menggunakan `--force` untuk memaksa `azd infra gen` menulis ganti fail tanpa meminta pengesahan.

Akhir sekali, jalankan `azd pipeline config` untuk mengkonfigurasi saluran pelaksanaan CI/CD.

## Pengebilan

Lawati halaman *Pengurusan Kos + Pengebilan* di Azure Portal untuk menjejak perbelanjaan semasa. Untuk maklumat lanjut tentang bagaimana anda dikenakan bayaran, dan bagaimana anda boleh memantau kos yang ditanggung dalam langganan Azure anda, lawati [gambaran keseluruhan pengebilan](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Penyelesaian Masalah

S: Saya melawat titik akhir perkhidmatan yang disenaraikan, dan saya melihat halaman kosong, halaman sambutan generik, atau halaman ralat.

J: Perkhidmatan anda mungkin gagal untuk dimulakan, atau mungkin kekurangan beberapa tetapan konfigurasi. Untuk menyiasat lebih lanjut:

1. Jalankan `azd show`. Klik pada pautan di bawah "View in Azure Portal" untuk membuka kumpulan sumber di Azure Portal.
2. Navigasi ke perkhidmatan Container App tertentu yang gagal dilaksanakan.
3. Klik pada semakan yang gagal di bawah "Revisions with Issues".
4. Semak "Status details" untuk maklumat lanjut tentang jenis kegagalan.
5. Perhatikan output log dari Console log stream dan System log stream untuk mengenal pasti sebarang ralat.
6. Jika log ditulis ke cakera, gunakan *Console* dalam navigasi untuk menyambung ke shell dalam kontena yang sedang berjalan.

Untuk maklumat penyelesaian masalah lanjut, lawati [penyelesaian masalah Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Maklumat tambahan

Untuk maklumat tambahan tentang menyediakan projek `azd` anda, lawati [dokumen rasmi kami](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan profesional oleh manusia adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->