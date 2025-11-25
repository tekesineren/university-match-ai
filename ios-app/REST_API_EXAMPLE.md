# 📱 SwiftUI REST API Örnekleri

> Backend API'ye REST istekleri atmak ve response'ları listelemek için SwiftUI örnek kodları

---

## 1️⃣ Backend'den Veri Çekme ve Liste Gösterme

### Örnek: Üniversiteleri Listeleme

```swift
import SwiftUI

// MARK: - View Model
@MainActor
class UniversitiesViewModel: ObservableObject {
    @Published var universities: [University] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func fetchUniversities() async {
        isLoading = true
        errorMessage = nil
        
        do {
            let fetchedUniversities = try await APIService.getUniversities()
            universities = fetchedUniversities
            isLoading = false
        } catch {
            errorMessage = (error as? APIError)?.userFriendlyMessage ?? error.localizedDescription
            isLoading = false
            print("❌ Error fetching universities: \(error)")
        }
    }
}

// MARK: - SwiftUI View
struct UniversitiesListView: View {
    @StateObject private var viewModel = UniversitiesViewModel()
    
    var body: some View {
        NavigationView {
            ZStack {
                // Content
                if viewModel.isLoading {
                    ProgressView("Loading universities...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if let error = viewModel.errorMessage {
                    ErrorView(message: error, onRetry: {
                        Task {
                            await viewModel.fetchUniversities()
                        }
                    })
                } else {
                    List(viewModel.universities) { university in
                        UniversityRow(university: university)
                    }
                    .refreshable {
                        await viewModel.fetchUniversities()
                    }
                }
            }
            .navigationTitle("Universities")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Refresh") {
                        Task {
                            await viewModel.fetchUniversities()
                        }
                    }
                }
            }
            .task {
                // View göründüğünde otomatik yükle
                await viewModel.fetchUniversities()
            }
        }
    }
}

// MARK: - University Row Component
struct UniversityRow: View {
    let university: University
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(university.name)
                    .font(.headline)
                Spacer()
                Text(university.country)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Text(university.program)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            HStack {
                Label("Min GPA: \(university.minGPA, specifier: "%.2f")", systemImage: "star.fill")
                    .font(.caption)
                Spacer()
                Label("Min Language: \(university.minLanguageScore)", systemImage: "globe")
                    .font(.caption)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Error View Component
struct ErrorView: View {
    let message: String
    let onRetry: () -> Void
    
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle.fill")
                .font(.system(size: 50))
                .foregroundColor(.orange)
            
            Text("Error")
                .font(.title2)
                .fontWeight(.semibold)
            
            Text(message)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
            
            Button(action: onRetry) {
                HStack {
                    Image(systemName: "arrow.clockwise")
                    Text("Retry")
                }
                .padding(.horizontal, 20)
                .padding(.vertical, 10)
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Preview
#Preview {
    UniversitiesListView()
}
```

### Kullanım Örneği

```swift
// Ana app'te kullanım
@main
struct UniversityMatchAIApp: App {
    var body: some Scene {
        WindowGroup {
            UniversitiesListView()
        }
    }
}
```

---

## 2️⃣ POST Request: Match Universities

### View Model ile State Yönetimi

