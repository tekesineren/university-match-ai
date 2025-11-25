//
//  APIService.swift
//  UniversityMatchAI
//
//  Backend API ile iletişim servisi
//  REST API çağrıları için tüm endpoint'ler burada
//

import Foundation

// MARK: - API Service Class
class APIService {
    
    // MARK: - Configuration
    
    /// Backend API base URL
    /// 
    /// ⚠️ ÖNEMLİ NOTLAR:
    /// - Simulator için: `localhost` çalışır
    /// - Gerçek iPhone için: Bilgisayarınızın IP adresini kullanın
    ///   Örnek: `http://192.168.1.100:5000/api`
    /// - Production için: Backend'in deploy edildiği URL'i kullanın
    ///   Örnek: `https://your-backend.railway.app/api`
    static let baseURL = "http://localhost:5000/api"
    
    /// Request timeout süresi (saniye)
    static let timeout: TimeInterval = 30.0
    
    // MARK: - Generic Request Helper
    
    /// Generic API request helper method
    /// Tüm API çağrıları için ortak kullanılır
    private static func makeRequest<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: [String: Any]? = nil
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            throw APIError.invalidURL
        }
        
        // URLRequest oluştur
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.timeoutInterval = timeout
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        // Request body ekle (POST/PUT için)
        if let body = body {
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
                // Debug: Request body'yi logla
                if let jsonString = String(data: request.httpBody!, encoding: .utf8) {
                    print("📤 Request Body: \(jsonString)")
                }
            } catch {
                throw APIError.encodeError
            }
        }
        
        // Debug: Request URL'i logla
        print("🌐 API Request: \(method) \(url.absoluteString)")
        
        // Network request yap
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            // HTTP response kontrolü
            guard let httpResponse = response as? HTTPURLResponse else {
                throw APIError.invalidResponse
            }
            
            // Debug: Response status code
            print("📥 Response Status: \(httpResponse.statusCode)")
            
            // Error handling
            guard (200...299).contains(httpResponse.statusCode) else {
                // Error response decode et
                if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                    throw APIError.serverError(errorResponse.error)
                }
                throw APIError.httpError(httpResponse.statusCode)
            }
            
            // JSON decode
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            
            do {
                let result = try decoder.decode(T.self, from: data)
                print("✅ Successfully decoded response")
                return result
            } catch let decodeError {
                // Debug: Decode error detayları
                print("❌ Decode Error: \(decodeError)")
                if let responseString = String(data: data, encoding: .utf8) {
                    print("📄 Response Data: \(responseString)")
                }
                throw APIError.decodeError
            }
            
        } catch let error as APIError {
            throw error
        } catch {
            throw APIError.networkError(error)
        }
    }
    
    // MARK: - API Endpoints
    
    /// Health check endpoint
    /// API'nin çalışıp çalışmadığını kontrol eder
    /// 
    /// **Endpoint:** `GET /api/health`
    /// **Response:** `{"status": "ok", "message": "API is running"}`
    static func checkHealth() async throws -> HealthResponse {
        return try await makeRequest(endpoint: "/health")
    }
    
    /// Tüm üniversiteleri getir
    /// 
    /// **Endpoint:** `GET /api/universities`
    /// **Response:** `{"universities": [...]}`
    static func getUniversities() async throws -> [University] {
        let response: UniversitiesResponse = try await makeRequest(endpoint: "/universities")
        return response.universities
    }
    
    /// Kullanıcı profiline göre üniversiteleri eşleştir
    /// 
    /// **Endpoint:** `POST /api/match`
    /// **Request Body:** UserProfile dictionary
    /// **Response:** `{"success": true, "results": {...}}`
    static func matchUniversities(profile: UserProfile) async throws -> MatchResponse {
        let requestBody = profile.toDictionary()
        return try await makeRequest(
            endpoint: "/match",
            method: "POST",
            body: requestBody
        )
    }
    
    // MARK: - Future Endpoints (Not yet implemented)
    
    /// CV upload ve parse (gelecekte eklenecek)
    /// Multipart form data ile dosya upload gerektirir
    static func parseCV(fileData: Data, fileName: String) async throws -> [String: Any] {
        // TODO: Multipart form data implementation
        throw APIError.notImplemented
    }
    
    /// Feedback gönder (gelecekte eklenecek)
    static func submitFeedback(
        name: String,
        email: String,
        message: String,
        type: String = "general"
    ) async throws -> [String: Any] {
        // TODO: Feedback endpoint implementation
        throw APIError.notImplemented
    }
}

// MARK: - API Error Types

enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case decodeError
    case encodeError
    case httpError(Int)
    case serverError(String)
    case networkError(Error)
    case notImplemented
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL - Check baseURL configuration"
        case .invalidResponse:
            return "Invalid response from server"
        case .decodeError:
            return "Failed to decode response data"
        case .encodeError:
            return "Failed to encode request data"
        case .httpError(let code):
            return "HTTP Error: \(code)"
        case .serverError(let message):
            return "Server Error: \(message)"
        case .networkError(let error):
            return "Network Error: \(error.localizedDescription)"
        case .notImplemented:
            return "This feature is not implemented yet"
        }
    }
    
    /// Kullanıcı dostu hata mesajı
    var userFriendlyMessage: String {
        switch self {
        case .networkError:
            return "Network connection error. Please check your internet connection and try again."
        case .invalidURL:
            return "Configuration error. Please check API URL settings."
        case .serverError(let message):
            return message
        case .httpError(404):
            return "API endpoint not found. Please check if backend is running."
        case .httpError(500...):
            return "Server error. Please try again later."
        default:
            return errorDescription ?? "An unknown error occurred"
        }
    }
}

// MARK: - Usage Examples

/*
 
 // MARK: - Example 1: Health Check
 Task {
     do {
         let health = try await APIService.checkHealth()
         print("✅ API Status: \(health.status)")
         print("📝 Message: \(health.message)")
     } catch {
         print("❌ Error: \(error.localizedDescription)")
     }
 }
 
 // MARK: - Example 2: Get All Universities
 Task {
     do {
         let universities = try await APIService.getUniversities()
         print("📚 Total Universities: \(universities.count)")
         for uni in universities.prefix(5) {
             print("- \(uni.name) (\(uni.country))")
         }
     } catch {
         print("❌ Error: \(error.localizedDescription)")
     }
 }
 
 // MARK: - Example 3: Match Universities
 let profile = UserProfile(
     gpa: 3.8,
     languageTestType: "toefl",
     languageTestScore: 110,
     background: ["engineering", "robotics", "control systems"],
     workExperience: 2.0,
     researchExperience: 1.0,
     publications: 2,
     recommendationLetters: 3
 )
 
 Task {
     do {
         let response = try await APIService.matchUniversities(profile: profile)
         if response.success, let results = response.results {
             print("🎯 High Match: \(results.highMatch.count) universities")
             print("📊 Medium Match: \(results.mediumMatch.count) universities")
             print("📈 Low Match: \(results.lowMatch.count) universities")
             
             // İlk high match üniversitesini göster
             if let firstMatch = results.highMatch.first {
                 print("\n🏆 Top Match:")
                 print("   Name: \(firstMatch.name)")
                 print("   Program: \(firstMatch.program)")
                 print("   Match Score: \(firstMatch.matchScore)")
             }
         } else {
             print("❌ Error: \(response.error ?? "Unknown error")")
         }
     } catch {
         if let apiError = error as? APIError {
             print("❌ API Error: \(apiError.userFriendlyMessage)")
         } else {
             print("❌ Error: \(error.localizedDescription)")
         }
     }
 }
 
 */
