# 📱 Xcode'a Adım Adım Yükleme Rehberi

> **University Match AI — Projeyi Xcode'a yükleyip App Store'a çıkana kadar her adım**

---

## 📋 İçindekiler

| # | Bölüm | Süre |
|---|-------|------|
| 0 | [Ön Gereksinimler](#adım-0--ön-gereksinimler) | 1 saat (indirme) |
| 1 | [Xcode Kurulumu](#adım-1--xcode-kurulumu) | 10 dk |
| 2 | [Projeyi İndirme (Clone)](#adım-2--projeyi-indirme-clone) | 2 dk |
| 3 | [Projeyi Xcode'da Açma](#adım-3--projeyi-xcodeda-açma) | 1 dk |
| 4 | [Proje Dosyalarını Tanıma](#adım-4--proje-dosyalarını-tanıma) | 5 dk |
| 5 | [Apple Developer Hesabı & Signing](#adım-5--apple-developer-hesabı--signing) | 10 dk |
| 6 | [App Icon Ekleme](#adım-6--app-icon-ekleme) | 5 dk |
| 7 | [Backend API'yi Başlatma](#adım-7--backend-apiyi-başlatma) | 5 dk |
| 8 | [Simulator'da Test](#adım-8--simulatorda-test) | 5 dk |
| 9 | [Gerçek iPhone'da Test](#adım-9--gerçek-iphoneda-test) | 5 dk |
| 10 | [Archive Oluşturma (App Store Build)](#adım-10--archive-oluşturma-app-store-build) | 10 dk |
| 11 | [App Store Connect'e Yükleme](#adım-11--app-store-connecte-yükleme) | 15 dk |
| 12 | [App Store'a Gönderme](#adım-12--app-storea-gönderme) | 10 dk |

---

## Adım 0 — Ön Gereksinimler

Başlamadan önce aşağıdakilere sahip olduğunuzdan emin olun:

| Gereksinim | Açıklama |
|------------|----------|
| **macOS bilgisayar** | Xcode yalnızca Mac'te çalışır (MacBook, iMac, Mac mini, vb.) |
| **macOS 13 Ventura+** | Xcode 15 için minimum macOS sürümü |
| **~15 GB boş disk alanı** | Xcode indirmesi yaklaşık 12 GB |
| **Apple ID** | Ücretsiz Apple ID (test için yeterli) |
| **Apple Developer Program** | App Store'a yüklemek için yıllık $99 ([developer.apple.com](https://developer.apple.com/programs/)) |
| **Git** | Projeyi klonlamak için (macOS'ta zaten yüklü gelir) |
| **Python 3.8+** | Backend API'yi çalıştırmak için |

---

## Adım 1 — Xcode Kurulumu

### 1.1 Xcode'u İndirin

1. Mac'inizde **App Store** uygulamasını açın
2. Arama çubuğuna **"Xcode"** yazın
3. Apple'ın resmi **Xcode** uygulamasını bulun (mavi çekiç ikonu)
4. **"Get" / "İndir"** butonuna tıklayın
5. İndirme tamamlanana kadar bekleyin (~12 GB, internet hızınıza göre 30-60 dk)

> 💡 **Alternatif:** [developer.apple.com/xcode](https://developer.apple.com/xcode/) adresinden de indirebilirsiniz.

### 1.2 Xcode'u İlk Kez Açın

1. **Launchpad** veya **Applications** klasöründen **Xcode**'u açın
2. "Lisans sözleşmesini" kabul edin (**Agree**)
3. Ek bileşenler (Additional Components) yüklemesini bekleyin
4. Xcode açıldığında "Welcome to Xcode" ekranını göreceksiniz — ✅ kurulum tamam!

### 1.3 Command Line Tools'u Doğrulayın

Terminal'i açın ve şu komutu çalıştırın:

```bash
xcode-select --install
```

> Zaten yüklüyse "already installed" mesajı görürsünüz, sorun değil.

---

## Adım 2 — Projeyi İndirme (Clone)

### 2.1 Terminal'den Klonlama

Terminal'i açın (Spotlight'ta "Terminal" arayın) ve şu komutları yazın:

```bash
# Masaüstüne gidin (veya istediğiniz klasöre)
cd ~/Desktop

# Projeyi klonlayın
git clone https://github.com/tekesineren/university-match-ai.git

# Proje klasörüne girin
cd university-match-ai
```

### 2.2 Klasör Yapısını Doğrulayın

```bash
ls ios-app/
```

Şu dosyaları görmelisiniz:

```
UniversityMatchAI.xcodeproj/    ← Xcode proje dosyası
UniversityMatchAI/              ← Swift kaynak kodları
ExportOptions.plist             ← App Store export ayarları
APP_STORE_GUIDE.md              ← App Store rehberi
IOS_SETUP_GUIDE.md              ← Kurulum rehberi
...
```

> ✅ `UniversityMatchAI.xcodeproj` dosyasını görüyorsanız her şey tamam!

---

## Adım 3 — Projeyi Xcode'da Açma

### Yöntem A: Terminal'den (Önerilen)

```bash
cd ios-app
open UniversityMatchAI.xcodeproj
```

### Yöntem B: Finder'dan

1. **Finder** ile `university-match-ai/ios-app/` klasörüne gidin
2. **`UniversityMatchAI.xcodeproj`** dosyasını **çift tıklayın**

### Ne Göreceksiniz

Xcode açıldığında sol taraftaki **Project Navigator** panelinde şu yapıyı göreceksiniz:

```
📁 UniversityMatchAI
├── 📄 UniversityMatchAIApp.swift
├── 📄 ContentView.swift
├── 📄 InputView.swift
├── 📄 ResultsView.swift
├── 📄 Models.swift
├── 📄 APIService.swift
├── 📁 Assets.xcassets
│   ├── 🎨 AccentColor
│   └── 🖼️ AppIcon
├── 📄 Info.plist
└── 📁 Preview Content
```

> ⚠️ Eğer "Trust" (Güven) diyalogu çıkarsa **"Trust and Open"** butonuna tıklayın.

---

## Adım 4 — Proje Dosyalarını Tanıma

Her dosyanın ne işe yaradığını bilmek önemlidir:

| Dosya | Ne İşe Yarar | Dokunmanız Gerekir mi? |
|-------|-------------|------------------------|
| **UniversityMatchAIApp.swift** | Uygulamanın başlangıç noktası (`@main`). `ContentView`'ı başlatır. | ❌ Hayır |
| **ContentView.swift** | Ana ekran — `InputView`'ı gösterir | ❌ Hayır |
| **InputView.swift** | Kullanıcının GPA, dil skoru, background, motivasyon mektubu girdiği form ekranı | ❌ Hayır |
| **ResultsView.swift** | Eşleşme sonuçlarını gösteren ekran (Yüksek / Orta / Düşük eşleşme) | ❌ Hayır |
| **Models.swift** | Veri modelleri: `UserProfile`, `University`, `MatchResponse`, `UserInput` | ❌ Hayır |
| **APIService.swift** | Backend API ile iletişimi sağlar (health check, universities, match) | ⚠️ Production URL'ini değiştirmeniz gerekebilir |
| **Assets.xcassets** | Uygulama ikonu ve renkleri | ✅ App icon eklemeniz gerekir |
| **Info.plist** | Uygulama ayarları (versiyon, izinler, ATS) | ⚠️ Versiyon güncellerken |
| **Preview Content** | SwiftUI önizleme kaynakları | ❌ Hayır |

### API URL Yapılandırması

`APIService.swift` dosyasında API URL'i otomatik olarak ayarlanmıştır:

```swift
#if DEBUG
static let baseURL = "http://localhost:5000/api"      // Geliştirme (Simulator)
#else
static let baseURL = "https://master-application-agent.onrender.com/api"  // Production (App Store)
#endif
```

- **Simulator'da test ederken:** Otomatik olarak `localhost:5000` kullanılır
- **App Store build'de:** Otomatik olarak production URL kullanılır
- **Kendi backend URL'iniz varsa:** `#else` satırındaki URL'i değiştirin

---

## Adım 5 — Apple Developer Hesabı & Signing

### 5.1 Apple ID'yi Xcode'a Ekleyin

1. Xcode menüsünden: **Xcode → Settings** (veya `⌘ + ,`)
2. **Accounts** sekmesine tıklayın
3. Sol altta **"+"** butonuna tıklayın
4. **"Apple ID"** seçin → **Continue**
5. Apple ID e-postanızı ve şifrenizi girin → **Sign In**

> 💡 Sadece simulator'da test için ücretsiz Apple ID yeterlidir.  
> App Store'a yüklemek için **Apple Developer Program** ($99/yıl) gerekir.

### 5.2 Signing Yapılandırması

1. Sol panelde **proje adına** (mavi ikon) tıklayın: `UniversityMatchAI`
2. Ortadaki panelde **TARGETS** altında **UniversityMatchAI** seçin
3. **Signing & Capabilities** sekmesine tıklayın
4. Şu ayarları yapın:

| Ayar | Değer |
|------|-------|
| **Automatically manage signing** | ✅ İşaretli olmalı |
| **Team** | Hesabınızı seçin (Apple ID'niz görünecek) |
| **Bundle Identifier** | `com.masterapplicationagent.app` (değiştirebilirsiniz) |

> ⚠️ "Failed to register bundle identifier" hatası alırsanız → Bundle Identifier'ı benzersiz bir değere değiştirin, örneğin: `com.sizinisminiz.universitymatchai`

### 5.3 Bundle Identifier Değiştirme (Gerekirse)

Bundle Identifier başka biri tarafından kullanılıyorsa:

1. **Signing & Capabilities** sekmesinde **Bundle Identifier** alanını bulun
2. Benzersiz bir değer girin: `com.sizinisminiz.universitymatchai`
3. Xcode otomatik olarak yeni sertifika ve profil oluşturacaktır

---

## Adım 6 — App Icon Ekleme

App Store'a gönderebilmek için bir uygulama ikonu gerekir.

### 6.1 İkon Hazırlama

1. **1024x1024 piksel** boyutunda bir **PNG** dosyası hazırlayın
   - Transparan arka plan **kullanmayın**
   - Kare olmalı (yuvarlak köşeleri Xcode otomatik ekler)
2. Tasarım araçları: [Canva](https://canva.com), [Figma](https://figma.com), [AppIcon.co](https://www.appicon.co/)

### 6.2 Xcode'a İkon Ekleme

1. Sol panelde **Assets.xcassets** dosyasını tıklayın
2. **AppIcon** öğesini seçin
3. Hazırladığınız 1024x1024 PNG dosyasını **sürükleyip bırakın** (drag & drop)
   - "iOS → 1024pt (1x)" kutusuna bırakın

> 💡 Sadece 1024x1024 yeterlidir — iOS 17+ tek boyut kabul eder.

### 6.3 İkon Doğrulama

1. Xcode üst menüsünden: **Product → Clean Build Folder** (⌘ + Shift + K)
2. Tekrar build edin (⌘ + B)
3. Simulator'da uygulamayı çalıştırın — Home ekranında ikonunuzu görmelisiniz

---

## Adım 7 — Backend API'yi Başlatma

Uygulama Simulator'da çalışırken backend API'ye bağlanır. Backend'i çalıştırmanız gerekir.

### 7.1 Backend Bağımlılıklarını Yükleme

**Yeni bir Terminal penceresi** açın (Xcode'daki Terminal'i kapatmayın):

```bash
# Proje ana dizinine gidin
cd ~/Desktop/university-match-ai

# Backend klasörüne gidin
cd backend

# Python bağımlılıklarını yükleyin
pip install -r requirements.txt
```

### 7.2 Backend'i Başlatma

```bash
python app.py
```

Başarılı çıktı:

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 7.3 Backend'in Çalıştığını Doğrulama

Yeni bir Terminal sekmesinde:

```bash
curl http://localhost:5000/api/health
```

Beklenen yanıt:

```json
{"status": "ok", "message": "API is running"}
```

> ✅ Bu yanıtı görüyorsanız backend hazır! Xcode'a dönebilirsiniz.

---

## Adım 8 — Simulator'da Test

### 8.1 Simulator Seçme

1. Xcode'un **üst ortasındaki** cihaz seçiciye tıklayın
2. Bir iPhone seçin: **iPhone 15** veya **iPhone 15 Pro** önerilir

### 8.2 Uygulamayı Çalıştırma

1. **▶️ Run** butonuna basın (veya `⌘ + R`)
2. Simulator açılacak ve uygulama yüklenecek (ilk seferde 1-2 dk sürebilir)

### 8.3 Test Adımları

1. **GPA** alanına bir değer girin (örn: `3.5`)
2. **Dil Skoru** alanına bir değer girin (örn: `100`)
3. **Background** bölümünden en az bir seçenek işaretleyin
4. **Motivation Letter** alanına bir metin yazın
5. **"Eşleştirmeyi Başlat"** butonuna basın
6. Sonuçların geldiğini doğrulayın ✅

### 8.4 Hata Durumunda

| Hata | Çözüm |
|------|-------|
| "Could not connect to server" | Backend'in çalıştığından emin olun (Adım 7) |
| Build hatası | **Product → Clean Build Folder** (⌘+Shift+K) sonra tekrar deneyin |
| Signing hatası | Adım 5'e geri dönün, Team seçtiğinizden emin olun |

---

## Adım 9 — Gerçek iPhone'da Test

### 9.1 Hazırlık

1. iPhone'unuzu **USB kablosu** ile Mac'e bağlayın
2. iPhone'da **"Bu Bilgisayara Güven"** diyaloğunu onaylayın
3. iPhone'un **kilidini açık** tutun

### 9.2 Cihaz Seçimi

1. Xcode üst barındaki cihaz seçiciye tıklayın
2. **"iOS Devices"** bölümünden iPhone'unuzu seçin

### 9.3 Çalıştırma

1. `⌘ + R` ile uygulamayı çalıştırın
2. İlk seferde iPhone'da **"Güvenilmeyen Geliştirici"** uyarısı çıkabilir:
   - iPhone'da: **Ayarlar → Genel → VPN ve Aygıt Yönetimi**
   - Geliştirici uygulamanızı bulun → **"Güven"** deyin

### 9.4 Backend Bağlantısı (Gerçek Cihaz İçin)

Gerçek iPhone'da `localhost` çalışmaz. Bunun yerine Mac'inizin IP adresini kullanmanız gerekir:

1. **Mac'te:** Sistem Ayarları → Wi-Fi → Bağlı ağın yanındaki **(i)** → **IP Address** not edin
   - Örnek: `192.168.1.42`
2. `APIService.swift` dosyasında **geçici olarak** Debug URL'ini değiştirin:

```swift
#if DEBUG
static let baseURL = "http://192.168.1.42:5000/api"  // Mac'inizin IP'si
#else
static let baseURL = "https://master-application-agent.onrender.com/api"
#endif
```

> ⚠️ Mac ve iPhone **aynı Wi-Fi ağında** olmalıdır.  
> 💡 Test bittikten sonra URL'i `localhost` olarak geri değiştirmeyi unutmayın.

---

## Adım 10 — Archive Oluşturma (App Store Build)

App Store'a yüklemek için önce bir Archive oluşturmanız gerekir.

### 10.1 Build Hedefini Ayarlama

1. Xcode üst barındaki cihaz seçiciye tıklayın
2. **"Any iOS Device (arm64)"** seçin (simulator değil!)

### 10.2 Build Kontrolü

1. Menüden: **Product → Build** (`⌘ + B`)
2. Herhangi bir hata olmadığını doğrulayın
3. Xcode alttaki status bar'da **"Build Succeeded"** göstermeli ✅

### 10.3 Archive Oluşturma

1. Menüden: **Product → Archive**
2. Archive işlemi başlayacak (1-3 dk sürebilir)
3. İşlem bittiğinde **Organizer** penceresi otomatik açılır
4. Az önce oluşturulan archive'ı listede göreceksiniz

> ⚠️ **"Archive" menüsü gri/tıklanamaz mı?**  
> Cihaz olarak **"Any iOS Device (arm64)"** seçtiğinizden emin olun. Simulator seçiliyken Archive yapılamaz.

---

## Adım 11 — App Store Connect'e Yükleme

### 11.1 App Store Connect'te Uygulama Oluşturma

1. Tarayıcıda [appstoreconnect.apple.com](https://appstoreconnect.apple.com) adresine gidin
2. Apple Developer hesabınızla giriş yapın
3. **"Apps"** (Uygulamalar) sekmesine tıklayın
4. Sol üstte **"+"** → **"New App"** (Yeni Uygulama) tıklayın
5. Formu doldurun:

| Alan | Değer |
|------|-------|
| **Platforms** | iOS |
| **Name** | University Match AI |
| **Primary Language** | Turkish (veya English) |
| **Bundle ID** | `com.masterapplicationagent.app` (Xcode'daki ile aynı!) |
| **SKU** | `university-match-ai-001` |
| **User Access** | Full Access |

6. **"Create"** (Oluştur) butonuna tıklayın

### 11.2 Uygulama Bilgilerini Doldurun

App Store Connect'te uygulamanızın sayfasında şunları doldurun:

| Bölüm | Ne Yapmalısınız |
|-------|----------------|
| **Screenshots** | iPhone 6.7" ve 6.1" ekran görüntüleri yükleyin (Simulator'dan alabilirsiniz: `⌘+S`) |
| **Description** | Uygulamanın ne yaptığını anlatan Türkçe/İngilizce açıklama |
| **Keywords** | `university, match, master, application, AI, education` |
| **Support URL** | GitHub repo URL'i veya bir web sayfası |
| **Category** | Education |
| **Age Rating** | Soruları yanıtlayın (genelde 4+ uygun) |
| **Privacy Policy URL** | Bir gizlilik politikası sayfası URL'i (zorunlu) |

### 11.3 Xcode'dan App Store Connect'e Yükleme

1. Xcode'da **Window → Organizer** açın (veya Archive sonrası otomatik açılır)
2. Soldaki listeden oluşturduğunuz **archive'ı** seçin
3. Sağ üstte **"Distribute App"** butonuna tıklayın
4. **"App Store Connect"** seçin → **Next**
5. **"Upload"** seçin → **Next**
6. Signing seçeneklerini kontrol edin:
   - **Automatically manage signing:** ✅ İşaretli
   - Doğru Team'in seçili olduğunu doğrulayın
7. **"Upload"** butonuna tıklayın
8. Yükleme tamamlanana kadar bekleyin (2-5 dk)

> ✅ "Upload Successful" mesajını gördüğünüzde build App Store Connect'e yüklenmiştir!

---

## Adım 12 — App Store'a Gönderme

### 12.1 Build'in İşlenmesini Bekleyin

1. App Store Connect'e geri dönün
2. Uygulamanızın sayfasında **"TestFlight"** sekmesine gidin
3. Yüklenen build burada görünecektir (15-30 dk sürebilir)
4. Build durumu **"Ready to Submit"** olana kadar bekleyin

### 12.2 Build'i Seçin

1. **"App Store"** sekmesine geçin
2. **"Build"** bölümünde **"+"** veya **"Select Build"** tıklayın
3. Az önce yüklediğiniz build'i seçin → **Done**

### 12.3 Review'a Gönderin

1. Tüm gerekli alanların doldurulduğundan emin olun (kırmızı uyarılar olmamalı)
2. Sayfanın sağ üstündeki **"Submit for Review"** butonuna tıklayın
3. Onaylayın

### 12.4 Bekleme Süreci

| Aşama | Süre |
|-------|------|
| Build işleme | 15-30 dakika |
| Apple review | Genellikle 24-48 saat |
| Yayınlanma | Review onayı sonrası otomatik veya manuel |

> 📧 Apple, review sonucunu e-posta ile bildirir.  
> Reddedilirse, açıklamayı okuyup gerekli düzeltmeleri yaparak tekrar gönderin.

---

## 🔧 Sorun Giderme

### Sıkça Karşılaşılan Hatalar

| Hata | Çözüm |
|------|-------|
| **"Signing certificate not found"** | Xcode → Settings → Accounts → Apple ID'nizi tekrar ekleyin |
| **"No matching provisioning profile"** | Signing & Capabilities'de "Automatically manage signing" işaretleyin |
| **"App icon is missing"** | Assets.xcassets → AppIcon'a 1024x1024 PNG ekleyin |
| **"Archive" menüsü gri** | Cihaz olarak "Any iOS Device (arm64)" seçin |
| **Build Error: "No such module"** | Product → Clean Build Folder (⌘+Shift+K) ve tekrar build |
| **"Could not connect to server"** | Backend'in çalıştığını kontrol edin (`python app.py`) |
| **iPhone'da "Güvenilmeyen Geliştirici"** | Ayarlar → Genel → VPN ve Aygıt Yönetimi → Güven |
| **"Invalid Bundle"** | Bundle Identifier'ın App Store Connect'teki ile aynı olduğunu kontrol edin |
| **"ITMS-90717: Invalid App Store Icon"** | İkon PNG dosyasının transparan arka planı olmamalı, alpha kanalını kaldırın |

### Temiz Build Yapma

Herhangi bir garip hata durumunda şu adımları deneyin:

```
1. Xcode → Product → Clean Build Folder (⌘ + Shift + K)
2. DerivedData klasörünü silin:
   - Finder'da: ~/Library/Developer/Xcode/DerivedData/
   - UniversityMatchAI ile başlayan klasörü silin
3. Xcode'u kapatıp tekrar açın
4. Tekrar build edin (⌘ + B)
```

---

## 📝 Özet Kontrol Listesi

Aşağıdaki listeyi sırayla takip edin:

- [ ] Xcode yüklü (15.0 veya üstü)
- [ ] Proje klonlandı (`git clone`)
- [ ] `UniversityMatchAI.xcodeproj` Xcode'da açıldı
- [ ] Apple ID Xcode'a eklendi (Settings → Accounts)
- [ ] Signing & Capabilities'de Team seçildi
- [ ] App icon eklendi (1024x1024 PNG)
- [ ] Backend çalışıyor (`python app.py`)
- [ ] Simulator'da test edildi ve çalışıyor
- [ ] (Opsiyonel) Gerçek iPhone'da test edildi
- [ ] Archive oluşturuldu (Product → Archive)
- [ ] App Store Connect'te uygulama oluşturuldu
- [ ] Archive App Store Connect'e yüklendi (Distribute App)
- [ ] Ekran görüntüleri ve açıklamalar eklendi
- [ ] Review'a gönderildi (Submit for Review)

---

## 📚 Ek Kaynaklar

| Kaynak | Link |
|--------|------|
| App Store detaylı rehber | [APP_STORE_GUIDE.md](APP_STORE_GUIDE.md) |
| iOS kurulum rehberi | [IOS_SETUP_GUIDE.md](IOS_SETUP_GUIDE.md) |
| İkon ve launch screen | [ICON_LAUNCH_SCREEN_GUIDE.md](ICON_LAUNCH_SCREEN_GUIDE.md) |
| REST API örnekleri | [REST_API_EXAMPLE.md](REST_API_EXAMPLE.md) |
| Apple Developer docs | [developer.apple.com/documentation](https://developer.apple.com/documentation/) |
| SwiftUI tutorials | [developer.apple.com/tutorials/swiftui](https://developer.apple.com/tutorials/swiftui) |
