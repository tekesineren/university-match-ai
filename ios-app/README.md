# 📱 University Match AI — iOS App

Master's başvuruları için AI destekli üniversite eşleştirme uygulamasının **native iOS (SwiftUI)** versiyonu.

## 🚀 Hızlı Başlangıç

```bash
cd ios-app
open UniversityMatchAI.xcodeproj
```

Xcode açıldıktan sonra `⌘ + R` ile Simulator'da çalıştırabilirsiniz.

> ⚠️ Backend API'nin çalıştığından emin olun: `cd backend && python app.py`

## 📖 Rehberler

| Rehber | Açıklama |
|--------|----------|
| **[XCODE_ADIM_ADIM_REHBER.md](XCODE_ADIM_ADIM_REHBER.md)** | 🔰 Sıfırdan Xcode kurulumu, projeyi açma ve App Store'a kadar her adım |
| [APP_STORE_GUIDE.md](APP_STORE_GUIDE.md) | App Store'a yayınlama detaylı rehber |
| [IOS_SETUP_GUIDE.md](IOS_SETUP_GUIDE.md) | Proje yapısı ve API entegrasyonu |
| [ICON_LAUNCH_SCREEN_GUIDE.md](ICON_LAUNCH_SCREEN_GUIDE.md) | App icon ve launch screen ekleme |
| [REST_API_EXAMPLE.md](REST_API_EXAMPLE.md) | Backend REST API kullanım örnekleri |

## 📁 Proje Yapısı

```
ios-app/
├── UniversityMatchAI.xcodeproj/       # Xcode proje dosyası
├── UniversityMatchAI/                  # Swift kaynak kodları
│   ├── UniversityMatchAIApp.swift     # @main giriş noktası
│   ├── ContentView.swift              # Ana ekran
│   ├── InputView.swift                # Kullanıcı giriş formu
│   ├── ResultsView.swift              # Eşleşme sonuçları
│   ├── Models.swift                   # Veri modelleri
│   ├── APIService.swift               # Backend API servisi
│   ├── Info.plist                     # Uygulama yapılandırması
│   ├── Assets.xcassets/               # App icon ve renkler
│   └── Preview Content/               # SwiftUI önizleme kaynakları
└── ExportOptions.plist                # App Store export ayarları
```

## 📱 Gereksinimler

| Gereksinim | Değer |
|------------|-------|
| macOS | 13 Ventura+ |
| Xcode | 15.0+ |
| iOS Deployment Target | 16.0 |
| Swift | 5.0 |
| Backend | Python 3.8+ (Flask) |

