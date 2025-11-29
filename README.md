🖼️ Görsel Envanter Arama Motoru (Visual Inventory Search Engine)
Görüntü İşleme (Image Processing) tabanlı, envanter ve stok yönetimi için geliştirilmiş hızlı ve güvenilir arama çözümü.

✨ Proje Hakkında
Bu proje, bir işletmenin elindeki büyük ürün görseli veritabanında hızlı ve doğru arama yapabilmesi için geliştirilmiş kurumsal bir araçtır. Geleneksel metin tabanlı aramanın aksine, sistem yüklenen bir görseli analiz eder ve veritabanındaki diğer görsellerle benzerlik ölçümleri yaparak en alakalı sonuçları ve bu sonuçların yüzdelik benzerlik skorlarını sunar.

Bu uygulama, özellikle binlerce farklı stok birimine (SKU) sahip perakende, üretim ve lojistik sektörlerindeki işletmeler için vazgeçilmez bir hız ve doğruluk sağlar.

💡 İşletmeler İçin Neden Kullanışlı? (Değer Teklifi)
Bu görsel arama motoru, işletmelerin karşılaştığı yaygın envanter sorunlarına doğrudan çözüm sunar:

Hızlı Stok Doğrulama:

Depo veya mağaza çalışanları, ürünün barkodunu okutmak veya karmaşık bir SKU girmek yerine, sadece fotoğrafını çekip anında sistemde aratabilir. Bu, hatalı girişleri ve zaman kaybını sıfırlar.

Kullanım Senaryosu: Yeni gelen bir ürünün daha önce sisteme girip girmediği, sadece fotoğraf yüklenerek saniyeler içinde kontrol edilir.

Hatalı Giriş ve Çift Kayıt Önleme:

Bir ürünün farklı açılardan veya hafif farklı versiyonlarının yanlışlıkla birden fazla SKU ile sisteme kaydedilmesini engeller. Yüksek benzerlik skorları sayesinde sistem, çalışanı potansiyel çift kayıtlara karşı uyarır.

Kalite Kontrol ve Uyum:

Üretim sonrası kalite kontrol süreçlerinde, üretilen ürün görselinin (numunenin) orijinal tasarıma ne kadar benzediğini yüzdelik skorlarla hızlıca karşılaştırır.

Müşteri Hizmetleri Hızı:

Müşteri, aradığı ürünü sadece bir görselle sorduğunda (örneğin e-ticaret sitenizdeki bir görselle), ilgili stok kodunu saniyeler içinde bulup müşteriye hizmet verebilirsiniz.

## Kullanılan Teknolojiler

| Kategori                           | Teknoloji                               | Açıklama |
|------------------------------------|-------------------------------------------|----------|
| **Backend / API**                  | Python / Flask                            | Uygulamanın web arayüzünü, istek yönetimini ve işleme mantığını sağlayan hafif ve hızlı web çatısı. |
| **Derin Öğrenme (DL) & Özellik Çıkarımı** | TensorFlow / Keras (MobileNetV2)         | Görüntüden yüksek boyutlu, ayırt edici özellik vektörlerini (Embeddings) çıkarmak için kullanılan önceden eğitilmiş Evrişimsel Sinir Ağı (CNN) modeli. |
| **Vektör Veritabanı & Arama Motoru** | FAISS (Facebook AI Similarity Search)     | Çıkarılan 1280 boyutlu özellik vektörleri üzerinde milyarlarca kat daha hızlı en yakın komşu araması (Approximate Nearest Neighbor) yaparak arama hızını maksimize eden kütüphane. |
| **Veritabanı**                     | SQLite3                                   | Ürünlerin meta verilerini (Ad, Fiyat, Stok, Kategori, vb.) depolamak ve sorgulamak için kullanılan hafif ve sunucusuz veritabanı. |
| **Arayüz (Frontend)**              | HTML / CSS / Bootstrap                    | Kurumsal kimliğe uygun, responsive (duyarlı) ve modern kontrol paneli arayüzü. |


## Notlar ve Gelişim Planı

Bu proje şu anda ağırlıklı olarak **görsel arama motorunun** geliştirilmesine odaklanmaktadır.  
Backend yapısı (API uç noktaları, yönetim paneli işlemleri, gelişmiş ürün yönetimi vb.) ilerleyen aşamalarda genişletilecek ve projeye ek yeni modüller ile desteklenecektir.

Mevcut öncelik:
- **Görüntülerden özellik çıkarımı**
- **Vektör arama motoru ile en yakın eşleşmelerin bulunması**
- **Hızlı ve doğru görsel arama deneyiminin optimize edilmesi**

Gelecekte eklenecek başlıca bölümler:
- Gelişmiş Backend/API mimarisi  
- Yetkilendirme & kimlik doğrulama  
- Ürün yönetim paneli iyileştirmeleri  
- Daha gelişmiş arayüz iyileştirmeleri  
- Entegrasyon özellikleri (REST / Webhook / diğer sistemler)

Proje aktif olarak geliştirilmektedir ve yeni bileşenler zamanla eklenmeye devam edecektir.

