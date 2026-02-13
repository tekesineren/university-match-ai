//
//  Models.swift
//  UniversityMatchAI
//
//  Veri modelleri - Backend API ile uyumlu
//

import Foundation

// MARK: - User Profile Model
/// Kullanıcı profili - Backend API'nin beklediği formatta
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
/// Üniversite modeli - Backend'den gelen veri formatı
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

/// Match API response modeli
struct MatchResponse: Codable {
    let success: Bool
    let results: MatchResults?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case success, results, error
    }
}

/// Eşleştirme sonuçları - kategorize edilmiş üniversiteler
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

/// Universities list API response
struct UniversitiesResponse: Codable {
    let universities: [University]
}

/// Health check API response
struct HealthResponse: Codable {
    let status: String
    let message: String
}

// MARK: - Error Response Model
struct ErrorResponse: Codable {
    let success: Bool
    let error: String
}

// MARK: - Helper Extensions

extension UserProfile {
    /// Profil geçerliliğini kontrol et
    var isValid: Bool {
        gpa > 0 &&
        !languageTestType.isEmpty &&
        languageTestScore > 0 &&
        !background.isEmpty
    }
    
    /// Backend API'ye göndermek için dictionary formatına çevir
    func toDictionary() -> [String: Any] {
        var dict: [String: Any] = [
            "gpa": gpa,
            "grading_system": gradingSystem,
            "language_test_type": languageTestType,
            "language_test_score": languageTestScore,
            "background": background,
            "work_experience": workExperience,
            "research_experience": researchExperience,
            "publications": publications,
            "recommendation_letters": recommendationLetters,
            "undergraduate_university_ranking": undergraduateUniversityRanking,
            "project_experience": projectExperience,
            "competition_achievements": competitionAchievements,
            "motivation_letter": motivationLetter,
            "has_masters_degree": hasMastersDegree,
            "masters_university_ranking": mastersUniversityRanking
        ]
        
        if let greScore = greScore {
            dict["gre_score"] = greScore
        }
        if let gmatScore = gmatScore {
            dict["gmat_score"] = gmatScore
        }
        
        return dict
    }
}

extension University {
    /// Match score'a göre kategori döndür
    var matchCategory: String {
        switch matchScore {
        case 70...:
            return "High Match"
        case 50..<70:
            return "Medium Match"
        case 30..<50:
            return "Low Match"
        default:
            return "Extra Options"
        }
    }
    
    /// Match score color
    var matchColor: String {
        switch matchScore {
        case 70...:
            return "green"
        case 50..<70:
            return "orange"
        case 30..<50:
            return "yellow"
        default:
            return "gray"
        }
    }
}
