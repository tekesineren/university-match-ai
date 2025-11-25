# 📱 iOS Uygulama Geliştirme - Tam Rehber

> **University Match AI iOS App - Complete Development Guide**  
> Tüm iOS geliştirme rehberleri ve örnekler için merkezi kaynak

---

## 📚 Rehber İndeksi

### 1. 🚀 Başlangıç ve Kurulum
- **[IOS_SETUP_GUIDE.md](IOS_SETUP_GUIDE.md)** - Xcode projesi kurulumu, dosya yapısı, backend entegrasyonu

### 2. 🔌 REST API Entegrasyonu
- **[REST_API_EXAMPLE.md](REST_API_EXAMPLE.md)** - Backend'den veri çekme, POST request, error handling örnekleri

### 3. 🎨 UI/UX
- **[ICON_LAUNCH_SCREEN_GUIDE.md](ICON_LAUNCH_SCREEN_GUIDE.md)** - App icon ve launch screen ekleme rehberi

### 4. 🔀 Git Workflow
- **[../../GIT_WORKFLOW_GUIDE.md](../../GIT_WORKFLOW_GUIDE.md)** - Branch, commit ve push işlemleri

---

## 🗂️ Dosya Yapısı

```
ios-app/
├── Models.swift                    ✅ Backend API ile uyumlu veri modelleri
├── APIService.swift                ✅ REST API servisi (tüm endpoint'ler)
├── ContentView.swift               ✅ Ana navigation container
├── InputView.swift                 ⚠️ Eski versiyon (güncelleme gerekebilir)
├── ResultsView.swift               ⚠️ Eski versiyon (güncelleme gerekebilir)
│
├── README.md                       📖 Temel iOS app açıklaması
├── IOS_SETUP_GUIDE.md             📖 Kurulum ve yapı rehberi
├── REST_API_EXAMPLE.md            📖 API entegrasyon örnekleri
├── ICON_LAUNCH_SCREEN_GUIDE.md    📖 Icon/Launch screen setup
└── README_IOS_COMPLETE.md         📖 Bu dosya (indeks)
```

---

## ✅ Tamamlanan Özellikler

### ✅ Veri Modelleri
- [x] `UserProfile` - Backend API ile tam uyumlu
- [x] `University` - Üniversite modeli
- [x] `MatchResponse` - API response modelleri
- [x] Error handling modelleri

### ✅ API Servisi
- [x] Health check endpoint
- [x] Universities list endpoint
- [x] Match universities endpoint
- [x] Error handling ve retry mekanizması
- [x] Debug logging

### ✅ Dokümantasyon
- [x] Kurulum rehberi
- [x] REST API örnekleri
- [x] Login form örneği
- [x] Icon/Launch screen rehberi
- [x] Git workflow rehberi

---

## 🚀 Hızlı Başlangıç

### 1. Xcode Projesi Oluştur
```bash
# Xcode'da yeni iOS App projesi oluştur
# Interface: SwiftUI
# Language: Swift
```

### 2. Dosyaları Ekle
```bash
# ios-app/ klasöründeki Swift dosyalarını Xcode'a ekle:
# - Models.swift
# - APIService.swift
# - ContentView.swift
```

### 3. Backend'i Başlat
```bash
cd backend
python app.py
# Backend http://localhost:5000 adresinde çalışacak
```

### 4. API URL'ini Ayarla
```swift
// APIService.swift içinde:
static let baseURL = "http://localhost:5000/api"
// Gerçek iPhone için: "http://[BILGISAYAR_IP]:5000/api"
```

### 5. Test Et
```swift
// ContentView içinde:
Task {
    let universities = try await APIService.getUniversities()
    print("✅ Universities loaded: \(universities.count)")
}
```

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
- [ ] Xcode projesi oluşturuldu
- [ ] Swift dosyaları eklendi
- [ ] Backend çalışıyor
- [ ] API URL doğru ayarlandı

### UI/UX
- [ ] App icon eklendi
- [ ] Launch screen oluşturuldu
- [ ] Temel navigation yapıldı
- [ ] Loading state'leri gösteriliyor
- [ ] Error handling çalışıyor

### API Entegrasyonu
- [ ] Health check çalışıyor
- [ ] Universities list görüntüleniyor
- [ ] Match universities çalışıyor
- [ ] Error messages gösteriliyor

### Test
- [ ] Simulator'da test edildi
- [ ] Gerçek cihazda test edildi
- [ ] Farklı network durumları test edildi

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

- **Backend URL**: Development için `localhost:5000`, production için backend URL'i güncelleyin
- **iOS Version**: Minimum iOS 14.0 (SwiftUI için)
- **Xcode Version**: Xcode 14+ önerilir

---

**Son Güncelleme:** Kasım 2024  
**Versiyon:** 1.0

