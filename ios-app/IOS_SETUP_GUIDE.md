# 📱 iOS (SwiftUI) Uygulama Başlangıç Rehberi

> **University Match AI - iOS App Development Guide**  
> Bu rehber, iOS uygulamasını kurmak ve backend API ile entegre etmek için adım adım talimatlar içerir.

---

## 🚀 Hızlı Başlangıç

Proje artık hazır bir Xcode projesi içeriyor. Başlamak için:

```bash
cd ios-app
open UniversityMatchAI.xcodeproj
```

> **App Store'a yayınlamak için**: [APP_STORE_GUIDE.md](APP_STORE_GUIDE.md) dosyasını inceleyin.

---

## 📋 İçindekiler

1. [Proje Yapısı](#-proje-yapısı)
2. [Xcode Projesi Açma](#-xcode-projesi-açma)
3. [Dosya Yapısı ve İskelet](#-dosya-yapısı-ve-iskelet)
4. [Backend API Entegrasyonu](#-backend-api-entegrasyonu)
5. [SwiftUI Ekranları](#-swiftui-ekranları)
6. [API İstek Örnekleri](#-api-istek-örnekleri)
7. [Test ve Hata Ayıklama](#-test-ve-hata-ayıklama)

---

## 📁 Proje Yapısı

### Xcode Proje Yapısı

```
ios-app/
├── UniversityMatchAI.xcodeproj/       # Xcode proje dosyası
│   ├── project.pbxproj                # Proje yapılandırması
│   └── xcshareddata/xcschemes/        # Build şemaları
├── UniversityMatchAI/                  # Kaynak kod dizini
│   ├── UniversityMatchAIApp.swift     # @main giriş noktası
│   ├── ContentView.swift              # Ana ekran container
│   ├── InputView.swift                # Kullanıcı giriş formu
│   ├── ResultsView.swift              # Eşleştirme sonuçları ekranı
│   ├── Models.swift                   # Veri modelleri (University, UserProfile, vb.)
│   ├── APIService.swift               # Backend API ile iletişim servisi
│   ├── Info.plist                     # Uygulama yapılandırması
│   ├── Assets.xcassets/               # Görsel kaynaklar ve app ikonu
│   └── Preview Content/               # SwiftUI önizleme kaynakları
├── ExportOptions.plist                # App Store dışa aktarma ayarları
└── APP_STORE_GUIDE.md                 # App Store yayınlama rehberi
```

---

## 🚀 Xcode Projesi Açma

### Adım 1: Projeyi Açın

```bash
cd ios-app
open UniversityMatchAI.xcodeproj
```

### Adım 2: Signing Yapılandırması

1. Xcode'da proje navigator'dan **UniversityMatchAI** projesine tıklayın
2. **Signing & Capabilities** sekmesine gidin
3. **Team** alanından Apple Developer hesabınızı seçin
4. **Automatically manage signing** seçeneğinin işaretli olduğundan emin olun

---

## 📂 Dosya Yapısı ve İskelet

### 1. Models.swift - Veri Modelleri

Backend API'nin beklediği ve döndürdüğü veri formatları:

```swift
import Foundation

// MARK: - User Input Model
struct UserProfile: Codable {
    var gpa: Double
    var gradingSystem: String = "4.0"
    var languageTestType: String
    var languageTestScore: Int
    var background: [String]
    var workExperience: Double = 0
    var researchExperience: Double = 0
    var publications: Int = 0
    var recommendationLetters: Int = 0
    var greScore: Int?
    var gmatScore: Int?
    var undergraduateUniversityRanking: String = ""
    var projectExperience: String = "none"
    var competitionAchievements: String = "none"
    var motivationLetter: String = ""
    var hasMastersDegree: Bool = false
    var mastersUniversityRanking: String = ""
    
    enum CodingKeys: String, CodingKey {
        case gpa
        case gradingSystem = "grading_system"
        case languageTestType = "language_test_type"
        case languageTestScore = "language_test_score"
        case background
        case workExperience = "work_experience"
        case researchExperience = "research_experience"
        case publications
        case recommendationLetters = "recommendation_letters"
        case greScore = "gre_score"
        case gmatScore = "gmat_score"
        case undergraduateUniversityRanking = "undergraduate_university_ranking"
        case projectExperience = "project_experience"
        case competitionAchievements = "competition_achievements"
        case motivationLetter = "motivation_letter"
        case hasMastersDegree = "has_masters_degree"
        case mastersUniversityRanking = "masters_university_ranking"
    }
}

// MARK: - University Model
struct University: Codable, Identifiable, Hashable {
    let id: Int
    let name: String
    let program: String
    let country: String
    let minGPA: Double
    let minLanguageScore: Int
    let requiredBackground: [String]
    var matchScore: Double
    
    enum CodingKeys: String, CodingKey {
        case id, name, program, country
        case minGPA = "min_gpa"
        case minLanguageScore = "min_language_score"
        case requiredBackground = "required_background"
        case matchScore = "match_score"
    }
}

// MARK: - API Response Models
struct MatchResponse: Codable {
    let success: Bool
    let results: MatchResults?
    let userData: [String: Any]?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case success, results, error
        case userData = "user_data"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        success = try container.decode(Bool.self, forKey: .success)
        results = try? container.decode(MatchResults.self, forKey: .results)
        error = try? container.decode(String.self, forKey: .error)
        userData = nil // Optional, şimdilik decode etmiyoruz
    }
}

struct MatchResults: Codable {
    let highMatch: [University]
    let mediumMatch: [University]
    let lowMatch: [University]
    let extraOptions: [University]
    
    enum CodingKeys: String, CodingKey {
        case highMatch = "high_match"
        case mediumMatch = "medium_match"
        case lowMatch = "low_match"
        case extraOptions = "extra_options"
    }
}

// MARK: - Universities Response
struct UniversitiesResponse: Codable {
    let universities: [University]
}

// MARK: - Health Check Response
struct HealthResponse: Codable {
    let status: String
    let message: String
}
```

---

### 2. APIService.swift - Backend API Servisi

Backend ile iletişim kuran servis sınıfı:

```swift
import Foundation

class APIService {
    // MARK: - Configuration
    
    /// Backend API base URL
    /// ⚠️ ÖNEMLI: Simulator için localhost çalışır
    /// Gerçek iPhone için bilgisayarınızın IP adresini kullanın
    static let baseURL = "http://localhost:5000/api"
    
    // Gerçek cihaz için:
    // static let baseURL = "http://192.168.1.100:5000/api" // Bilgisayarınızın IP'si
    
    /// Timeout süresi (saniye)
    static let timeout: TimeInterval = 30
    
    // MARK: - Helper Methods
    
    /// Generic API request helper
    private static func makeRequest<T: Decodable>(
        url: URL,
        method: String = "GET",
        body: [String: Any]? = nil
    ) async throws -> T {
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.timeoutInterval = timeout
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        // Request body ekle (POST için)
        if let body = body {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        }
        
        // Network request
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // HTTP response kontrolü
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            if let errorData = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw APIError.serverError(errorData.error)
            }
            throw APIError.httpError(httpResponse.statusCode)
        }
        
        // JSON decode
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            print("❌ Decode Error: \(error)")
            print("📄 Response: \(String(data: data, encoding: .utf8) ?? "N/A")")
            throw APIError.decodeError
        }
    }
    
    // MARK: - API Endpoints
    
    /// Health check endpoint - API'nin çalışıp çalışmadığını kontrol eder
    static func checkHealth() async throws -> HealthResponse {
        let url = URL(string: "\(baseURL)/health")!
        return try await makeRequest(url: url)
    }
    
    /// Tüm üniversiteleri getir
    static func getUniversities() async throws -> [University] {
        let url = URL(string: "\(baseURL)/universities")!
        let response: UniversitiesResponse = try await makeRequest(url: url)
        return response.universities
    }
    
    /// Kullanıcı profiline göre üniversiteleri eşleştir
    static func matchUniversities(profile: UserProfile) async throws -> MatchResponse {
        let url = URL(string: "\(baseURL)/match")!
        
        // UserProfile'ı backend'in beklediği formata çevir
        var requestBody: [String: Any] = [
            "gpa": profile.gpa,
            "grading_system": profile.gradingSystem,
            "language_test_type": profile.languageTestType,
            "language_test_score": profile.languageTestScore,
            "background": profile.background,
            "work_experience": profile.workExperience,
            "research_experience": profile.researchExperience,
            "publications": profile.publications,
            "recommendation_letters": profile.recommendationLetters,
            "undergraduate_university_ranking": profile.undergraduateUniversityRanking,
            "project_experience": profile.projectExperience,
            "competition_achievements": profile.competitionAchievements,
            "motivation_letter": profile.motivationLetter,
            "has_masters_degree": profile.hasMastersDegree,
            "masters_university_ranking": profile.mastersUniversityRanking
        ]
        
        // Optional alanlar
        if let greScore = profile.greScore {
            requestBody["gre_score"] = greScore
        }
        if let gmatScore = profile.gmatScore {
            requestBody["gmat_score"] = gmatScore
        }
        
        return try await makeRequest(url: url, method: "POST", body: requestBody)
    }
    
    /// CV yükle ve parse et (opsiyonel - ileride eklenebilir)
    static func parseCV(fileData: Data, fileName: String) async throws -> [String: Any] {
        // TODO: Multipart form data ile CV upload
        // Şimdilik backend'de mevcut ama iOS tarafında implement edilmemiş
        throw APIError.notImplemented
    }
}

// MARK: - API Errors

enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case decodeError
    case httpError(Int)
    case serverError(String)
    case networkError(Error)
    case notImplemented
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .decodeError:
            return "Failed to decode response"
        case .httpError(let code):
            return "HTTP Error: \(code)"
        case .serverError(let message):
            return "Server Error: \(message)"
        case .networkError(let error):
            return "Network Error: \(error.localizedDescription)"
        case .notImplemented:
            return "Feature not implemented yet"
        }
    }
}

// MARK: - Error Response Model

struct ErrorResponse: Codable {
    let error: String
    let success: Bool?
}
```

---

### 3. ContentView.swift - Ana Ekran

Ana navigation container:

```swift
import SwiftUI

struct ContentView: View {
    @State private var showResults = false
    @State private var userProfile = UserProfile(
        gpa: 3.5,
        languageTestType: "toefl",
        languageTestScore: 95,
        background: []
    )
    
    var body: some View {
        NavigationView {
            if showResults {
                ResultsView(userProfile: userProfile)
                    .navigationBarTitleDisplayMode(.inline)
            } else {
                InputFormView(profile: $userProfile, onSubmit: {
                    showResults = true
                })
                .navigationBarTitle("University Match AI", displayMode: .large)
            }
        }
        .navigationViewStyle(StackNavigationViewStyle())
    }
}

#Preview {
    ContentView()
}
```

---

## 🔌 Backend API Entegrasyonu

### API Endpoint'leri

Backend'de mevcut endpoint'ler:

| Endpoint | Method | Açıklama | İstek Body | Response |
|----------|--------|----------|------------|----------|
| `/api/health` | GET | API sağlık kontrolü | - | `{"status": "ok", "message": "API is running"}` |
| `/api/universities` | GET | Tüm üniversiteleri listele | - | `{"universities": [...]}` |
| `/api/match` | POST | Üniversiteleri eşleştir | UserProfile | `{"success": true, "results": {...}}` |
| `/api/parse-cv` | POST | CV parse et | Multipart file | `{"success": true, "data": {...}}` |
| `/api/feedback` | POST | Feedback gönder | Feedback data | `{"success": true}` |

### Örnek API İstekleri

#### 1. Health Check

```swift
// Kullanım
do {
    let health = try await APIService.checkHealth()
    print("✅ API Status: \(health.status)")
} catch {
    print("❌ Error: \(error.localizedDescription)")
}
```

#### 2. Üniversiteleri Getir

```swift
// Kullanım
do {
    let universities = try await APIService.getUniversities()
    print("📚 Total Universities: \(universities.count)")
    for uni in universities {
        print("- \(uni.name)")
    }
} catch {
    print("❌ Error: \(error.localizedDescription)")
}
```

#### 3. Üniversite Eşleştirme

```swift
// Kullanım
let profile = UserProfile(
    gpa: 3.8,
    gradingSystem: "4.0",
    languageTestType: "toefl",
    languageTestScore: 110,
    background: ["engineering", "robotics", "control systems"],
    workExperience: 2.0,
    researchExperience: 1.0,
    publications: 2,
    recommendationLetters: 3,
    undergraduateUniversityRanking: "top500",
    projectExperience: "some",
    competitionAchievements: "none",
    motivationLetter: "I am passionate about robotics..."
)

do {
    let response = try await APIService.matchUniversities(profile: profile)
    if response.success, let results = response.results {
        print("🎯 High Match: \(results.highMatch.count) universities")
        print("📊 Medium Match: \(results.mediumMatch.count) universities")
        print("📈 Low Match: \(results.lowMatch.count) universities")
    } else {
        print("❌ Error: \(response.error ?? "Unknown error")")
    }
} catch {
    print("❌ Error: \(error.localizedDescription)")
}
```

---

## 📱 SwiftUI Ekranları

### InputFormView - Kullanıcı Giriş Formu

```swift
import SwiftUI

struct InputFormView: View {
    @Binding var profile: UserProfile
    let onSubmit: () -> Void
    
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    // Background seçenekleri
    let backgroundOptions = [
        "engineering", "robotics", "control systems",
        "computer science", "electrical engineering",
        "mechanical engineering", "software engineering",
        "mathematics", "physics"
    ]
    
    var body: some View {
        Form {
            // GPA Section
            Section(header: Text("Academic Information")) {
                HStack {
                    Text("GPA")
                    Spacer()
                    TextField("3.5", value: $profile.gpa, format: .number.precision(.fractionLength(2)))
                        .keyboardType(.decimalPad)
                        .frame(width: 100)
                }
                
                Picker("Grading System", selection: $profile.gradingSystem) {
                    Text("4.0 Scale").tag("4.0")
                    Text("UK System").tag("uk")
                    Text("Percentage").tag("percentage")
                }
            }
            
            // Language Test Section
            Section(header: Text("Language Test")) {
                Picker("Test Type", selection: $profile.languageTestType) {
                    Text("TOEFL").tag("toefl")
                    Text("IELTS").tag("ielts")
                    Text("PTE").tag("pte")
                    Text("Duolingo").tag("duolingo")
                }
                
                HStack {
                    Text("Score")
                    Spacer()
                    TextField("95", value: $profile.languageTestScore, format: .number)
                        .keyboardType(.numberPad)
                        .frame(width: 100)
                }
            }
            
            // Background Section
            Section(header: Text("Background")) {
                ForEach(backgroundOptions, id: \.self) { option in
                    Toggle(option.capitalized, isOn: Binding(
                        get: { profile.background.contains(option) },
                        set: { isOn in
                            if isOn {
                                profile.background.append(option)
                            } else {
                                profile.background.removeAll { $0 == option }
                            }
                        }
                    ))
                }
            }
            
            // Experience Section
            Section(header: Text("Experience")) {
                HStack {
                    Text("Work Experience (years)")
                    Spacer()
                    TextField("0", value: $profile.workExperience, format: .number.precision(.fractionLength(1)))
                        .keyboardType(.decimalPad)
                        .frame(width: 100)
                }
                
                HStack {
                    Text("Research Experience (years)")
                    Spacer()
                    TextField("0", value: $profile.researchExperience, format: .number.precision(.fractionLength(1)))
                        .keyboardType(.decimalPad)
                        .frame(width: 100)
                }
                
                HStack {
                    Text("Publications")
                    Spacer()
                    TextField("0", value: $profile.publications, format: .number)
                        .keyboardType(.numberPad)
                        .frame(width: 100)
                }
                
                HStack {
                    Text("Recommendation Letters")
                    Spacer()
                    TextField("0", value: $profile.recommendationLetters, format: .number)
                        .keyboardType(.numberPad)
                        .frame(width: 100)
                }
            }
            
            // Submit Button
            Section {
                Button(action: handleSubmit) {
                    HStack {
                        if isLoading {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        } else {
                            Text("Find My Matches")
                                .fontWeight(.semibold)
                        }
                    }
                    .frame(maxWidth: .infinity)
                }
                .disabled(isLoading || !isValidProfile)
                
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                }
            }
        }
    }
    
    private var isValidProfile: Bool {
        profile.gpa > 0 &&
        !profile.languageTestType.isEmpty &&
        profile.languageTestScore > 0 &&
        !profile.background.isEmpty
    }
    
    private func handleSubmit() {
        guard isValidProfile else {
            errorMessage = "Please fill in all required fields"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await APIService.matchUniversities(profile: profile)
                await MainActor.run {
                    isLoading = false
                    if response.success {
                        onSubmit()
                    } else {
                        errorMessage = response.error ?? "Unknown error"
                    }
                }
            } catch {
                await MainActor.run {
                    isLoading = false
                    errorMessage = error.localizedDescription
                }
            }
        }
    }
}
```

---

## 🧪 Test ve Hata Ayıklama

### 1. Backend Bağlantı Sorunları

**Sorun**: "Could not connect to server"

**Çözümler**:
- Backend'in çalıştığından emin olun: `python app.py`
- Simulator için `localhost` kullanın
- Gerçek iPhone için bilgisayarınızın IP adresini kullanın:
  ```swift
  static let baseURL = "http://192.168.1.100:5000/api" // IP'nizi değiştirin
  ```
- Aynı WiFi ağında olduğunuzdan emin olun
- Firewall'un 5000 portunu engellemediğinden emin olun

### 2. CORS Hatası

Backend'de CORS zaten ayarlanmış (`flask-cors`). Eğer hata alırsanız:

```python
# backend/app.py
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### 3. Debug İpuçları

```swift
// API çağrısından önce log ekle
print("🔵 Request URL: \(url)")
print("🔵 Request Body: \(requestBody)")

// Response'u logla
print("🟢 Response Status: \(httpResponse.statusCode)")
print("🟢 Response Data: \(String(data: data, encoding: .utf8) ?? "N/A")")
```

---

## 🎯 Sonraki Adımlar

1. ✅ Temel iskelet hazır
2. ✅ Xcode projesi oluşturuldu
3. ✅ App Store hazırlığı tamamlandı
4. ⏭️ UI/UX iyileştirmeleri
5. ⏭️ CV upload özelliği
6. ⏭️ Offline cache
7. ⏭️ Push notifications

---

## 📚 Kaynaklar

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui/)
- [URLSession Documentation](https://developer.apple.com/documentation/foundation/urlsession)
- [Swift Codable](https://developer.apple.com/documentation/swift/codable)
- Backend API: [README.md](../README.md)

---

**Sorularınız için**: GitHub Issues kullanın veya dokümantasyonu kontrol edin.

