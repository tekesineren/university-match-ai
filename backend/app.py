"""
Master Application Agent - Backend API
Ana eşleştirme algoritması ve API endpoint'leri
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import re
import io
from datetime import datetime, date

# =============================================================================
# SYNONYM MAPPING SYSTEM - Teknoloji ve Beceri Eşleştirme
# =============================================================================
# CV'lerde farklı yazılabilen teknolojileri standart forma getir
# Örnek: "JS" -> "JavaScript", "Node" -> "Node.js"

SKILL_SYNONYMS = {
    # JavaScript Ecosystem
    "javascript": ["javascript", "js", "ecmascript", "es6", "es2015", "es2020", "vanilla js"],
    "typescript": ["typescript", "ts"],
    "node.js": ["node.js", "nodejs", "node", "node js"],
    "react": ["react", "reactjs", "react.js", "react js"],
    "vue.js": ["vue.js", "vue", "vuejs", "vue js", "vue 3"],
    "angular": ["angular", "angularjs", "angular.js", "angular 2+"],
    "next.js": ["next.js", "nextjs", "next"],
    "express.js": ["express.js", "expressjs", "express"],
    
    # Python Ecosystem
    "python": ["python", "py", "python3", "python 3"],
    "django": ["django", "django rest framework", "drf"],
    "flask": ["flask", "flask api"],
    "fastapi": ["fastapi", "fast api"],
    "pandas": ["pandas", "pd"],
    "numpy": ["numpy", "np"],
    "tensorflow": ["tensorflow", "tf", "tensorflow 2"],
    "pytorch": ["pytorch", "torch"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    
    # Java Ecosystem
    "java": ["java", "java 8", "java 11", "java 17", "jdk"],
    "spring": ["spring", "spring boot", "springboot", "spring framework"],
    "kotlin": ["kotlin", "kt"],
    
    # C/C++ Family
    "c": ["c language", "c programming"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c#": ["c#", "csharp", "c sharp", ".net c#"],
    ".net": [".net", "dotnet", ".net core", ".net framework", "asp.net"],
    
    # Mobile Development
    "react native": ["react native", "react-native", "rn"],
    "flutter": ["flutter", "dart flutter"],
    "swift": ["swift", "swiftui", "swift ui"],
    "ios": ["ios", "ios development", "iphone development"],
    "android": ["android", "android development", "android studio"],
    
    # Databases
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres", "psql", "pg"],
    "mongodb": ["mongodb", "mongo", "mongo db"],
    "redis": ["redis", "redis db"],
    "firebase": ["firebase", "firestore", "firebase db"],
    "supabase": ["supabase", "supabase db"],
    
    # Cloud & DevOps
    "aws": ["aws", "amazon web services", "amazon aws"],
    "azure": ["azure", "microsoft azure", "ms azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "docker": ["docker", "docker container", "containerization"],
    "kubernetes": ["kubernetes", "k8s", "kube"],
    "ci/cd": ["ci/cd", "cicd", "ci cd", "continuous integration", "continuous deployment"],
    "git": ["git", "github", "gitlab", "bitbucket", "version control"],
    
    # AI/ML
    "machine learning": ["machine learning", "ml", "makine öğrenmesi"],
    "deep learning": ["deep learning", "dl", "derin öğrenme"],
    "artificial intelligence": ["artificial intelligence", "ai", "yapay zeka"],
    "nlp": ["nlp", "natural language processing", "doğal dil işleme"],
    "computer vision": ["computer vision", "cv", "görüntü işleme", "image processing"],
    "llm": ["llm", "large language model", "gpt", "chatgpt", "claude", "mistral"],
    
    # Data Engineering
    "etl": ["etl", "extract transform load", "data pipeline"],
    "spark": ["spark", "apache spark", "pyspark"],
    "hadoop": ["hadoop", "apache hadoop", "hdfs"],
    "kafka": ["kafka", "apache kafka"],
    "airflow": ["airflow", "apache airflow"],
    
    # Frontend Tools
    "html": ["html", "html5", "html 5"],
    "css": ["css", "css3", "css 3"],
    "sass": ["sass", "scss"],
    "tailwind": ["tailwind", "tailwindcss", "tailwind css"],
    "bootstrap": ["bootstrap", "bootstrap 5"],
    
    # Other Languages
    "go": ["go", "golang", "go lang"],
    "rust": ["rust", "rust lang"],
    "ruby": ["ruby", "ruby on rails", "rails", "ror"],
    "php": ["php", "laravel", "symfony"],
    "scala": ["scala"],
    "r": ["r", "r language", "r programming"],
    
    # Soft Skills (Türkçe dahil)
    "problem solving": ["problem solving", "problem çözme", "analitik düşünme"],
    "teamwork": ["teamwork", "team work", "takım çalışması", "ekip çalışması"],
    "communication": ["communication", "iletişim", "communication skills"],
    "leadership": ["leadership", "liderlik", "team lead", "takım liderliği"],
    "agile": ["agile", "scrum", "kanban", "çevik metodoloji"],
}

def normalize_skill(skill_text):
    """
    Bir beceri metnini standart forma getirir.
    
    Örnek:
        "JS" -> "javascript"
        "Node" -> "node.js"
        "React.js" -> "react"
    """
    if not skill_text:
        return None
    
    skill_lower = skill_text.lower().strip()
    
    # Tüm synonym gruplarını kontrol et
    for standard_name, synonyms in SKILL_SYNONYMS.items():
        for synonym in synonyms:
            if skill_lower == synonym.lower():
                return standard_name
            # Partial match için (kelime sınırlarıyla)
            pattern = r'\b' + re.escape(synonym.lower()) + r'\b'
            if re.search(pattern, skill_lower):
                return standard_name
    
    # Eşleşme bulunamazsa orijinali döndür
    return skill_lower

def extract_skills_from_cv(text):
    """
    CV metninden becerileri çıkarır ve normalize eder.
    
    Returns:
        dict: {
            'raw_skills': [...],      # CV'de bulunan ham beceriler
            'normalized_skills': [...], # Normalize edilmiş beceriler
            'skill_categories': {...}  # Kategorilere göre gruplandırılmış
        }
    """
    if not text:
        return {'raw_skills': [], 'normalized_skills': [], 'skill_categories': {}}
    
    text_lower = text.lower()
    found_skills = set()
    raw_skills = set()
    
    # Tüm synonym gruplarını tara
    for standard_name, synonyms in SKILL_SYNONYMS.items():
        for synonym in synonyms:
            # Kelime sınırlarıyla exact match
            pattern = r'\b' + re.escape(synonym.lower()) + r'\b'
            if re.search(pattern, text_lower):
                raw_skills.add(synonym)
                found_skills.add(standard_name)
                break  # Bu grup için bir eşleşme yeterli
    
    # Kategorilere ayır
    categories = {
        'programming_languages': [],
        'frameworks': [],
        'databases': [],
        'cloud_devops': [],
        'ai_ml': [],
        'soft_skills': [],
        'other': []
    }
    
    language_keywords = ['javascript', 'typescript', 'python', 'java', 'c++', 'c#', 'c', 'go', 'rust', 'ruby', 'php', 'scala', 'r', 'kotlin', 'swift']
    framework_keywords = ['react', 'vue.js', 'angular', 'next.js', 'node.js', 'express.js', 'django', 'flask', 'fastapi', 'spring', '.net', 'react native', 'flutter']
    database_keywords = ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'firebase', 'supabase']
    cloud_keywords = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'git']
    ai_keywords = ['machine learning', 'deep learning', 'artificial intelligence', 'nlp', 'computer vision', 'llm', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy']
    soft_keywords = ['problem solving', 'teamwork', 'communication', 'leadership', 'agile']
    
    for skill in found_skills:
        if skill in language_keywords:
            categories['programming_languages'].append(skill)
        elif skill in framework_keywords:
            categories['frameworks'].append(skill)
        elif skill in database_keywords:
            categories['databases'].append(skill)
        elif skill in cloud_keywords:
            categories['cloud_devops'].append(skill)
        elif skill in ai_keywords:
            categories['ai_ml'].append(skill)
        elif skill in soft_keywords:
            categories['soft_skills'].append(skill)
        else:
            categories['other'].append(skill)
    
    return {
        'raw_skills': list(raw_skills),
        'normalized_skills': list(found_skills),
        'skill_categories': categories
    }

def get_skill_match_score(user_skills, required_skills):
    """
    Kullanıcı becerileri ile gereken beceriler arasındaki eşleşme skorunu hesaplar.
    Synonym mapping kullanarak akıllı eşleştirme yapar.
    
    Returns:
        float: 0-1 arası eşleşme skoru
    """
    if not required_skills:
        return 1.0  # Gereksinim yoksa tam eşleşme
    if not user_skills:
        return 0.0  # Kullanıcı becerisi yoksa sıfır
    
    # Normalize et
    normalized_user = set(normalize_skill(s) for s in user_skills if s)
    normalized_required = set(normalize_skill(s) for s in required_skills if s)
    
    # None değerleri temizle
    normalized_user.discard(None)
    normalized_required.discard(None)
    
    if not normalized_required:
        return 1.0
    
    matches = normalized_user & normalized_required
    return len(matches) / len(normalized_required)
from premium import rate_limit, get_user_id, get_user_stats, upgrade_user, create_api_key, require_tier
from stripe_integration import create_checkout_session, handle_stripe_webhook
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

app = Flask(__name__)

# CORS settings - Allow all origins (for Expo Go and web apps)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Expo Go ve tüm web uygulamaları için
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# =============================================================================
# DOCUMENT TEMPLATES (Üniversitelere eklenecek standart belgeler)
# =============================================================================

# Standart belge şablonları - Ülkeye göre özelleştirilebilir
DOCUMENT_TEMPLATES = {
    "cv": {
        "type": "cv",
        "name": "Curriculum Vitae",
        "formats": ["pdf"],
        "max_size_mb": 2,
        "required": True,
        "tips": "Academic CV format, 1-2 pages"
    },
    "transcript": {
        "type": "transcript",
        "name": "Official Transcript",
        "formats": ["pdf"],
        "max_size_mb": 5,
        "required": True,
        "tips": "Must be officially sealed"
    },
    "motivation": {
        "type": "motivation_letter",
        "name": "Statement of Purpose",
        "formats": ["pdf", "docx"],
        "max_size_mb": 1,
        "required": True,
        "word_limit": {"min": 500, "max": 1000},
        "tips": "Explain why this program and your goals"
    },
    "recommendation_2": {
        "type": "recommendation",
        "name": "Letters of Recommendation",
        "formats": ["pdf"],
        "max_size_mb": 2,
        "required": True,
        "count": 2,
        "tips": "From professors or employers"
    },
    "recommendation_3": {
        "type": "recommendation",
        "name": "Letters of Recommendation",
        "formats": ["pdf"],
        "max_size_mb": 2,
        "required": True,
        "count": 3,
        "tips": "At least 2 academic references"
    },
    "toefl": {
        "type": "language_cert",
        "name": "English Proficiency (TOEFL/IELTS)",
        "formats": ["pdf"],
        "max_size_mb": 2,
        "required": True,
        "accepted_tests": ["TOEFL iBT", "IELTS Academic"],
        "tips": "Must be valid (within 2 years)"
    },
    "passport": {
        "type": "passport",
        "name": "Passport Copy",
        "formats": ["pdf", "jpg"],
        "max_size_mb": 3,
        "required": True,
        "tips": "Bio page, valid for program duration"
    },
    "gre": {
        "type": "gre",
        "name": "GRE Score",
        "formats": ["pdf"],
        "max_size_mb": 2,
        "required": False,
        "tips": "Recommended but not always required"
    },
    "portfolio": {
        "type": "portfolio",
        "name": "Portfolio/Projects",
        "formats": ["pdf", "url"],
        "max_size_mb": 10,
        "required": False,
        "tips": "GitHub or personal website"
    }
}

def get_standard_docs(country, recommendation_count=2, gre_required=False):
    """Ülkeye göre standart belge listesi oluştur"""
    docs = [
        DOCUMENT_TEMPLATES["cv"].copy(),
        DOCUMENT_TEMPLATES["transcript"].copy(),
        DOCUMENT_TEMPLATES["motivation"].copy(),
        DOCUMENT_TEMPLATES[f"recommendation_{recommendation_count}"].copy() if recommendation_count in [2, 3] else DOCUMENT_TEMPLATES["recommendation_2"].copy(),
        DOCUMENT_TEMPLATES["toefl"].copy(),
        DOCUMENT_TEMPLATES["passport"].copy()
    ]
    
    # USA için GRE genellikle gerekli
    if country == "USA" or gre_required:
        gre = DOCUMENT_TEMPLATES["gre"].copy()
        gre["required"] = True
        docs.append(gre)
    
    return docs

# University database with document requirements
UNIVERSITIES = [
    {
        "id": 1,
        "name": "ETH Zurich",
        "program": "MSc in Robotics, Systems and Control",
        "country": "Switzerland",
        "min_gpa": 3.5,
        "min_language_score": 100,
        "required_background": ["engineering", "robotics", "control systems"],
        "match_score": 0,
        "required_documents": get_standard_docs("Switzerland", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-15", "spring_2026": "2025-07-15"},
        "application_fee": {"amount": 150, "currency": "CHF"},
        "application_url": "https://ethz.ch/apply"
    },
    {
        "id": 2,
        "name": "MIT",
        "program": "Master of Science in Mechanical Engineering",
        "country": "USA",
        "min_gpa": 3.7,
        "min_language_score": 100,
        "required_background": ["engineering", "mechanical engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("USA", 3, gre_required=True),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-15"},
        "application_fee": {"amount": 75, "currency": "USD"},
        "application_url": "https://gradadmissions.mit.edu"
    },
    {
        "id": 3,
        "name": "Stanford University",
        "program": "MS in Computer Science",
        "country": "USA",
        "min_gpa": 3.8,
        "min_language_score": 100,
        "required_background": ["computer science", "engineering", "mathematics"],
        "match_score": 0,
        "required_documents": get_standard_docs("USA", 3, gre_required=True),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-04"},
        "application_fee": {"amount": 125, "currency": "USD"},
        "application_url": "https://gradadmissions.stanford.edu"
    },
    {
        "id": 4,
        "name": "Carnegie Mellon University",
        "program": "MS in Robotics",
        "country": "USA",
        "min_gpa": 3.6,
        "min_language_score": 100,
        "required_background": ["robotics", "engineering", "computer science"],
        "match_score": 0,
        "required_documents": get_standard_docs("USA", 3, gre_required=True),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-01"},
        "application_fee": {"amount": 75, "currency": "USD"},
        "application_url": "https://www.ri.cmu.edu/education/academic-programs/master-of-science-robotics/"
    },
    {
        "id": 5,
        "name": "University of California, Berkeley",
        "program": "MEng in Electrical Engineering and Computer Sciences",
        "country": "USA",
        "min_gpa": 3.5,
        "min_language_score": 90,
        "required_background": ["electrical engineering", "computer science", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("USA", 3, gre_required=False),
        "optional_documents": [DOCUMENT_TEMPLATES["gre"], DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-06"},
        "application_fee": {"amount": 135, "currency": "USD"},
        "application_url": "https://grad.berkeley.edu"
    },
    {
        "id": 6,
        "name": "Imperial College London",
        "program": "MSc in Advanced Robotics",
        "country": "UK",
        "min_gpa": 3.5,
        "min_language_score": 92,
        "required_background": ["robotics", "engineering", "mechanical engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("UK", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 80, "currency": "GBP"},
        "application_url": "https://www.imperial.ac.uk/study/apply/postgraduate-taught/"
    },
    {
        "id": 7,
        "name": "University of Cambridge",
        "program": "MPhil in Advanced Computer Science",
        "country": "UK",
        "min_gpa": 3.7,
        "min_language_score": 110,
        "required_background": ["computer science", "mathematics", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("UK", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-03"},
        "application_fee": {"amount": 75, "currency": "GBP"},
        "application_url": "https://www.graduate.study.cam.ac.uk"
    },
    {
        "id": 8,
        "name": "EPFL",
        "program": "Master in Robotics",
        "country": "Switzerland",
        "min_gpa": 3.5,
        "min_language_score": 100,
        "required_background": ["robotics", "engineering", "control systems"],
        "match_score": 0,
        "required_documents": get_standard_docs("Switzerland", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15", "spring_2026": "2025-09-15"},
        "application_fee": {"amount": 150, "currency": "CHF"},
        "application_url": "https://www.epfl.ch/education/admission/"
    },
    {
        "id": 9,
        "name": "TU Delft",
        "program": "MSc in Robotics",
        "country": "Netherlands",
        "min_gpa": 3.3,
        "min_language_score": 90,
        "required_background": ["robotics", "engineering", "mechanical engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Netherlands", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 100, "currency": "EUR"},
        "application_url": "https://www.tudelft.nl/onderwijs/opleidingen/masters"
    },
    {
        "id": 10,
        "name": "Technical University of Munich",
        "program": "MSc in Robotics, Cognition, Intelligence",
        "country": "Germany",
        "min_gpa": 3.4,
        "min_language_score": 88,
        "required_background": ["robotics", "computer science", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Germany", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15", "spring_2026": "2025-05-31"},
        "application_fee": {"amount": 0, "currency": "EUR"},
        "application_url": "https://www.tum.de/en/studies/application"
    },
    {
        "id": 11,
        "name": "ETH Zurich",
        "program": "MSc in Computer Science",
        "country": "Switzerland",
        "min_gpa": 3.5,
        "min_language_score": 100,
        "required_background": ["computer science", "mathematics", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Switzerland", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-15"},
        "application_fee": {"amount": 150, "currency": "CHF"},
        "application_url": "https://ethz.ch/apply"
    },
    {
        "id": 12,
        "name": "Georgia Institute of Technology",
        "program": "MS in Robotics",
        "country": "USA",
        "min_gpa": 3.5,
        "min_language_score": 100,
        "required_background": ["robotics", "engineering", "computer science"],
        "match_score": 0,
        "required_documents": get_standard_docs("USA", 3, gre_required=False),
        "optional_documents": [DOCUMENT_TEMPLATES["gre"], DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-01"},
        "application_fee": {"amount": 85, "currency": "USD"},
        "application_url": "https://grad.gatech.edu"
    },
    {
        "id": 13,
        "name": "University of Oxford",
        "program": "MSc in Computer Science",
        "country": "UK",
        "min_gpa": 3.7,
        "min_language_score": 110,
        "required_background": ["computer science", "mathematics", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("UK", 3),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-20"},
        "application_fee": {"amount": 75, "currency": "GBP"},
        "application_url": "https://www.ox.ac.uk/admissions/graduate/"
    },
    {
        "id": 14,
        "name": "University of Toronto",
        "program": "MSc in Mechanical and Industrial Engineering",
        "country": "Canada",
        "min_gpa": 3.3,
        "min_language_score": 93,
        "required_background": ["mechanical engineering", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Canada", 3),
        "optional_documents": [DOCUMENT_TEMPLATES["gre"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 125, "currency": "CAD"},
        "application_url": "https://www.sgs.utoronto.ca/admissions/"
    },
    {
        "id": 15,
        "name": "National University of Singapore",
        "program": "MSc in Mechanical Engineering",
        "country": "Singapore",
        "min_gpa": 3.4,
        "min_language_score": 85,
        "required_background": ["mechanical engineering", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Singapore", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["gre"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 50, "currency": "SGD"},
        "application_url": "https://www.nus.edu.sg/admissions/graduate"
    },
    {
        "id": 16,
        "name": "KAIST",
        "program": "MS in Robotics",
        "country": "South Korea",
        "min_gpa": 3.3,
        "min_language_score": 83,
        "required_background": ["robotics", "engineering", "computer science"],
        "match_score": 0,
        "required_documents": get_standard_docs("South Korea", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-03-15", "spring_2026": "2025-09-15"},
        "application_fee": {"amount": 80000, "currency": "KRW"},
        "application_url": "https://admission.kaist.ac.kr"
    },
    {
        "id": 17,
        "name": "University of Tokyo",
        "program": "Master in Information Science and Technology",
        "country": "Japan",
        "min_gpa": 3.4,
        "min_language_score": 90,
        "required_background": ["computer science", "engineering", "mathematics"],
        "match_score": 0,
        "required_documents": get_standard_docs("Japan", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2024-12-01"},
        "application_fee": {"amount": 30000, "currency": "JPY"},
        "application_url": "https://www.u-tokyo.ac.jp/en/admissions/graduate.html"
    },
    {
        "id": 18,
        "name": "KTH Royal Institute of Technology",
        "program": "MSc in Systems, Control and Robotics",
        "country": "Sweden",
        "min_gpa": 3.3,
        "min_language_score": 90,
        "required_background": ["robotics", "control systems", "engineering"],
        "match_score": 0,
        "required_documents": get_standard_docs("Sweden", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 900, "currency": "SEK"},
        "application_url": "https://www.kth.se/en/studies/master/application"
    },
    {
        "id": 19,
        "name": "Aalto University",
        "program": "MSc in Automation and Electrical Engineering",
        "country": "Finland",
        "min_gpa": 3.2,
        "min_language_score": 92,
        "required_background": ["electrical engineering", "engineering", "control systems"],
        "match_score": 0,
        "required_documents": get_standard_docs("Finland", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-03"},
        "application_fee": {"amount": 0, "currency": "EUR"},
        "application_url": "https://www.aalto.fi/en/admission-services"
    },
    {
        "id": 20,
        "name": "University of Edinburgh",
        "program": "MSc in Robotics and Autonomous Systems",
        "country": "UK",
        "min_gpa": 3.4,
        "min_language_score": 92,
        "required_background": ["robotics", "engineering", "computer science"],
        "match_score": 0,
        "required_documents": get_standard_docs("UK", 2),
        "optional_documents": [DOCUMENT_TEMPLATES["portfolio"]],
        "deadlines": {"fall_2025": "2025-01-15"},
        "application_fee": {"amount": 60, "currency": "GBP"},
        "application_url": "https://www.ed.ac.uk/studying/postgraduate/applying"
    }
]

def normalize_language_score(test_type, score):
    """
    Farklı dil sınavlarını 0-100 arası normalize eder
    """
    score = float(score)
    
    if test_type == 'toefl':
        # TOEFL iBT: 0-120 -> 0-100
        return (score / 120.0) * 100
    elif test_type == 'ielts':
        # IELTS: 0-9 -> 0-100
        return (score / 9.0) * 100
    elif test_type == 'cambridge_cae':
        # Cambridge CAE: 0-210 -> 0-100 (Grade A: 200-210, B: 193-199, C: 180-192)
        return (score / 210.0) * 100
    elif test_type == 'cambridge_cpe':
        # Cambridge CPE: 0-230 -> 0-100 (Grade A: 220-230, B: 213-219, C: 200-212)
        return (score / 230.0) * 100
    elif test_type == 'pte':
        # PTE Academic: 0-90 -> 0-100
        return (score / 90.0) * 100
    elif test_type == 'duolingo':
        # Duolingo: 0-160 -> 0-100
        return (score / 160.0) * 100
    elif test_type == 'toeic':
        # TOEIC: 0-990 -> 0-100
        return (score / 990.0) * 100
    elif test_type == 'yds' or test_type == 'yokdil':
        # YDS/YÖKDİL: 0-100 -> direkt
        return score
    elif test_type == 'testdaf':
        # TestDaF: 0-5 -> 0-100 (3.0 = 60, 4.0 = 80, 5.0 = 100)
        return (score / 5.0) * 100
    elif test_type == 'goethe':
        # Goethe: 0-100 -> direkt
        return score
    elif test_type == 'dsh':
        # DSH: 0-3 -> 0-100 (DSH-1 = 33, DSH-2 = 67, DSH-3 = 100)
        return (score / 3.0) * 100
    elif test_type == 'delf' or test_type == 'dalf':
        # DELF/DALF: 0-100 -> direkt
        return score
    elif test_type == 'tcf':
        # TCF: 0-699 -> 0-100
        return (score / 699.0) * 100
    else:
        return 0

def convert_gpa_to_4_0(gpa, grading_system):
    """
    Farklı notlandırma sistemlerini 4.0 GPA sistemine dönüştürür
    """
    if not gpa or gpa == 0:
        return 0.0
    
    grading_system = grading_system or '4.0'
    
    if grading_system == '4.0':
        return float(gpa)
    elif grading_system == 'uk':
        # UK sistemi: 70+ = First (3.7-4.0), 60-69 = Upper Second (3.0-3.6), 50-59 = Lower Second (2.0-2.9), <50 = Third (0-1.9)
        if gpa >= 70:
            return min(4.0, 3.7 + ((gpa - 70) / 30.0) * 0.3)
        elif gpa >= 60:
            return 3.0 + ((gpa - 60) / 10.0) * 0.6
        elif gpa >= 50:
            return 2.0 + ((gpa - 50) / 10.0) * 0.9
        else:
            return (gpa / 50.0) * 1.9
    elif grading_system == 'german':
        # Alman sistemi: 1.0 en iyi, 4.0 en kötü - ters çevir
        return 5.0 - float(gpa)  # 1.0 -> 4.0, 2.0 -> 3.0, 3.0 -> 2.0, 4.0 -> 1.0
    elif grading_system == 'french':
        # Fransız sistemi: 0-20, 20 en iyi - (Not / 20) * 4.0
        return (float(gpa) / 20.0) * 4.0
    else:
        # Diğer sistemler için varsayılan olarak 100'lük sistem kabul et
        return (float(gpa) / 100.0) * 4.0

# ÖSYM sıralaması kaldırıldı - artık kullanılmıyor

def calculate_bonus_points(user_data):
    """
    Ek puan kriterlerini hesaplar (Savunma Sanayisi kriterlerine göre)
    """
    bonus = 0.0
    
    # 1. Work experience bonus points
    work_exp = user_data.get('work_experience', 0)
    if 2 <= work_exp < 5:
        bonus += 0.2
    elif 5 <= work_exp < 10:
        bonus += 0.4
    elif work_exp >= 10:
        bonus += 0.6  # 10+ yıl için ekstra
    
    # 2. Master's degree bonus points
    has_masters = user_data.get('has_masters_degree', False)
    masters_ranking = user_data.get('masters_university_ranking', '')
    if has_masters:
        if masters_ranking in ['top100', 'top500', 'top1000']:
            bonus += 0.2
        else:
            bonus += 0.1
    
    # 3. Lisans üniversitesi sıralaması (dolaylı etki - GPA'ya eklenir)
    # Bu kısım GPA hesaplamasında kullanılacak
    
    # 4. Project experience bonus points
    project_exp = user_data.get('project_experience', 'none')
    if project_exp == 'national':
        bonus += 0.1
    elif project_exp == 'eu':
        bonus += 0.15
    elif project_exp == 'international':
        bonus += 0.15
    elif project_exp == 'multiple':
        bonus += 0.2
    
    # 5. Yayınlar ek puanı (SCI, SCI Exp, SSCI)
    publications = user_data.get('publications', 0)
    if publications >= 1:
        bonus += 0.1
    
    # 6. GRE/GMAT ek puanı
    gre_score = user_data.get('gre_score')
    gmat_score = user_data.get('gmat_score')
    if gre_score and gre_score >= 320:
        bonus += 0.1
    elif gre_score and gre_score >= 310:
        bonus += 0.05
    if gmat_score and gmat_score >= 700:
        bonus += 0.1
    elif gmat_score and gmat_score >= 650:
        bonus += 0.05
    
    # 7. Yarışma başarıları ek puanı
    competition = user_data.get('competition_achievements', 'none')
    if competition == 'bronze':
        bonus += 0.05
    elif competition == 'silver':
        bonus += 0.08
    elif competition == 'gold':
        bonus += 0.1
    elif competition == 'multiple':
        bonus += 0.15
    
    return min(bonus, 1.0)  # Maksimum 1.0 ek puan

def calculate_minimum_gpa_requirement(user_data):
    """
    Ülke bazlı minimum GPA gereksinimini hesaplar (4.0 sisteminde)
    """
    gpa = user_data.get('gpa', 0)
    grading_system = user_data.get('grading_system', '4.0')
    country = user_data.get('country', 'turkey')
    
    # GPA'yi 4.0 sistemine dönüştür
    gpa_4_0 = convert_gpa_to_4_0(gpa, grading_system)
    
    # Bonus puanları hesapla
    bonus_points = calculate_bonus_points(user_data)
    
    # Türkiye için standart minimum (ÖSYM sıralaması kaldırıldı)
    if country == 'turkey':
        return 2.50 - bonus_points
    
    # Diğer ülkeler için standart minimum
    return 2.50 - bonus_points

def calculate_match_score(user_data, university):
    """
    Advanced matching score calculation
    
    Base Scores (100 points total):
    - GPA: 30 points
    - Language score: 20 points
    - Background: 15 points
    - Research experience: 10 points
    - Work experience: 8 points
    - Publications: 5 points
    - Recommendation letters: 5 points
    - University ranking: 4 points
    - GRE/GMAT: 3 points
    
    Bonus Points:
    - Project experience
    - Competition achievements
    - Master's degree
    """
    score = 0.0
    max_score = 100.0
    
    # GPA'yi 4.0 sistemine dönüştür
    gpa = user_data.get('gpa', 0)
    grading_system = user_data.get('grading_system', '4.0')
    gpa_4_0 = convert_gpa_to_4_0(gpa, grading_system)
    
    # Minimum GPA kontrolü
    min_gpa_req = calculate_minimum_gpa_requirement(user_data)
    
    # If 10+ years work experience, minimum GPA requirement is waived
    work_exp = user_data.get('work_experience', 0)
    if work_exp < 10 and gpa_4_0 < min_gpa_req:
        # Below minimum GPA = very low score
        return 20.0  # Very low match
    
    # 1. GPA evaluation (30 points) - on 4.0 scale
    if gpa_4_0 >= university['min_gpa']:
        gpa_score = min(30, (gpa_4_0 / 4.0) * 30)
        score += gpa_score
    else:
        score += (gpa_4_0 / university['min_gpa']) * 15
    
    # Üniversite sıralaması bonusu (GPA'ya eklenir)
    undergrad_ranking = user_data.get('undergraduate_university_ranking', '')
    if undergrad_ranking == 'top100':
        score += 2.0
    elif undergrad_ranking == 'top500':
        score += 1.5
    elif undergrad_ranking == 'top1000':
        score += 1.0
    
    # 2. Dil skoru değerlendirmesi (20 puan)
    language_test_type = user_data.get('language_test_type', '')
    language_test_score = user_data.get('language_test_score')
    
    if language_test_type and language_test_score:
        # Normalized score based on test type (0-100 scale)
        normalized_score = normalize_language_score(language_test_type, language_test_score)
        
        if normalized_score >= 90:  # Very high level
            score += 20
        elif normalized_score >= 80:  # High level
            score += 18
        elif normalized_score >= 70:  # Good level
            score += 15
        elif normalized_score >= 60:  # Orta seviye
            score += 10
        else:
            score += 5
    else:
        score += 0  # Dil sınavı yoksa puan yok
    
    # 3. Background eşleşmesi (15 puan)
    user_background = user_data.get('background', [])
    required_background = university.get('required_background', [])
    
    if required_background:
        common_fields = set(user_background) & set(required_background)
        if common_fields:
            background_score = (len(common_fields) / len(required_background)) * 15
            score += min(15, background_score)
    else:
        # Background gereksinimi yoksa tam puan
        score += 15
    
    # 4. Research experience (10 points)
    research_exp = user_data.get('research_experience', 0)
    if research_exp >= 2:
        score += 10
    elif research_exp >= 1:
        score += 7
    elif research_exp >= 0.5:
        score += 4
    
    # 5. Work experience (8 points)
    if work_exp >= 10:
        score += 8  # 10+ yıl = tam puan
    elif work_exp >= 5:
        score += 6
    elif work_exp >= 2:
        score += 4
    elif work_exp >= 1:
        score += 2
    
    # 6. Yayınlar (5 puan)
    publications = user_data.get('publications', 0)
    if publications >= 5:
        score += 5
    elif publications >= 3:
        score += 3
    elif publications >= 1:
        score += 2
    
    # 7. Referans mektupları (5 puan)
    rec_letters = user_data.get('recommendation_letters', 0)
    if rec_letters >= 3:
        score += 5
    elif rec_letters >= 2:
        score += 3
    elif rec_letters >= 1:
        score += 2
    
    # 8. GRE/GMAT (3 puan)
    gre_score = user_data.get('gre_score')
    gmat_score = user_data.get('gmat_score')
    if gre_score and gre_score >= 320:
        score += 3
    elif gre_score and gre_score >= 310:
        score += 2
    elif gre_score and gre_score >= 300:
        score += 1
    if gmat_score and gmat_score >= 700:
        score += 3
    elif gmat_score and gmat_score >= 650:
        score += 2
    elif gmat_score and gmat_score >= 600:
        score += 1
    
    # Ek puanlar (bonus - maksimum 10 puan ekstra)
    bonus_points = calculate_bonus_points(user_data)
    score += bonus_points * 10  # 0.1 ek puan = 1 puan bonus
    
    # Maksimum 110 puan olabilir (100 + 10 bonus)
    return round(min(score, 110.0), 2)

def extract_text_from_pdf(file_content):
    """PDF'den text çıkar"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"PDF parsing error: {e}")
        return None

