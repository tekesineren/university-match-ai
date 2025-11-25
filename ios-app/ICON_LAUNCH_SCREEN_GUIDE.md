# 🎨 iOS Icon ve Launch Screen Rehberi

> **University Match AI - App Icon & Launch Screen Setup**  
> Xcode'da icon ve launch screen ekleme adım adım rehberi

---

## 📋 İçindekiler

1. [App Icon Ekleme](#-app-icon-ekleme)
2. [Launch Screen Oluşturma](#-launch-screen-oluşturma)
3. [Resim Gereklilikleri](#-resim-gereklilikleri)
4. [Xcode Ayarları](#-xcode-ayarları)
5. [Hızlı Başlangıç](#-hızlı-başlangıç)

---

## 🖼️ App Icon Ekleme

### Adım 1: Icon Resimlerini Hazırlama

iOS uygulaması için farklı boyutlarda icon'lar gerekir:

| Boyut | Kullanım | Gereklilik |
|-------|----------|------------|
| **1024x1024** | App Store | ✅ Zorunlu |
| **180x180** | iPhone App Icon (@3x) | ✅ Zorunlu |
| **120x120** | iPhone App Icon (@2x) | ✅ Zorunlu |
| **87x87** | iPhone Settings (@3x) | ⚠️ Önerilen |
| **58x58** | iPhone Settings (@2x) | ⚠️ Önerilen |
| **80x80** | iPhone Spotlight (@2x) | ⚠️ Önerilen |
| **120x120** | iPhone Spotlight (@3x) | ⚠️ Önerilen |

**📌 Önemli Notlar:**
- Tüm icon'lar **PNG formatında** olmalı (transparan arka plan yok)
- Icon'lar **square** (kare) olmalı, yuvarlak köşeler Xcode tarafından otomatik eklenir
- Background color kullanmalısınız (transparan olamaz)

### Adım 2: Icon Set Oluşturma

**Yöntem 1: Xcode Asset Catalog (Önerilen)**

1. Xcode'da projenizi açın
2. **Navigator** panelinde `Assets.xcassets` dosyasını bulun
3. **AppIcon** asset'ini seçin (yoksa oluşturun)
4. Gerekli boyutlardaki icon'ları sürükleyip bırakın

**Yöntem 2: Online Icon Generator Kullanım**

Ücretsiz online araçlar:
- [AppIcon.co](https://www.appicon.co/)
- [Icon Generator](https://icon.kitchen/)
- [MakeAppIcon](https://makeappicon.com/)

Bu araçlar tek bir 1024x1024 icon'dan tüm boyutları otomatik oluşturur.

### Adım 3: Xcode'da Icon Ayarlama

#### 3.1 Assets.xcassets ile

1. **Xcode'da Assets.xcassets açın**
2. **AppIcon** seçin (sol panelde)
3. Sağ panelde gerekli slot'lara icon'ları sürükleyip bırakın:

```
AppIcon
├── iPhone Notification (@2x) - 40x40 (iOS 7-15)
├── iPhone Notification (@3x) - 60x60 (iOS 7-15)
├── iPhone Settings (@2x) - 58x58 (iOS 7-15)
├── iPhone Settings (@3x) - 87x87 (iOS 7-15)
├── iPhone Spotlight (@2x) - 80x80 (iOS 7-15)
├── iPhone Spotlight (@3x) - 120x120 (iOS 7-15)
├── iPhone App (@2x) - 120x120 (iOS 7-15)
├── iPhone App (@3x) - 180x180 (iOS 7-15)
└── App Store - 1024x1024 (zorunlu)
```

#### 3.2 info.plist ile (Eski Yöntem)

```xml
<key>CFBundleIcons</key>
<dict>
    <key>CFBundlePrimaryIcon</key>
    <dict>
        <key>CFBundleIconFiles</key>
        <array>
            <string>AppIcon-60@2x</string>
            <string>AppIcon-60@3x</string>
        </array>
    </dict>
</dict>
```

### Adım 4: Icon Tasarım İpuçları

✅ **DO:**
- Basit ve tanınabilir tasarım kullan
- Yüksek kontrast renkler
- Merkezi yerleşim (kenarlarda önemli detaylar olmasın)
- 1024x1024'ten küçültülmüş versiyonlar net görünmeli

❌ **DON'T:**
- Metin kullanma (küçük boyutlarda okunamaz)
- Çok fazla detay ekleme
- Transparan arka plan
- Kare köşeler için özel şekil (Xcode otomatik yapar)

---

## 🚀 Launch Screen Oluşturma

Launch Screen, uygulama açılırken gösterilen ilk ekrandır.

### Yöntem 1: Storyboard ile (Önerilen)

#### Adım 1: LaunchScreen.storyboard Oluşturma

1. **Xcode'da File > New > File** seçin
2. **iOS > User Interface > Storyboard** seçin
3. Dosya adı: `LaunchScreen`
4. **Target Membership**: Projenizi seçin

#### Adım 2: Storyboard Tasarımı

**LaunchScreen.storyboard içeriği:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<document type="com.apple.InterfaceBuilder3.CocoaTouch.Storyboard.XIB" version="3.0" toolsVersion="21701" targetRuntime="iOS.CocoaTouch" propertyAccessControl="none" useAutolayout="YES" launchScreen="YES" useTraitCollections="YES" useSafeAreas="YES" colorMatched="YES" initialViewController="01J-lp-oVM">
    <device id="retina6_1" orientation="portrait" appearance="light"/>
    <dependencies>
        <plugIn identifier="com.apple.InterfaceBuilder.IBCocoaTouchPlugin" version="21679"/>
    </dependencies>
    <scenes>
        <scene sceneID="EHf-IW-A2E">
            <objects>
                <viewController id="01J-lp-oVM" sceneMemberID="viewController">
                    <view key="view" contentMode="scaleToFill" id="Ze5-6b-2t3">
                        <rect key="frame" x="0.0" y="0.0" width="414" height="896"/>
                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
                        <subviews>
                            <!-- Logo Image -->
                            <imageView clipsSubviews="YES" userInteractionEnabled="NO" contentMode="scaleAspectFit" horizontalHuggingPriority="251" verticalHuggingPriority="251" image="AppIcon" translatesAutoresizingMaskIntoConstraints="NO" id="logo-image">
                                <rect key="frame" x="157" y="398" width="100" height="100"/>
                                <constraints>
                                    <constraint firstAttribute="width" constant="100" id="logo-width"/>
                                    <constraint firstAttribute="height" constant="100" id="logo-height"/>
                                </constraints>
                            </imageView>
                            
                            <!-- App Name Label -->
                            <label opaque="NO" userInteractionEnabled="NO" contentMode="left" horizontalHuggingPriority="251" verticalHuggingPriority="251" text="University Match AI" textAlignment="center" lineBreakMode="tailTruncation" baselineAdjustment="alignBaselines" adjustsFontSizeToFit="NO" translatesAutoresizingMaskIntoConstraints="NO" id="app-name">
                                <rect key="frame" x="50" y="518" width="314" height="36"/>
                                <fontDescription key="fontDescription" type="system" weight="semibold" pointSize="30"/>
                                <color key="textColor" systemColor="labelColor"/>
                                <nil key="highlightedColor"/>
                            </label>
                            
                            <!-- Subtitle Label -->
                            <label opaque="NO" userInteractionEnabled="NO" contentMode="left" horizontalHuggingPriority="251" verticalHuggingPriority="251" text="Find Your Perfect University Match" textAlignment="center" lineBreakMode="tailTruncation" baselineAdjustment="alignBaselines" adjustsFontSizeToFit="NO" translatesAutoresizingMaskIntoConstraints="NO" id="subtitle">
                                <rect key="frame" x="50" y="564" width="314" height="21"/>
                                <fontDescription key="fontDescription" type="system" pointSize="17"/>
                                <color key="textColor" systemColor="secondaryLabelColor"/>
                                <nil key="highlightedColor"/>
                            </label>
                        </subviews>
                        <viewLayoutGuide key="safeArea" id="6Tk-OE-BBY"/>
                        <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                        <constraints>
                            <!-- Logo Constraints -->
                            <constraint firstItem="logo-image" firstAttribute="centerX" secondItem="Ze5-6b-2t3" secondAttribute="centerX" id="logo-centerX"/>
                            <constraint firstItem="logo-image" firstAttribute="centerY" secondItem="Ze5-6b-2t3" secondAttribute="centerY" id="logo-centerY"/>
                            
                            <!-- App Name Constraints -->
                            <constraint firstItem="app-name" firstAttribute="top" secondItem="logo-image" secondAttribute="bottom" constant="20" id="name-top"/>
                            <constraint firstItem="app-name" firstAttribute="leading" secondItem="6Tk-OE-BBY" secondAttribute="leading" constant="50" id="name-leading"/>
                            <constraint firstItem="6Tk-OE-BBY" firstAttribute="trailing" secondItem="app-name" secondAttribute="trailing" constant="50" id="name-trailing"/>
                            
                            <!-- Subtitle Constraints -->
                            <constraint firstItem="subtitle" firstAttribute="top" secondItem="app-name" secondAttribute="bottom" constant="10" id="subtitle-top"/>
                            <constraint firstItem="subtitle" firstAttribute="leading" secondItem="6Tk-OE-BBY" secondAttribute="leading" constant="50" id="subtitle-leading"/>
                            <constraint firstItem="6Tk-OE-BBY" firstAttribute="trailing" secondItem="subtitle" secondAttribute="trailing" constant="50" id="subtitle-trailing"/>
                        </constraints>
                    </view>
                </viewController>
                <placeholder placeholderIdentifier="IBFirstResponder" id="iYj-Kq-Ea1" userLabel="First Responder" sceneMemberID="firstResponder"/>
            </objects>
            <point key="canvasLocation" x="53" y="375"/>
        </scene>
    </scenes>
    <resources>
        <image name="AppIcon" width="1024" height="1024"/>
        <systemColor name="labelColor">
            <color white="0.0" alpha="1" colorSpace="custom" customColorSpace="genericGamma22GrayColorSpace"/>
        </systemColor>
        <systemColor name="secondaryLabelColor">
            <color white="0.40000000000000002" alpha="1" colorSpace="custom" customColorSpace="genericGamma22GrayColorSpace"/>
        </systemColor>
        <systemColor name="systemBackgroundColor">
            <color white="1" alpha="1" colorSpace="custom" customColorSpace="genericGamma22GrayColorSpace"/>
        </systemColor>
    </resources>
</document>
```

#### Adım 3: info.plist Ayarları

`Info.plist` dosyasında launch screen'i belirtin:

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>
```

**Veya** Xcode'da:
1. **Project Navigator** > `Info.plist` açın
2. **Custom iOS Target Properties** bölümüne gidin
3. `Launch Screen` key'ini ekleyin ve değer olarak `LaunchScreen` yazın

### Yöntem 2: SwiftUI ile (iOS 14+)

iOS 14+ için SwiftUI ile launch screen oluşturabilirsiniz:

#### Adım 1: LaunchScreenView.swift Oluşturun

```swift
import SwiftUI

struct LaunchScreenView: View {
    @State private var isActive = false
    
    var body: some View {
        ZStack {
            // Background
            Color(red: 0.40, green: 0.47, blue: 0.92) // Purple gradient start
                .ignoresSafeArea()
            
            VStack(spacing: 20) {
                // Logo
                Image(systemName: "graduationcap.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.white)
                
                // App Name
                Text("University Match AI")
                    .font(.system(size: 32, weight: .bold))
                    .foregroundColor(.white)
                
                // Subtitle
                Text("Find Your Perfect University Match")
                    .font(.system(size: 18, weight: .medium))
                    .foregroundColor(.white.opacity(0.9))
            }
        }
        .onAppear {
            // 2 saniye sonra ana ekrana geç
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                withAnimation {
                    isActive = true
                }
            }
        }
        .fullScreenCover(isPresented: $isActive) {
            ContentView()
        }
    }
}

#Preview {
    LaunchScreenView()
}
```

#### Adım 2: App Entry Point

```swift
@main
struct UniversityMatchAIApp: App {
    var body: some Scene {
        WindowGroup {
            LaunchScreenView() // İlk açılışta launch screen göster
        }
    }
}
```

### Yöntem 3: XIB Dosyası (Eski Yöntem)

1. **File > New > File**
2. **iOS > User Interface > View** seçin
3. Dosya adı: `LaunchScreen.xib`
4. Tasarımınızı yapın
5. `Info.plist`'e ekleyin

---

## 📐 Resim Gereklilikleri

### App Icon Boyutları (Tam Liste)

| Platform | Boyut | Dosya Adı Örneği | Ölçek |
|----------|-------|------------------|-------|
| **App Store** | 1024x1024 | AppIcon-1024.png | 1x |
| **iPhone** | 180x180 | AppIcon-60@3x.png | 3x |
| **iPhone** | 120x120 | AppIcon-60@2x.png | 2x |
| **iPhone Settings** | 87x87 | AppIcon-29@3x.png | 3x |
| **iPhone Settings** | 58x58 | AppIcon-29@2x.png | 2x |
| **iPhone Spotlight** | 120x120 | AppIcon-40@3x.png | 3x |
| **iPhone Spotlight** | 80x80 | AppIcon-40@2x.png | 2x |
| **iPhone Notification** | 60x60 | AppIcon-20@3x.png | 3x |
| **iPhone Notification** | 40x40 | AppIcon-20@2x.png | 2x |

### Launch Screen Gereksinimleri

- **Format**: PNG veya Storyboard
- **Boyut**: Tam ekran (iPhone/iPad için farklı)
- **Orientasyon**: Portrait ve Landscape desteği
- **Dark Mode**: iOS 13+ için dark mode desteği önerilir

---

## ⚙️ Xcode Ayarları

### Adım 1: Project Settings

1. **Xcode'da projenizi seçin** (sol üstte)
2. **TARGETS > YourApp** seçin
3. **General** sekmesine gidin

### Adım 2: App Icons Source

1. **App Icons and Launch Screen** bölümüne gidin
2. **App Icons Source**: `AppIcon` seçin (Assets.xcassets'den)
3. **Launch Screen**: `LaunchScreen` storyboard seçin

### Adım 3: Asset Catalog Kontrolü

1. **Assets.xcassets** açın
2. **AppIcon** asset'ini kontrol edin
3. Tüm slot'ların dolu olduğundan emin olun

### Adım 4: Build Settings Kontrolü

1. **Build Settings** sekmesine gidin
2. **Asset Catalog Compiler** ayarlarını kontrol edin:
   - `ASSETCATALOG_COMPILER_APPICON_NAME`: `AppIcon`
   - `ASSETCATALOG_COMPILER_LAUNCHIMAGE_NAME`: (boş bırakın, storyboard kullanıyorsanız)

---

## 🚀 Hızlı Başlangıç (5 Dakika)

### En Hızlı Yol: Online Generator

1. **1024x1024 icon hazırlayın**
2. [AppIcon.co](https://www.appicon.co/) veya benzeri siteye gidin
3. Icon'unuzu yükleyin
4. Tüm boyutları indirin
5. Xcode'da Assets.xcassets > AppIcon'a sürükleyip bırakın
6. ✅ Tamamlandı!

### Launch Screen (2 Dakika)

1. Xcode'da **File > New > File > Storyboard**
2. Adı: `LaunchScreen.storyboard`
3. Basit bir view ekleyin (logo + app name)
4. `Info.plist`'e `UILaunchStoryboardName: LaunchScreen` ekleyin
5. ✅ Tamamlandı!

---

## ✅ Kontrol Listesi

- [ ] 1024x1024 App Store icon hazır
- [ ] Tüm iPhone icon boyutları hazır
- [ ] Assets.xcassets > AppIcon'a icon'lar eklendi
- [ ] LaunchScreen.storyboard oluşturuldu
- [ ] Info.plist'te launch screen ayarlandı
- [ ] Simulator'da test edildi
- [ ] Gerçek cihazda test edildi

---

## 🐛 Yaygın Sorunlar ve Çözümleri

### Sorun 1: Icon Görünmüyor

**Çözüm:**
- Icon'ların Assets.xcassets > AppIcon'a eklendiğinden emin olun
- Build > Clean Build Folder yapın
- Cihazı/simulator'ı yeniden başlatın

### Sorun 2: Launch Screen Gösterilmiyor

**Çözüm:**
- Info.plist'te `UILaunchStoryboardName` key'inin olduğunu kontrol edin
- Storyboard dosyasının target membership'inde olduğunu kontrol edin
- Build Settings'te launch screen source'unun doğru olduğunu kontrol edin

### Sorun 3: Icon Köşeleri Kesik Görünüyor

**Çözüm:**
- Icon'unuzda yuvarlak köşeler olmamalı, Xcode otomatik ekler
- Önemli içerik merkeze yerleştirin (kenarlarda detay olmasın)

---

## 📚 Ekstra Kaynaklar

- [Apple Human Interface Guidelines - App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [Apple Human Interface Guidelines - Launch Screen](https://developer.apple.com/design/human-interface-guidelines/launch-screen)
- [AppIcon.co - Online Icon Generator](https://www.appicon.co/)
- [Icon Generator - Free Tool](https://icon.kitchen/)

---

**Sonraki Adım**: Icon ve launch screen hazır olduktan sonra, Git workflow rehberine geçebiliriz! 🎉

