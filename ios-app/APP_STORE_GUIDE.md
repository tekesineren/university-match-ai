# 🚀 App Store'a Yayınlama Rehberi

Bu rehber, **University Match AI** uygulamasını Xcode üzerinden App Store'a yayınlamak için gereken tüm adımları içerir.

## 📋 Ön Gereksinimler

- **macOS** bilgisayar (Xcode sadece macOS'ta çalışır)
- **Xcode 15.0+** yüklü olmalı ([Mac App Store'dan indirin](https://apps.apple.com/app/xcode/id497799835))
- **Apple Developer Program** üyeliği (yıllık $99) — [developer.apple.com](https://developer.apple.com/programs/)
- **Apple ID** ile Xcode'a giriş yapılmış olmalı

---

## 1️⃣ Projeyi Xcode'da Açma

```bash
# Terminal'de proje dizinine gidin
cd ios-app

# Xcode projesini açın
open UniversityMatchAI.xcodeproj
```

Veya Finder'dan `ios-app/UniversityMatchAI.xcodeproj` dosyasını çift tıklayarak açabilirsiniz.

---

## 2️⃣ Signing & Team Yapılandırması

1. Xcode'da proje navigator'dan **UniversityMatchAI** projesine tıklayın
2. **Signing & Capabilities** sekmesine gidin
3. **Team** alanından Apple Developer hesabınızı seçin
4. **Bundle Identifier** alanını kontrol edin: `com.masterapplicationagent.app`
   - Eğer bu ID başkası tarafından kullanılıyorsa, benzersiz bir ID belirleyin
5. **Automatically manage signing** seçeneğinin işaretli olduğundan emin olun

---

## 3️⃣ App Icon Ekleme

1. `UniversityMatchAI/Assets.xcassets/AppIcon.appiconset/` klasörüne gidin
2. **1024x1024 piksel** boyutunda bir PNG app ikonu hazırlayın
3. İkonu `AppIcon.appiconset` klasörüne `AppIcon.png` adıyla koyun
4. `Contents.json` dosyasını güncelleyin:

```json
{
  "images" : [
    {
      "filename" : "AppIcon.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

---

## 4️⃣ API URL Yapılandırması

### Geliştirme (Debug)
Simulator kullanırken otomatik olarak `localhost:5000` kullanılır.

### Production (Release)
Release build'de otomatik olarak production URL kullanılır.  
`APIService.swift` dosyasında yapılandırma:

```swift
#if DEBUG
static let baseURL = "http://localhost:5000/api"
#else
static let baseURL = "https://master-application-agent.onrender.com/api"
#endif
```

Production URL'inizi değiştirmek isterseniz `APIService.swift` dosyasındaki `baseURL` değerini güncelleyin.

---

## 5️⃣ Build & Test

### Simulator'da Test
1. Xcode'da üst kısımdan bir iPhone simulator seçin (örn: iPhone 15)
2. **⌘ + R** (Cmd + R) ile uygulamayı çalıştırın
3. Tüm ekranları ve fonksiyonları test edin

### Gerçek Cihazda Test
1. iPhone'unuzu Mac'e USB ile bağlayın
2. Xcode'da cihazınızı hedef olarak seçin
3. **⌘ + R** ile uygulamayı cihaza yükleyin

---

## 6️⃣ Archive Oluşturma

1. Xcode'da hedef cihazı **"Any iOS Device (arm64)"** olarak seçin
2. Menüden **Product → Archive** seçin (veya **⌘ + Shift + .) tuşlarına basın)
3. Archive işlemi tamamlandığında **Organizer** penceresi açılır

---

## 7️⃣ App Store Connect Hazırlığı

### App Store Connect'te Yeni Uygulama Oluşturma
1. [appstoreconnect.apple.com](https://appstoreconnect.apple.com) adresine gidin
2. **My Apps** → **+** → **New App** tıklayın
3. Aşağıdaki bilgileri doldurun:

| Alan | Değer |
|------|-------|
| Platform | iOS |
| Name | University Match AI |
| Primary Language | English (veya Turkish) |
| Bundle ID | com.masterapplicationagent.app |
| SKU | university-match-ai-001 |

### Uygulama Bilgilerini Doldurun
- **Açıklama**: Uygulamanızın ne yaptığını anlatan metin
- **Anahtar Kelimeler**: university, match, master, application, AI
- **Ekran Görüntüleri**: iPhone 6.7" ve 6.1" boyutlarında ekran görüntüleri
- **App Icon**: 1024x1024 PNG
- **Kategori**: Education
- **Yaş Sınıflandırması**: 4+ (uygun şekilde doldurun)
- **Gizlilik Politikası URL'i**: Gerekli bir URL

---

## 8️⃣ App Store'a Yükleme

### Xcode Organizer'dan Yükleme
1. Organizer'da oluşturduğunuz archive'ı seçin
2. **Distribute App** butonuna tıklayın
3. **App Store Connect** seçin → **Next**
4. **Upload** seçin → **Next**
5. Signing seçeneklerini onaylayın → **Upload**

### Alternatif: Transporter Uygulaması
1. Mac App Store'dan **Transporter** uygulamasını indirin
2. Xcode'dan Export ettiğiniz `.ipa` dosyasını Transporter'a sürükleyin
3. **Deliver** butonuna tıklayın

---

## 9️⃣ App Review'a Gönderme

1. App Store Connect'te uygulamanıza gidin
2. Yüklenen build'in işlenmesini bekleyin (genellikle 15-30 dakika)
3. Build'i seçin
4. Tüm gerekli alanların doldurulduğundan emin olun
5. **Submit for Review** butonuna tıklayın

### Review Süresi
- Genellikle **24-48 saat** içinde sonuçlanır
- Reddedilirse, Apple'ın açıklamasını okuyup düzeltmeleri yaparak tekrar gönderin

---

## 📁 Proje Dosya Yapısı

```
ios-app/
├── UniversityMatchAI.xcodeproj/       # Xcode proje dosyası
│   ├── project.pbxproj                # Proje yapılandırması
│   └── xcshareddata/
│       └── xcschemes/
│           └── UniversityMatchAI.xcscheme  # Build şeması
├── UniversityMatchAI/                  # Kaynak kod dizini
│   ├── UniversityMatchAIApp.swift     # @main giriş noktası
│   ├── ContentView.swift              # Ana görünüm
│   ├── InputView.swift                # Kullanıcı giriş formu
│   ├── ResultsView.swift              # Sonuç ekranı
│   ├── Models.swift                   # Veri modelleri
│   ├── APIService.swift               # API servisi
│   ├── Info.plist                     # Uygulama yapılandırması
│   ├── Assets.xcassets/               # Görsel kaynaklar
│   │   ├── AppIcon.appiconset/        # App ikonu (1024x1024 PNG ekleyin)
│   │   └── AccentColor.colorset/      # Tema rengi
│   └── Preview Content/               # SwiftUI önizleme kaynakları
└── ExportOptions.plist                # App Store dışa aktarma seçenekleri
```

---

## ⚠️ Yaygın Sorunlar ve Çözümleri

### "Signing Certificate" Hatası
- Xcode → Settings → Accounts → Apple ID'nizi ekleyin
- Signing & Capabilities'de Team'inizi seçin

### "No matching provisioning profile" Hatası
- Xcode'un otomatik signing yapmasına izin verin
- Bundle ID'nin doğru olduğundan emin olun

### "App icon is missing" Hatası
- `Assets.xcassets/AppIcon.appiconset/` klasörüne 1024x1024 PNG ekleyin
- `Contents.json` dosyasında filename alanını güncelleyin

### API Bağlantı Hatası
- Production URL'in doğru olduğunu kontrol edin
- Backend sunucunuzun çalıştığından emin olun
- HTTPS kullandığınızdan emin olun (App Transport Security)

### "Invalid Bundle" Hatası
- Bundle Identifier'ın App Store Connect'teki ile eşleştiğini kontrol edin
- Info.plist'in doğru yapılandırıldığından emin olun

---

## 🔒 Gizlilik ve Güvenlik

### App Transport Security (ATS)
- Production'da tüm API çağrıları **HTTPS** üzerinden yapılmalıdır
- `Info.plist`'te yalnızca localhost için HTTP izni verilmiştir (geliştirme amaçlı)

### Veri Gizliliği
- App Store Connect'te "App Privacy" bölümünü doldurun
- Hangi verilerin toplandığını belirtin
- Gizlilik politikası URL'i sağlayın

---

## 📱 Desteklenen Cihazlar

| Ayar | Değer |
|------|-------|
| Minimum iOS | 16.0 |
| Desteklenen Cihazlar | iPhone, iPad |
| Yönelim (iPhone) | Portrait |
| Yönelim (iPad) | Tümü |
| Mimari | arm64 |

---

## 🔄 Güncelleme Yayınlama

1. Kod değişikliklerini yapın
2. `Info.plist`'te **CFBundleShortVersionString** (versiyon) ve **CFBundleVersion** (build numarası) değerlerini artırın
3. Yeni bir Archive oluşturun
4. App Store Connect'e yükleyin
5. Review'a gönderin