def extract_text_from_docx(file_content):
    """DOCX'den text çıkar"""
    try:
        doc_file = io.BytesIO(file_content)
        doc = Document(doc_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"DOCX parsing error: {e}")
        return None

def parse_cv_content(text):
    """
    CV text'inden bilgileri çıkar.
    
    Synonym mapping kullanarak becerileri normalize eder:
    - "JS" -> "javascript"
    - "Node" -> "node.js"
    - "React.js" -> "react"
    """
    if not text:
        return {}
    
    text_lower = text.lower()
    extracted_data = {}
    
    # ===== SKILL EXTRACTION WITH SYNONYM MAPPING =====
    skills_data = extract_skills_from_cv(text)
    extracted_data['skills'] = skills_data['normalized_skills']
    extracted_data['raw_skills'] = skills_data['raw_skills']
    extracted_data['skill_categories'] = skills_data['skill_categories']
    
    # GPA extraction - daha kapsamlı pattern'ler
    gpa_patterns = [
        r'gpa[:\s]*([0-9]+\.[0-9]+)',
        r'grade point average[:\s]*([0-9]+\.[0-9]+)',
        r'not ortalaması[:\s]*([0-9]+\.[0-9]+)',
        r'not[:\s]*([0-9]+\.[0-9]+)',
        r'([0-9]\.[0-9]+)\s*/\s*4\.0',
        r'([0-9]\.[0-9]+)\s*out of\s*4\.0',
        r'([0-9]\.[0-9]+)\s*\(4\.0',
        r'cgpa[:\s]*([0-9]+\.[0-9]+)',
        r'cumulative gpa[:\s]*([0-9]+\.[0-9]+)'
    ]
    for pattern in gpa_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                gpa = float(match.group(1))
                if 0 <= gpa <= 4.0:
                    extracted_data['gpa'] = gpa
                    break
            except:
                continue
    
    # Language scores - daha kapsamlı pattern'ler
    toefl_patterns = [
        r'toefl[:\s]*(\d{2,3})',
        r'toefl ibt[:\s]*(\d{2,3})',
        r'toefl.*?(\d{2,3})',
        r'(\d{2,3})\s*toefl'
    ]
    for pattern in toefl_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                score = int(match.group(1))
                if 0 <= score <= 120:
                    extracted_data['language_test_type'] = 'toefl'
                    extracted_data['language_test_score'] = score
                    break
            except:
                continue
    
    ielts_patterns = [
        r'ielts[:\s]*(\d\.\d)',
        r'ielts academic[:\s]*(\d\.\d)',
        r'ielts.*?(\d\.\d)',
        r'(\d\.\d)\s*ielts'
    ]
    for pattern in ielts_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                score = float(match.group(1))
                if 0 <= score <= 9:
                    extracted_data['language_test_type'] = 'ielts'
                    extracted_data['language_test_score'] = score
                    break
            except:
                continue
    
    yds_patterns = [
        r'yds[:\s]*(\d{2,3})',
        r'eyds[:\s]*(\d{2,3})',
        r'yökdil[:\s]*(\d{2,3})',
        r'e-yökdil[:\s]*(\d{2,3})'
    ]
    for pattern in yds_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                score = int(match.group(1))
                if 0 <= score <= 100:
                    extracted_data['language_test_type'] = 'yds'
                    extracted_data['language_test_score'] = score
                    break
            except:
                continue
    
    # Background fields extraction - daha kapsamlı
    background_keywords = {
        'computer science': ['computer science', 'cs', 'bilgisayar', 'bilgisayar bilimi', 'computer engineering'],
        'engineering': ['engineering', 'mühendislik', 'engineer'],
        'robotics': ['robotics', 'robotik', 'robot'],
        'data science': ['data science', 'veri bilimi', 'data scientist', 'machine learning', 'ml'],
        'mechanical engineering': ['mechanical engineering', 'makine mühendisliği', 'mechanical'],
        'electrical engineering': ['electrical engineering', 'elektrik mühendisliği', 'electrical', 'ee'],
        'mathematics': ['mathematics', 'matematik', 'math', 'applied math'],
        'physics': ['physics', 'fizik'],
        'software engineering': ['software engineering', 'yazılım mühendisliği', 'software'],
        'artificial intelligence': ['artificial intelligence', 'ai', 'yapay zeka'],
        'control systems': ['control systems', 'kontrol sistemleri', 'control engineering'],
        'statistics': ['statistics', 'istatistik']
    }
    
    found_backgrounds = []
    for field, keywords in background_keywords.items():
        for keyword in keywords:
            # Kelime sınırları ile arama (tam kelime eşleşmesi)
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                found_backgrounds.append(field)
                break
    
    if found_backgrounds:
        extracted_data['background'] = list(set(found_backgrounds))
    
    # Research experience - daha esnek pattern'ler
    research_patterns = [
        r'research[:\s]*(\d+\.?\d*)\s*(?:year|yıl|yr)',
        r'araştırma[:\s]*(\d+\.?\d*)\s*(?:year|yıl|yr)',
        r'(\d+\.?\d*)\s*(?:year|yıl|yr).*research',
        r'research assistant[:\s]*(\d+\.?\d*)',
        r'ra[:\s]*(\d+\.?\d*)'
    ]
    for pattern in research_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                extracted_data['research_experience'] = float(match.group(1))
                break
            except:
                continue
    
    # Work experience - daha esnek pattern'ler
    work_patterns = [
        r'work experience[:\s]*(\d+\.?\d*)\s*(?:year|yıl|yr)',
        r'experience[:\s]*(\d+\.?\d*)\s*(?:year|yıl|yr)',
        r'(\d+\.?\d*)\s*(?:year|yıl|yr).*experience',
        r'(\d+)\s*(?:year|yıl|yr).*work',
        r'professional experience[:\s]*(\d+\.?\d*)',
        r'employment[:\s]*(\d+\.?\d*)'
    ]
    for pattern in work_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            try:
                extracted_data['work_experience'] = float(match.group(1))
                break
            except:
                continue
    
    # Publications
    pub_patterns = [
        r'(\d+)\s*(?:publication|yayın|paper|makale)',
        r'publication[:\s]+(\d+)',
        r'(\d+)\s*published'
    ]
    for pattern in pub_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            extracted_data['publications'] = int(match.group(1))
            break
    
    # Country detection
    if 'türkiye' in text_lower or 'turkey' in text_lower:
        extracted_data['country'] = 'turkey'
    elif 'usa' in text_lower or 'united states' in text_lower:
        extracted_data['country'] = 'usa'
    elif 'germany' in text_lower or 'almanya' in text_lower:
        extracted_data['country'] = 'germany'
    elif 'france' in text_lower or 'fransa' in text_lower:
        extracted_data['country'] = 'france'
    elif 'uk' in text_lower or 'united kingdom' in text_lower:
        extracted_data['country'] = 'uk'
    
    # Default values
    if 'gpa' not in extracted_data:
        extracted_data['gpa'] = None
    if 'language_test_type' not in extracted_data:
        extracted_data['language_test_type'] = None
    if 'language_test_score' not in extracted_data:
        extracted_data['language_test_score'] = None
    if 'background' not in extracted_data:
        extracted_data['background'] = []
    if 'research_experience' not in extracted_data:
        extracted_data['research_experience'] = 0
    if 'work_experience' not in extracted_data:
        extracted_data['work_experience'] = 0
    if 'publications' not in extracted_data:
        extracted_data['publications'] = 0
    if 'country' not in extracted_data:
        extracted_data['country'] = 'turkey'
    
    extracted_data['grading_system'] = '4.0'
    extracted_data['language'] = 'english'
    
    return extracted_data