```swift
import SwiftUI

// MARK: - Match View Model
@MainActor
class MatchViewModel: ObservableObject {
    @Published var results: MatchResults?
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var userProfile = UserProfile(
        gpa: 3.5,
        languageTestType: "toefl",
        languageTestScore: 95,
        background: []
    )
    
    func findMatches() async {
        guard userProfile.isValid else {
            errorMessage = "Please fill in all required fields"
            return
        }
        
        isLoading = true
        errorMessage = nil
        results = nil
        
        do {
            let response = try await APIService.matchUniversities(profile: userProfile)
            
            if response.success, let matchResults = response.results {
                results = matchResults
                isLoading = false
            } else {
                errorMessage = response.error ?? "Unknown error occurred"
                isLoading = false
            }
        } catch {
            errorMessage = (error as? APIError)?.userFriendlyMessage ?? error.localizedDescription
            isLoading = false
        }
    }
    
    func reset() {
        results = nil
        errorMessage = nil
    }
}

// MARK: - Match Results View
struct MatchResultsView: View {
    @StateObject private var viewModel = MatchViewModel()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Input Form
                    InputFormSection(profile: $viewModel.userProfile)
                    
                    // Submit Button
                    Button(action: {
                        Task {
                            await viewModel.findMatches()
                        }
                    }) {
                        HStack {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            } else {
                                Image(systemName: "magnifyingglass")
                                Text("Find Matches")
                                    .fontWeight(.semibold)
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.userProfile.isValid && !viewModel.isLoading ? Color.blue : Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                    .disabled(!viewModel.userProfile.isValid || viewModel.isLoading)
                    .padding(.horizontal)
                    
                    // Error Message
                    if let error = viewModel.errorMessage {
                        HStack {
                            Image(systemName: "exclamationmark.circle.fill")
                                .foregroundColor(.red)
                            Text(error)
                                .font(.caption)
                                .foregroundColor(.red)
                            Spacer()
                        }
                        .padding(.horizontal)
                    }
                    
                    // Results
                    if let results = viewModel.results {
                        ResultsSection(results: results)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("University Matcher")
        }
    }
}

// MARK: - Input Form Section
struct InputFormSection: View {
    @Binding var profile: UserProfile
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Your Profile")
                .font(.headline)
            
            // GPA
            HStack {
                Text("GPA:")
                    .frame(width: 120, alignment: .leading)
                TextField("3.5", value: $profile.gpa, format: .number.precision(.fractionLength(2)))
                    .keyboardType(.decimalPad)
                    .textFieldStyle(.roundedBorder)
            }
            
            // Language Test
            HStack {
                Text("Language Test:")
                    .frame(width: 120, alignment: .leading)
                Picker("", selection: $profile.languageTestType) {
                    Text("TOEFL").tag("toefl")
                    Text("IELTS").tag("ielts")
                    Text("PTE").tag("pte")
                }
                .pickerStyle(.menu)
                .frame(maxWidth: .infinity)
            }
            
            // Language Score
            HStack {
                Text("Score:")
                    .frame(width: 120, alignment: .leading)
                TextField("95", value: $profile.languageTestScore, format: .number)
                    .keyboardType(.numberPad)
                    .textFieldStyle(.roundedBorder)
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
        .padding(.horizontal)
    }
}

// MARK: - Results Section
struct ResultsSection: View {
    let results: MatchResults
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Match Results")
                .font(.headline)
                .padding(.horizontal)
            
            // High Match
            if !results.highMatch.isEmpty {
                MatchCategoryView(
                    title: "High Match",
                    universities: results.highMatch,
                    color: .green
                )
            }
            
            // Medium Match
            if !results.mediumMatch.isEmpty {
                MatchCategoryView(
                    title: "Medium Match",
                    universities: results.mediumMatch,
                    color: .orange
                )
            }
            
            // Low Match
            if !results.lowMatch.isEmpty {
                MatchCategoryView(
                    title: "Low Match",
                    universities: results.lowMatch,
                    color: .yellow
                )
            }
        }
    }
}

// MARK: - Match Category View
struct MatchCategoryView: View {
    let title: String
    let universities: [University]
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(title)
                    .font(.headline)
                    .foregroundColor(color)
                Spacer()
                Text("\(universities.count)")
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(color.opacity(0.2))
                    .cornerRadius(8)
            }
            .padding(.horizontal)
            
            ForEach(universities) { university in
                UniversityCard(university: university)
            }
        }
    }
}

// MARK: - University Card
struct UniversityCard: View {
    let university: University
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(university.name)
                    .font(.headline)
                Spacer()
                Text("\(Int(university.matchScore))%")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(matchScoreColor(university.matchScore))
            }
            
            Text(university.program)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Text(university.country)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(8)
        .shadow(radius: 2)
        .padding(.horizontal)
    }
    
    private func matchScoreColor(_ score: Double) -> Color {
        switch score {
        case 70...:
            return .green
        case 50..<70:
            return .orange
        default:
            return .gray
        }
    }
}

// MARK: - Preview
#Preview {
    MatchResultsView()
}
```

---

## 3️⃣ Login Form Örneği

### Login View Model ve State Yönetimi

