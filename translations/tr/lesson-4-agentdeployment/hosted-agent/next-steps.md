<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:35:25+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "tr"
}
-->
# `azd init` Sonrası Sonraki Adımlar

## İçindekiler

1. [Sonraki Adımlar](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Altyapıyı sağlama](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Altyapıyı değiştirme](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Üretime hazır hale getirme](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Faturalandırma](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Sorun Giderme](../../../../lesson-4-agentdeployment/hosted-agent)

## Sonraki Adımlar

### Altyapıyı sağlama ve uygulama kodunu dağıtma

Altyapınızı sağlamak ve Azure'a tek adımda dağıtmak için `azd up` komutunu çalıştırın (veya görevleri ayrı ayrı yapmak için önce `azd provision`, sonra `azd deploy` komutlarını çalıştırın). Uygulamanızın çalıştığını görmek için listelenen servis uç noktalarını ziyaret edin!

Herhangi bir sorunla karşılaşırsanız, [sorun giderme](../../../../lesson-4-agentdeployment/hosted-agent) bölümüne bakın.

### Altyapıyı değiştirme

Altyapıyı ve uygulamayı tanımlamak için `azure.yaml` dosyası eklendi. Bu dosya, uygulamanızı tanımlayan tüm servisleri ve kaynakları içerir.

Yeni servisler veya kaynaklar eklemek için `azd add` komutunu çalıştırın. Gerekirse `azure.yaml` dosyasını doğrudan da düzenleyebilirsiniz.

### Üretime hazır hale getirme

Gerekli altyapı kodunu `azd` gerektiğinde bellekte oluşturur ve kullanır. `azd` tarafından kullanılan altyapıyı görmek veya değiştirmek isterseniz, diske kaydetmek için `azd infra gen` komutunu çalıştırın.

Bunu yaptığınızda, bazı ek dizinler oluşturulacaktır:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Not*: Altyapınızı diske oluşturduktan sonra, bu dosyalar `azd` için gerçek kaynak olur. `azure.yaml` dosyasında yapılan herhangi bir değişiklik (örneğin `azd add` ile) altyapıya yansımayacaktır; altyapıyı tekrar oluşturmak için `azd infra gen` komutunu yeniden çalıştırmanız gerekir. Dosyalar üzerine yazmadan önce size soracaktır. Dosyaların üzerine yazmak için `--force` parametresini kullanabilirsiniz.

Son olarak, bir CI/CD dağıtım hattı yapılandırmak için `azd pipeline config` komutunu çalıştırın.

## Faturalandırma

Mevcut harcamalarınızı takip etmek için Azure Portal'daki *Maliyet Yönetimi + Faturalandırma* sayfasını ziyaret edin. Faturalandırma hakkında daha fazla bilgi ve Azure aboneliklerinizde oluşan maliyetleri nasıl izleyebileceğiniz için [faturalandırma genel bakış](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing) sayfasına bakabilirsiniz.

## Sorun Giderme

S: Listelenen servis uç noktasını ziyaret ettim, ancak boş bir sayfa, genel bir karşılama sayfası veya hata sayfası görüyorum.

C: Servisiniz başlatılamamış olabilir veya bazı yapılandırma ayarları eksik olabilir. Daha fazla incelemek için:

1. `azd show` komutunu çalıştırın. "Azure Portal'da Görüntüle" altındaki bağlantıya tıklayarak kaynak grubunu Azure Portal'da açın.
2. Dağıtımı başarısız olan belirli Container App servisine gidin.
3. "Sorunlu Revizyonlar" altında başarısız olan revizyona tıklayın.
4. Hata türü hakkında daha fazla bilgi için "Durum detayları"nı inceleyin.
5. Hataları belirlemek için Konsol günlük akışı ve Sistem günlük akışı çıktılarının loglarını gözlemleyin.
6. Loglar diske yazılıyorsa, çalışan konteyner içinde bir kabuğa bağlanmak için gezinmedeki *Konsol* bölümünü kullanın.

Daha fazla sorun giderme bilgisi için [Container Apps sorun giderme](https://learn.microsoft.com/azure/container-apps/troubleshooting) sayfasını ziyaret edin.

### Ek bilgi

`azd` projenizi kurma hakkında ek bilgi için resmi [dokümanlarımıza](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert) bakabilirsiniz.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:  
Bu belge, AI çeviri servisi [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba gösterilse de, otomatik çevirilerin hatalar veya yanlışlıklar içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu oluşabilecek yanlış anlamalar veya yorum hatalarından sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->