# 📱 iOS Uygulama Geliştirme - Tam Rehber

> **University Match AI iOS App - Complete Development Guide**  
> Tüm iOS geliştirme rehberleri ve örnekler için merkezi kaynak

---

## 🔰 Yeni Başlayanlar İçin

**Xcode'u ilk kez kullanıyorsanız → [XCODE_ADIM_ADIM_REHBER.md](XCODE_ADIM_ADIM_REHBER.md)**

Bu rehber, sıfırdan Xcode kurulumundan App Store'a yüklemeye kadar tüm adımları ekran ekran anlatır.

---

## 📚 Rehber İndeksi

### 1. 🔰 Adım Adım Başlangıç (Yeni!)
- **[XCODE_ADIM_ADIM_REHBER.md](XCODE_ADIM_ADIM_REHBER.md)** - Xcode kurulumu, projeyi açma, signing, test, archive ve App Store'a yükleme

### 2. 🚀 Kurulum ve Yapı
- **[IOS_SETUP_GUIDE.md](IOS_SETUP_GUIDE.md)** - Xcode projesi kurulumu, dosya yapısı, backend entegrasyonu

### 3. 🔌 REST API Entegrasyonu
- **[REST_API_EXAMPLE.md](REST_API_EXAMPLE.md)** - Backend'den veri çekme, POST request, error handling örnekleri

### 4. 🎨 UI/UX
- **[ICON_LAUNCH_SCREEN_GUIDE.md](ICON_LAUNCH_SCREEN_GUIDE.md)** - App icon ve launch screen ekleme rehberi

### 5. 🚀 App Store Yayınlama
- **[APP_STORE_GUIDE.md](APP_STORE_GUIDE.md)** - App Store'a yayınlama detaylı rehber

### 6. 🔀 Git Workflow
- **[../../GIT_WORKFLOW_GUIDE.md](../../GIT_WORKFLOW_GUIDE.md)** - Branch, commit ve push işlemleri

---

## 🗂️ Dosya Yapısı

```
ios-app/
├── UniversityMatchAI.xcodeproj/       # Xcode proje dosyası (bunu açın!)
│   ├── project.pbxproj                # Proje yapılandırması
│   └── xcshareddata/xcschemes/        # Build şemaları
├── UniversityMatchAI/                  # Swift kaynak kodları
│   ├── UniversityMatchAIApp.swift     # @main giriş noktası
│   ├── ContentView.swift              # Ana ekran container
│   ├── InputView.swift                # Kullanıcı giriş formu
│   ├── ResultsView.swift              # Eşleştirme sonuçları ekranı
│   ├── Models.swift                   # Veri modelleri (University, UserProfile, vb.)
│   ├── APIService.swift               # Backend API ile iletişim servisi
│   ├── Info.plist                     # Uygulama yapılandırması
│   ├── Assets.xcassets/               # App icon ve renkler
│   └── Preview Content/               # SwiftUI önizleme kaynakları
├── ExportOptions.plist                # App Store export ayarları
├── XCODE_ADIM_ADIM_REHBER.md         # 🔰 Adım adım Xcode rehberi
├── APP_STORE_GUIDE.md                 # App Store yayınlama rehberi
├── IOS_SETUP_GUIDE.md                 # Kurulum ve API rehberi
├── ICON_LAUNCH_SCREEN_GUIDE.md        # İkon ve launch screen rehberi
├── REST_API_EXAMPLE.md                # API entegrasyon örnekleri
├── README.md                          # Hızlı başlangıç
└── README_IOS_COMPLETE.md             # Bu dosya (indeks)
```

---

## ✅ Tamamlanan Özellikler

### ✅ Xcode Projesi
- [x] `UniversityMatchAI.xcodeproj` — hazır Xcode projesi
- [x] `UniversityMatchAIApp.swift` — `@main` giriş noktası
- [x] `Info.plist` — App Transport Security, versiyon, launch screen
- [x] `Assets.xcassets` — AppIcon ve AccentColor
- [x] `ExportOptions.plist` — App Store export yapılandırması

### ✅ Veri Modelleri
- [x] `UserProfile` — Backend API ile tam uyumlu
- [x] `UserInput` — InputView için basitleştirilmiş model
- [x] `University` — Üniversite modeli
- [x] `MatchResponse` — API response modelleri
- [x] Error handling modelleri

### ✅ API Servisi
- [x] Health check endpoint
- [x] Universities list endpoint
- [x] Match universities endpoint
- [x] Error handling ve debug logging
- [x] Debug/Release URL yapılandırması

### ✅ SwiftUI Ekranları
- [x] `ContentView` — Ana ekran container
- [x] `InputView` — GPA, dil skoru, background, motivasyon mektubu formu
- [x] `ResultsView` — Yüksek/Orta/Düşük eşleşme sonuçları

### ✅ Dokümantasyon
- [x] Adım adım Xcode rehberi (XCODE_ADIM_ADIM_REHBER.md)
- [x] App Store yayınlama rehberi
- [x] Kurulum rehberi
- [x] REST API örnekleri
- [x] Icon/Launch screen rehberi