```swift
import SwiftUI

// MARK: - Login View Model
@MainActor
class LoginViewModel: ObservableObject {
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var isLoggedIn = false
    
    // Form validation
    var isValid: Bool {
        !email.isEmpty && !password.isEmpty &&
        email.contains("@") && password.count >= 6
    }
    
    func login() async {
        guard isValid else {
            errorMessage = "Please enter valid email and password (min 6 characters)"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        do {
            // Backend API'ye login request gönder
            let response = try await APIService.login(
                email: email,
                password: password
            )
            
            if response.success {
                // Login başarılı - token kaydet vs.
                isLoggedIn = true
                isLoading = false
            } else {
                errorMessage = response.error ?? "Login failed"
                isLoading = false
            }
        } catch {
            errorMessage = (error as? APIError)?.userFriendlyMessage ?? error.localizedDescription
            isLoading = false
        }
    }
}

// MARK: - Login View
struct LoginView: View {
    @StateObject private var viewModel = LoginViewModel()
    @FocusState private var focusedField: Field?
    
    enum Field {
        case email, password
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: 24) {
                // Logo/Header
                VStack(spacing: 8) {
                    Image(systemName: "graduationcap.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)
                    
                    Text("University Match AI")
                        .font(.title)
                        .fontWeight(.bold)
                }
                .padding(.top, 60)
                
                Spacer()
                
                // Login Form
                VStack(spacing: 16) {
                    // Email Field
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Email")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        TextField("Enter your email", text: $viewModel.email)
                            .textFieldStyle(.roundedBorder)
                            .keyboardType(.emailAddress)
                            .autocapitalization(.none)
                            .focused($focusedField, equals: .email)
                            .submitLabel(.next)
                            .onSubmit {
                                focusedField = .password
                            }
                    }
                    
                    // Password Field
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Password")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        SecureField("Enter your password", text: $viewModel.password)
                            .textFieldStyle(.roundedBorder)
                            .focused($focusedField, equals: .password)
                            .submitLabel(.go)
                            .onSubmit {
                                if viewModel.isValid {
                                    Task {
                                        await viewModel.login()
                                    }
                                }
                            }
                    }
                    
                    // Error Message
                    if let error = viewModel.errorMessage {
                        HStack {
                            Image(systemName: "exclamationmark.circle.fill")
                                .foregroundColor(.red)
                            Text(error)
                                .font(.caption)
                                .foregroundColor(.red)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    
                    // Login Button
                    Button(action: {
                        Task {
                            await viewModel.login()
                        }
                    }) {
                        HStack {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            } else {
                                Text("Login")
                                    .fontWeight(.semibold)
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.isValid && !viewModel.isLoading ? Color.blue : Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                    .disabled(!viewModel.isValid || viewModel.isLoading)
                    
                    // Sign Up Link
                    HStack {
                        Text("Don't have an account?")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Button("Sign Up") {
                            // Navigate to sign up
                        }
                        .font(.caption)
                        .fontWeight(.semibold)
                    }
                }
                .padding(.horizontal, 32)
                
                Spacer()
            }
            .navigationBarHidden(true)
            .fullScreenCover(isPresented: $viewModel.isLoggedIn) {
                // Main app content after login
                ContentView()
            }
        }
    }
}

// MARK: - API Service Extension (Login)
extension APIService {
    static func login(email: String, password: String) async throws -> LoginResponse {
        let requestBody: [String: Any] = [
            "email": email,
            "password": password
        ]
        
        return try await makeRequest(
            endpoint: "/login",
            method: "POST",
            body: requestBody
        )
    }
}

// MARK: - Login Response Model
struct LoginResponse: Codable {
    let success: Bool
    let token: String?
    let user: User?
    let error: String?
}

struct User: Codable {
    let id: Int
    let email: String
    let name: String?
}

// MARK: - Preview
#Preview {
    LoginView()
}
```

---

## 📝 Özet

### State Yönetimi Best Practices:

1. **@StateObject**: View'a ait ve lifecycle'ı view ile bağlı
2. **@ObservableObject**: Observable property'ler için
3. **@Published**: Değişiklikleri otomatik yayınlar
4. **@MainActor**: UI güncellemeleri için main thread'de çalışır

### Error Handling:

- ✅ Her API çağrısında try-catch kullan
- ✅ Kullanıcı dostu hata mesajları göster
- ✅ Retry mekanizması ekle
- ✅ Loading state'leri göster

### REST API Pattern:

```swift
// 1. ViewModel oluştur
@MainActor class MyViewModel: ObservableObject {
    @Published var data: [Model] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
}

// 2. Async function ile API çağrısı
func fetchData() async {
    isLoading = true
    do {
        data = try await APIService.fetchData()
    } catch {
        errorMessage = error.localizedDescription
    }
    isLoading = false
}

// 3. View'da kullan
@StateObject var viewModel = MyViewModel()
Task { await viewModel.fetchData() }
```

---

**Sonraki Adım**: Bu örnekleri kullanarak kendi view'larınızı oluşturabilirsiniz. Herhangi bir sorunuz varsa sormaktan çekinmeyin!