@app.route('/api/parse-cv', methods=['POST', 'OPTIONS'])
@rate_limit
def parse_cv():
    """CV dosyasını parse et ve bilgileri çıkar"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("📥 CV parse isteği alındı")
        print(f"Request files: {list(request.files.keys())}")
        print(f"Content-Type: {request.content_type}")
        
        if 'cv' not in request.files:
            print("❌ 'cv' key bulunamadı")
            return jsonify({
                "success": False,
                "error": "CV dosyası bulunamadı"
            }), 400
        
        file = request.files['cv']
        print(f"📄 Dosya alındı: {file.filename}, type: {file.content_type}, size: {len(file.read())}")
        
        # Dosyayı tekrar oku (read() dosyayı tüketir)
        file.seek(0)
        file_content = file.read()
        
        if file.filename == '' or len(file_content) == 0:
            print("❌ Dosya boş")
            return jsonify({
                "success": False,
                "error": "Dosya seçilmedi veya boş"
            }), 400
        
        # Dosya tipi kontrolü
        file_type = file.content_type
        print(f"📋 Dosya tipi: {file_type}")
        
        # Text extraction
        text = None
        if file_type == 'application/pdf':
            if not PDF_AVAILABLE:
                return jsonify({
                    "success": False,
                    "error": "PDF parsing kütüphanesi yüklü değil"
                }), 500
            text = extract_text_from_pdf(file_content)
        elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
            if not DOCX_AVAILABLE:
                return jsonify({
                    "success": False,
                    "error": "DOCX parsing kütüphanesi yüklü değil"
                }), 500
            text = extract_text_from_docx(file_content)
        else:
            return jsonify({
                "success": False,
                "error": "Desteklenmeyen dosya formatı. PDF veya DOCX yükleyin."
            }), 400
        
        if not text or len(text.strip()) < 50:
            return jsonify({
                "success": False,
                "error": "CV content could not be extracted or is too short. Please upload a valid CV."
            }), 400
        
        # CV içeriği validasyonu
        text_lower = text.lower()
        cv_keywords = ['education', 'experience', 'skill', 'university', 'gpa', 'grade', 'work', 'employment']
        found_keywords = [kw for kw in cv_keywords if kw in text_lower]
        
        if len(found_keywords) < 3:
            return jsonify({
                "success": False,
                "error": "Bu dosya bir CV gibi görünmüyor. Lütfen geçerli bir CV yükleyin."
            }), 400
        
        # Bilgileri çıkar
        print("🔍 CV içeriği parse ediliyor...")
        extracted_data = parse_cv_content(text)
        print(f"✅ Parse edilen veriler: {extracted_data}")
        
        return jsonify({
            "success": True,
            "extracted_text": text[:500],  # İlk 500 karakter (debug için)
            "extracted_data": extracted_data,
            "confidence": len(found_keywords) / len(cv_keywords)
        })
        
    except Exception as e:
        import traceback
        print(f"❌ CV parsing error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": f"CV analiz edilirken hata oluştu: {str(e)}"
        }), 500

@app.route('/api/feedback', methods=['POST'])
@rate_limit
def submit_feedback():
    """Kullanıcı geri bildirimini al ve email gönder"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        name = data.get('name', 'Anonymous')
        email = data.get('email', 'No email provided')
        message = data.get('message', '')
        feedback_type = data.get('type', 'general')
        user_info = {
            'language': data.get('language', 'Unknown'),
            'url': data.get('url', 'Unknown'),
            'userAgent': data.get('userAgent', 'Unknown')
        }
        
        if not message or len(message.strip()) < 10:
            return jsonify({
                "success": False,
                "error": "Message must be at least 10 characters"
            }), 400
        
        # Import email service
        try:
            from email_service import send_feedback_email
            email_sent = send_feedback_email(name, email, message, feedback_type, user_info)
            
            if email_sent:
                return jsonify({
                    "success": True,
                    "message": "Feedback sent successfully"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to send feedback email"
                }), 500
        except ImportError:
            # Email service not available, just log
            print(f"📧 Feedback received (email service not configured):")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Type: {feedback_type}")
            print(f"Message: {message}")
            
            return jsonify({
                "success": True,
                "message": "Feedback received (logged)"
            })
            
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        "name": "University Match AI API",
        "version": "2.0",
        "status": "running",
        "tiers": {
            "basic": "Free - Sınırsız eşleştirme, CV parsing",
            "premium": "$19/mo - AI Agent, Document Checklist, Deadline Tracking"
        },
        "features": {
            "skill_synonym_mapping": "JavaScript=JS=Node.js style normalization",
            "cv_parsing": "PDF and DOCX support with smart extraction",
            "university_matching": "Advanced scoring algorithm",
            "ai_agent": "Claude Opus 4.5 personal assistant (Premium)",
            "document_checklist": "Smart document tracking (Premium)",
            "deadline_tracking": "Never miss a deadline (Premium)"
        },
        "endpoints": {
            "core": {
                "health": "GET /api/health",
                "universities": "GET /api/universities",
                "match": "POST /api/match",
                "parse_cv": "POST /api/parse-cv"
            },
            "skills": {
                "normalize": "POST /api/skills/normalize",
                "extract": "POST /api/skills/extract",
                "synonyms": "GET /api/skills/synonyms"
            },
            "pricing": {
                "pricing": "GET /api/pricing - Full pricing page data",
                "tiers": "GET /api/pricing/tiers",
                "features": "GET /api/pricing/features",
                "user_tier": "GET /api/user/tier",
                "can_access": "GET /api/user/can-access/<feature_id>"
            },
            "premium": {
                "ai_chat": "POST /api/ai-agent/chat (Premium)",
                "ai_capabilities": "GET /api/ai-agent/capabilities"
            }
        },
        "documentation": "See README.md and SETUP_GUIDE.md",
        "web_app": "http://localhost:5173",
        "github": "https://github.com/tekesineren/university-match-ai"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """API sağlık kontrolü"""
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/api/skills/normalize', methods=['POST'])
def normalize_skills_endpoint():
    """
    Beceri listesini normalize et - Synonym mapping kullanarak standart forma getir.
    
    Request body:
    {
        "skills": ["JS", "Node", "React.js", "Python3"]
    }
    
    Response:
    {
        "success": true,
        "original": ["JS", "Node", "React.js", "Python3"],
        "normalized": ["javascript", "node.js", "react", "python"],
        "mapping": {
            "JS": "javascript",
            "Node": "node.js",
            "React.js": "react",
            "Python3": "python"
        }
    }
    """
    try:
        data = request.json
        skills = data.get('skills', [])
        
        if not skills:
            return jsonify({
                "success": False,
                "error": "skills listesi gerekli"
            }), 400
        
        normalized = []
        mapping = {}
        
        for skill in skills:
            norm = normalize_skill(skill)
            normalized.append(norm)
            mapping[skill] = norm
        
        return jsonify({
            "success": True,
            "original": skills,
            "normalized": list(set(normalized)),  # Unique değerler
            "mapping": mapping
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/skills/extract', methods=['POST'])
def extract_skills_endpoint():
    """
    Metin içinden becerileri çıkar ve kategorize et.
    
    Request body:
    {
        "text": "I have 5 years of experience with JavaScript, Node.js, and React..."
    }
    
    Response:
    {
        "success": true,
        "skills": {
            "raw_skills": ["JavaScript", "Node.js", "React"],
            "normalized_skills": ["javascript", "node.js", "react"],
            "skill_categories": {
                "programming_languages": ["javascript"],
                "frameworks": ["node.js", "react"],
                ...
            }
        }
    }
    """
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                "success": False,
                "error": "text gerekli"
            }), 400
        
        skills_data = extract_skills_from_cv(text)
        
        return jsonify({
            "success": True,
            "skills": skills_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/skills/synonyms', methods=['GET'])
def get_skill_synonyms():
    """
    Tüm skill synonym mapping'lerini döndür.
    
    Response:
    {
        "success": true,
        "synonyms": {
            "javascript": ["javascript", "js", "ecmascript", ...],
            "python": ["python", "py", "python3", ...],
            ...
        },
        "total_skills": 50,
        "total_synonyms": 200
    }
    """
    total_synonyms = sum(len(syns) for syns in SKILL_SYNONYMS.values())
    
    return jsonify({
        "success": True,
        "synonyms": SKILL_SYNONYMS,
        "total_skills": len(SKILL_SYNONYMS),
        "total_synonyms": total_synonyms
    })

@app.route('/api/user/stats', methods=['GET'])
def user_stats():
    """Kullanıcı istatistiklerini al"""
    user_id = get_user_id()
    stats = get_user_stats(user_id)
    if stats:
        return jsonify({"success": True, "stats": stats})
    return jsonify({"success": False, "error": "Kullanıcı bulunamadı"}), 404

@app.route('/api/user/upgrade', methods=['POST'])
def user_upgrade():
    """Kullanıcı tier'ını yükselt (Stripe webhook'tan çağrılacak)"""
    try:
        data = request.json
        user_id = data.get('user_id')
        tier = data.get('tier')
        stripe_customer_id = data.get('stripe_customer_id')
        subscription_id = data.get('subscription_id')
        
        if not user_id or not tier:
            return jsonify({"success": False, "error": "user_id ve tier gerekli"}), 400
        
        upgrade_user(user_id, tier, stripe_customer_id, subscription_id)
        return jsonify({"success": True, "message": f"Kullanıcı {tier} tier'a yükseltildi"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/api-key/create', methods=['POST'])
@require_tier('pro')
def create_api_key_endpoint():
    """API key oluştur (Pro tier için)"""
    try:
        user_id = get_user_id()
        key_name = request.json.get('key_name', 'default')
        
        api_key = create_api_key(user_id, key_name)
        return jsonify({
            "success": True,
            "api_key": api_key,
            "message": "API key oluşturuldu. Bu key'i güvenli bir yerde saklayın!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/checkout/create', methods=['POST'])
def create_checkout():
    """Stripe Checkout session oluştur"""
    try:
        data = request.json
        tier = data.get('tier')  # 'premium' veya 'pro'
        user_id = get_user_id()
        
        if tier not in ['premium', 'pro']:
            return jsonify({"success": False, "error": "Geçersiz tier"}), 400
        
        checkout_url, error = create_checkout_session(tier, user_id)
        if error:
            return jsonify({"success": False, "error": error}), 500
        
        return jsonify({
            "success": True,
            "checkout_url": checkout_url
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Stripe webhook endpoint"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    message, error = handle_stripe_webhook(payload, sig_header)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"status": "success", "message": message}), 200

@app.route('/api/universities', methods=['GET'])
def get_universities():
    """
    Tüm okulları listele.
    Query params:
        - include_expired: true/false (default: false)
        - country: Filter by country
    """
    include_expired = request.args.get('include_expired', 'false').lower() == 'true'
    country_filter = request.args.get('country', '').strip()
    
    universities_with_status = []
    expired_count = 0
    
    for university in UNIVERSITIES:
        # Country filter
        if country_filter and university.get('country', '').lower() != country_filter.lower():
            continue
        
        # Deadline kontrolü
        has_active, next_deadline, days_remaining = has_active_deadline(university)
        
        if not has_active and not include_expired:
            expired_count += 1
            continue
        
        uni_copy = university.copy()
        uni_copy['deadline_status'] = {
            'has_active': has_active,
            'next_deadline': next_deadline,
            'days_remaining': days_remaining,
            'urgency': 'critical' if days_remaining and days_remaining <= 7 else 
                      'warning' if days_remaining and days_remaining <= 30 else 'normal'
        }
        universities_with_status.append(uni_copy)
    
    return jsonify({
        "universities": universities_with_status,
        "total": len(universities_with_status),
        "expired_hidden": expired_count,
        "showing_active_only": not include_expired
    })

def has_active_deadline(university):
    """
    Üniversitenin aktif (geçmemiş) bir deadline'ı var mı kontrol et.
    
    Returns:
        tuple: (has_active, next_deadline_str, days_remaining)
    """
    deadlines = university.get('deadlines', {})
    if not deadlines:
        # Deadline bilgisi yoksa varsayılan olarak göster
        return True, None, None
    
    today = date.today()
    active_deadlines = []
    
    for term, deadline_str in deadlines.items():
        try:
            deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            if deadline_date >= today:
                days_remaining = (deadline_date - today).days
                active_deadlines.append({
                    'term': term,
                    'date': deadline_str,
                    'days_remaining': days_remaining
                })
        except (ValueError, TypeError):
            continue
    
    if active_deadlines:
        # En yakın deadline'ı döndür
        closest = min(active_deadlines, key=lambda x: x['days_remaining'])
        return True, closest['date'], closest['days_remaining']
    
    return False, None, None


@app.route('/api/match', methods=['POST'])
@rate_limit
def match_universities():
    """
    Kullanıcı verilerine göre okulları eşleştir ve sırala.
    Deadline'ı geçmiş üniversiteler otomatik filtrelenir.
    
    Request body:
    {
        "gpa": 3.8,
        "language_score": 110,
        "motivation_letter": "...",
        "background": ["engineering", "robotics"],
        "include_expired": false  // Opsiyonel: true ise geçmiş deadline'ları da göster
    }
    """
    try:
        user_data = request.json
        include_expired = user_data.get('include_expired', False)
        
        # Her okul için skor hesapla ve deadline kontrolü yap
        matched_universities = []
        expired_count = 0
        
        for university in UNIVERSITIES:
            # Deadline kontrolü
            has_active, next_deadline, days_remaining = has_active_deadline(university)
            
            if not has_active and not include_expired:
                expired_count += 1
                continue  # Geçmiş deadline'ları atla
            
            university_copy = university.copy()
            match_score = calculate_match_score(user_data, university)
            university_copy['match_score'] = match_score
            
            # Deadline bilgisini ekle
            university_copy['deadline_status'] = {
                'has_active': has_active,
                'next_deadline': next_deadline,
                'days_remaining': days_remaining,
                'urgency': 'critical' if days_remaining and days_remaining <= 7 else 
                          'warning' if days_remaining and days_remaining <= 30 else 'normal'
            }
            
            matched_universities.append(university_copy)
        
        # Sort by score (highest to lowest)
        matched_universities.sort(key=lambda x: x['match_score'], reverse=True)
        
        # High match (70+), medium (50-70), low (30-50), very low (<30)
        high_match = [u for u in matched_universities if u['match_score'] >= 70]
        medium_match = [u for u in matched_universities if 50 <= u['match_score'] < 70]
        low_match = [u for u in matched_universities if 30 <= u['match_score'] < 50]
        extra_options = [u for u in matched_universities if u['match_score'] < 30]
        
        return jsonify({
            "success": True,
            "results": {
                "high_match": high_match,
                "medium_match": medium_match,
                "low_match": low_match,
                "extra_options": extra_options
            },
            "user_data": user_data,
            "filtered_info": {
                "expired_universities_hidden": expired_count,
                "showing_active_deadlines_only": not include_expired,
                "tip": "Add 'include_expired': true to see all universities"
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# =============================================================================
# PRICING & PREMIUM ROUTES
# =============================================================================
try:
    from pricing import register_pricing_routes
    register_pricing_routes(app)
    print("✅ Pricing routes registered")
except ImportError as e:
    print(f"⚠️ Pricing module not loaded: {e}")

# =============================================================================
# TOKEN SYSTEM & AI AGENTS
# =============================================================================
try:
    from token_system import register_token_routes
    register_token_routes(app)
    print("✅ Token system routes registered")
except ImportError as e:
    print(f"⚠️ Token system not loaded: {e}")


if __name__ == '__main__':
    # Use PORT from environment (Replit sets this), default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # In deployment (when PORT is set), bind to 0.0.0.0
    # In development, bind to localhost only
    if os.environ.get('PORT'):
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
    
    # Debug mode enabled for development
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host=host, port=port)