---

## 🚀 Hızlı Başlangıç

### 1. Projeyi Xcode'da Açın
```bash
cd ios-app
open UniversityMatchAI.xcodeproj
```

### 2. Backend'i Başlatın
```bash
cd backend
pip install -r requirements.txt
python app.py
# Backend http://localhost:5000 adresinde çalışacak
```

### 3. Simulator'da Çalıştırın
- Xcode'da bir iPhone simulator seçin (örn: iPhone 15)
- `⌘ + R` ile çalıştırın

> 🔰 **Detaylı adımlar için:** [XCODE_ADIM_ADIM_REHBER.md](XCODE_ADIM_ADIM_REHBER.md)

---

## 📖 Kullanım Örnekleri

### Üniversiteleri Listeleme

```swift
@StateObject var viewModel = UniversitiesViewModel()

Task {
    await viewModel.fetchUniversities()
}
```

### Match Universities

```swift
let profile = UserProfile(
    gpa: 3.8,
    languageTestType: "toefl",
    languageTestScore: 110,
    background: ["engineering", "robotics"]
)

let response = try await APIService.matchUniversities(profile: profile)
```

### Login Form

```swift
@StateObject var viewModel = LoginViewModel()

Task {
    await viewModel.login()
}
```

**Detaylı örnekler için:** [REST_API_EXAMPLE.md](REST_API_EXAMPLE.md)

---

## 🔗 Backend API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/health` | GET | API sağlık kontrolü |
| `/api/universities` | GET | Tüm üniversiteleri listele |
| `/api/match` | POST | Üniversiteleri eşleştir |
| `/api/parse-cv` | POST | CV parse et (opsiyonel) |
| `/api/feedback` | POST | Feedback gönder (opsiyonel) |

**API dokümantasyonu için:** [../../README.md](../../README.md)

---

## 📱 Geliştirme Checklist

### Temel Kurulum
- [x] Xcode projesi oluşturuldu
- [x] Swift dosyaları eklendi
- [ ] Backend çalışıyor
- [x] API URL doğru ayarlandı (Debug/Release)

### UI/UX
- [ ] App icon eklendi (1024x1024 PNG)
- [ ] Launch screen özelleştirildi (opsiyonel)
- [x] Temel navigation yapıldı
- [x] Loading state'leri gösteriliyor
- [x] Error handling çalışıyor

### API Entegrasyonu
- [x] Health check çalışıyor
- [x] Universities list görüntüleniyor
- [x] Match universities çalışıyor
- [x] Error messages gösteriliyor

### Test
- [ ] Simulator'da test edildi
- [ ] Gerçek cihazda test edildi

### App Store
- [ ] Apple Developer Program üyeliği alındı
- [ ] Signing yapılandırıldı
- [ ] Archive oluşturuldu
- [ ] App Store Connect'e yüklendi
- [ ] Review'a gönderildi

---

## 🐛 Yaygın Sorunlar

### Backend Bağlantı Hatası
**Sorun:** "Could not connect to server"  
**Çözüm:** 
- Backend'in çalıştığından emin olun
- Gerçek iPhone için IP adresini kullanın
- Aynı WiFi ağında olduğunuzdan emin olun

### CORS Hatası
**Sorun:** "CORS policy error"  
**Çözüm:** Backend'de CORS zaten ayarlanmış (`flask-cors`)

### Icon Görünmüyor
**Sorun:** App icon gösterilmiyor  
**Çözüm:** 
- Assets.xcassets > AppIcon'a eklendiğinden emin olun
- Build > Clean Build Folder yapın

**Detaylı sorun giderme:** [ICON_LAUNCH_SCREEN_GUIDE.md](ICON_LAUNCH_SCREEN_GUIDE.md)

---

## 🔄 Git Workflow

### Yeni Özellik Ekleme

```bash
# 1. Branch oluştur
git checkout -b feature/ios-new-feature

# 2. Değişiklikleri yap

# 3. Commit et
git add .
git commit -m "feat: Add new feature"

# 4. Push et
git push -u origin feature/ios-new-feature
```

**Detaylı rehber:** [../../GIT_WORKFLOW_GUIDE.md](../../GIT_WORKFLOW_GUIDE.md)

---

## 📚 Ek Kaynaklar

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui/)
- [URLSession Guide](https://developer.apple.com/documentation/foundation/urlsession)
- [Apple HIG - App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Backend API Docs](../../README.md)

---

## 🤝 Katkıda Bulunma

Yeni özellik veya iyileştirme önerileri için:
1. Yeni branch oluşturun
2. Değişikliklerinizi yapın
3. Pull Request açın

---

## 📝 Notlar

- **Backend URL**: Debug'da `localhost:5000`, Release'de production URL otomatik kullanılır
- **iOS Version**: Minimum iOS 16.0 (SwiftUI)
- **Xcode Version**: Xcode 15+ önerilir
- **Swift Version**: 5.0

---

**Son Güncelleme:** Şubat 2026  
**Versiyon:** 2.0

