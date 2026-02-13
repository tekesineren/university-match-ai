# 🍎 Hynops iOS App - Kurulum ve App Store Yayınlama Rehberi

Bu rehber, mevcut web uygulamasını Capacitor kullanarak iOS uygulamasına dönüştürme ve App Store'a yükleme adımlarını anlatır.

> **Not:** Uygulama, web versiyonuyla **tamamen aynı** içerik, UI, algoritma ve backend'i kullanır. Capacitor, web uygulamasını native iOS shell içinde çalıştırır.

---

## 📋 Gereksinimler

| Gereksinim | Açıklama |
|-----------|----------|
| **macOS** | Xcode sadece macOS'ta çalışır |
| **Xcode 15+** | Mac App Store'dan indirin (ücretsiz) |
| **Node.js 18+** | [nodejs.org](https://nodejs.org) |
| **Apple Developer Account** | [developer.apple.com](https://developer.apple.com) ($99/yıl) |
| **CocoaPods** | `sudo gem install cocoapods` |

---

## 🚀 Hızlı Başlangıç (5 Adım)

### 1. Bağımlılıkları Yükle

```bash
cd web-app
npm install
```

### 2. iOS Platformunu Ekle

```bash
# İlk seferde iOS platformunu ekle
npm run ios:init
```

Bu komut `web-app/ios/` klasörünü oluşturur ve Xcode projesini hazırlar.

### 3. Web Uygulamasını Build Et ve iOS'a Sync Et

```bash
npm run ios:sync
```

Bu komut:
- `vite build` ile web uygulamasını build eder → `dist/` klasörü oluşur
- `cap sync ios` ile build edilmiş dosyaları iOS projesine kopyalar

### 4. Xcode'da Aç

```bash
npm run ios:open
```

### 5. Simulator'da Test Et

Xcode'da:
1. Üst kısımdan bir iPhone simulator seçin (örn: iPhone 15 Pro)
2. ▶️ **Run** butonuna basın
3. Uygulama simulator'da açılacak

---

## 📱 App Store'a Yükleme

### Adım 1: Apple Developer Hesabı Ayarları

1. [developer.apple.com](https://developer.apple.com) adresine gidin
2. **Account** → **Certificates, Identifiers & Profiles** seçin
3. **Identifiers** → **+** butonuyla yeni App ID oluşturun:
   - **Bundle ID:** `com.masterapplicationagent.app`
   - **Description:** Hynops

### Adım 2: App Store Connect'te Uygulama Oluşturun

1. [appstoreconnect.apple.com](https://appstoreconnect.apple.com) adresine gidin
2. **My Apps** → **+** → **New App**
3. Bilgileri doldurun:
   - **Name:** Hynops
   - **Primary Language:** Turkish
   - **Bundle ID:** `com.masterapplicationagent.app`
   - **SKU:** hynops-ios

### Adım 3: Xcode'da Signing Ayarları

1. `npm run ios:open` ile Xcode'u açın
2. Sol panelde **App** projesini seçin
3. **Signing & Capabilities** sekmesine gidin
4. **Team:** Apple Developer hesabınızı seçin
5. **Bundle Identifier:** `com.masterapplicationagent.app` olduğundan emin olun
6. **Automatically manage signing** işaretli olsun

### Adım 4: App Icon Ekle

1. Xcode'da `Assets.xcassets` → `AppIcon` setini açın
2. 1024x1024 PNG icon dosyasını sürükleyip bırakın
3. Xcode otomatik olarak tüm boyutları oluşturacak

> **İpucu:** `generated-icon.png` dosyasını kullanabilir veya [appicon.co](https://appicon.co) sitesinden tüm boyutları oluşturabilirsiniz.

### Adım 5: Splash Screen (Başlangıç Ekranı)

Capacitor config'de splash screen ayarları zaten yapılmış durumda. Özelleştirmek için:

1. Xcode'da `Assets.xcassets` → `Splash` setini düzenleyin
2. Veya `capacitor.config.json` dosyasındaki `SplashScreen` ayarlarını değiştirin

### Adım 6: Archive ve Upload

1. Xcode'da üst menüden **Product** → **Archive** seçin
   - Build target'ın **Any iOS Device** olduğundan emin olun (simulator değil)
2. Archive tamamlandığında **Organizer** penceresi açılır
3. **Distribute App** → **App Store Connect** seçin
4. **Upload** → varsayılan ayarlarla devam edin
5. Upload tamamlandığında App Store Connect'te build'i görürsünüz

### Adım 7: App Store Connect'te Yayınla

1. [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → uygulamanız
2. **App Store** sekmesinde bilgileri doldurun:
   - **Screenshots:** iPhone 6.7" ve 5.5" ekran görüntüleri
   - **Description:** Uygulama açıklaması
   - **Keywords:** Anahtar kelimeler
   - **Support URL:** Destek sayfası
   - **Privacy Policy URL:** Gizlilik politikası
3. **Build** bölümünde yüklediğiniz build'i seçin
4. **Submit for Review** butonuna basın

---

## 🔧 Yapılandırma

### API URL Değiştirme

Uygulama varsayılan olarak `https://hynops.com/api` backend'ini kullanır. Değiştirmek için:

```bash
# web-app/.env dosyası oluşturun
VITE_API_URL=https://your-backend-url.com/api
```

Sonra yeniden build edin:
```bash
npm run ios:sync
```

### Capacitor Ayarları

`web-app/capacitor.config.json` dosyasından ayarları değiştirebilirsiniz:

```json
{
  "appId": "com.masterapplicationagent.app",
  "appName": "Hynops",
  "webDir": "dist",
  "plugins": {
    "SplashScreen": { ... },
    "StatusBar": { ... },
    "Keyboard": { ... }
  }
}
```

---

## 📁 Proje Yapısı

```
web-app/
├── src/                    # React kaynak kodu (web ve iOS aynı)
│   ├── components/         # UI bileşenleri
│   ├── utils/
│   │   ├── api.js         # API URL yönetimi (Capacitor/web algılama)
│   │   ├── cvParser.js    # CV ayrıştırıcı
│   │   └── analytics.js   # Analitik
│   ├── App.jsx            # Ana uygulama
│   └── main.jsx           # Giriş noktası (Capacitor başlatma)
├── dist/                   # Build çıktısı (iOS'a kopyalanır)
├── ios/                    # Capacitor iOS projesi (cap add ios sonrası)
│   ├── App/
│   │   ├── App.xcodeproj  # Xcode projesi
│   │   └── App/
│   │       └── public/    # Web build dosyaları
│   └── Podfile            # CocoaPods bağımlılıkları
├── capacitor.config.json   # Capacitor yapılandırması
├── package.json           # Bağımlılıklar ve scripts
└── vite.config.js         # Vite yapılandırması
```

---

## 🔄 Güncelleme Akışı

Web uygulamasında değişiklik yaptığınızda iOS'u güncellemek için:

```bash
cd web-app
npm run ios:sync
```

Bu, web uygulamasını build edip iOS projesine kopyalar. Ardından Xcode'dan tekrar Archive/Upload yapın.

---

## ❓ Sık Sorulan Sorular

### Uygulama web versiyonuyla aynı mı?
Evet. Capacitor, web uygulamasını native WebView içinde çalıştırır. UI, algoritma ve tüm işlevsellik **birebir aynıdır**.

### Backend ayrı mı çalışıyor?
Evet. Backend (`hynops.com/api`) web ve iOS versiyonu tarafından ortaklaşa kullanılır. Ayrı bir backend kurmaya gerek yoktur.

### iOS'a özel değişiklikler neler?
- **Safe area desteği:** iPhone notch/çentik alanları için CSS padding
- **Status bar:** Native renklendirme
- **Splash screen:** Uygulama açılış ekranı
- **Keyboard:** Klavye açıldığında otomatik ekran ayarı
- **API URL:** Capacitor ortamında doğrudan backend URL'i kullanılır (proxy yerine)

### App Store review'da reddedilir mi?
WebView tabanlı uygulamalar Apple tarafından kabul edilir, ancak şunlara dikkat edin:
- Uygulamanın bir web sitesinin basit sarmalayıcısı olmadığından emin olun (CV parsing, offline destek gibi native özellikler ekleyebilirsiniz)
- Privacy policy sayfanız olsun
- Uygulama açıklaması doğru ve eksiksiz olsun

---

## 🆘 Sorun Giderme

| Sorun | Çözüm |
|-------|--------|
| `cap add ios` hata veriyor | `npm install` çalıştırın, Node.js 18+ olduğundan emin olun |
| Xcode build hatası | **Product** → **Clean Build Folder** deneyin |
| CocoaPods hatası | `cd ios/App && pod install --repo-update` |
| API bağlantı hatası | Backend URL'inin doğru olduğunu kontrol edin |
| Simulator'da beyaz ekran | `npm run ios:sync` tekrar çalıştırın |
| Signing hatası | Apple Developer hesabınızı Xcode'a ekleyin |
