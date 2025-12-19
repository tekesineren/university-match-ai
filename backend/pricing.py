"""
Premium & Pricing System for University Match AI
Tiered access with AI Agent rental (Claude Opus 4.5)
"""

from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

# =============================================================================
# PRICING TIERS
# =============================================================================

PRICING_TIERS = {
    "basic": {
        "name": "Basic",
        "price": 0,
        "currency": "USD",
        "billing": "free",
        "tagline": "Ücretsiz başla, potansiyelini gör",
        "features": {
            # ✅ BASIC'TE VAR
            "university_matching": True,
            "match_limit": -1,  # ✅ SINIRSIZ - Tüm üniversiteleri görsünler!
            "matching_type": "algorithm",  # Algoritma bazlı eşleştirme
            "cv_parsing": True,  # CV yükleyip parse edebilsinler
            "skill_extraction": True,  # Skill synonym mapping
            "basic_results": True,  # Match skorları görsünler
            
            # ❌ BASIC'TE YOK - Premium için upgrade
            "document_checklist": False,
            "deadline_tracking": False,
            "ai_agent": False,
            "cv_review": False,
            "motivation_review": False,
            "email_reminders": False,
            "priority_support": False,
            "document_storage": False,
            "export_pdf": False,
            "ai_recommendations": False
        },
        "limits": {
            "matches_per_day": -1,  # Sınırsız match
            "cv_parses_per_day": 5  # Günde 5 CV parse
        },
        "badge": "🆓",
        "badge_text": "Free Forever",
        "cta": "Premium'a Geç",
        "value_props": [
            "✅ Sınırsız üniversite eşleştirmesi",
            "✅ CV parsing ve skill analizi",
            "✅ Match skorları ve sıralama",
            "❌ Belge takibi yok",
            "❌ AI asistan yok"
        ]
    },
    
    "premium": {
        "name": "Premium",
        "price": 19,
        "currency": "USD",
        "billing": "monthly",
        "tagline": "AI destekli tam başvuru deneyimi",
        "features": {
            # ✅ BASIC'TEKİ HER ŞEY
            "university_matching": True,
            "match_limit": -1,
            "matching_type": "ai_enhanced",  # AI destekli gelişmiş eşleştirme
            "cv_parsing": True,
            "skill_extraction": True,
            "basic_results": True,
            
            # ⭐ PREMIUM ÖZEL
            "document_checklist": True,  # Akıllı belge takibi
            "deadline_tracking": True,  # Deadline hatırlatıcı
            "ai_agent": True,  # Claude Opus 4.5 kişisel asistan
            "cv_review": True,  # AI CV analizi
            "motivation_review": True,  # AI motivation letter desteği
            "email_reminders": True,  # Email bildirimleri
            "priority_support": True,  # Öncelikli destek
            "document_storage": True,  # Belge saklama
            "export_pdf": True,  # PDF export
            "ai_recommendations": True  # Akıllı öneriler
        },
        "limits": {
            "matches_per_day": -1,
            "cv_parses_per_day": -1,
            "ai_agent_messages_per_day": 100,
            "document_storage_mb": 1000
        },
        "badge": "⭐",
        "badge_text": "Premium",
        "cta": "Premium Üyesin!",
        "ai_model": "claude-opus-4-20250514",
        "value_props": [
            "✅ Basic'teki her şey",
            "⭐ Akıllı belge takip sistemi",
            "⭐ Deadline hatırlatıcıları",
            "⭐ Claude Opus 4.5 AI Asistan",
            "⭐ CV & Motivation Letter analizi",
            "⭐ Belge saklama & PDF export"
        ],
        "highlight_features": ["ai_agent", "document_checklist", "deadline_tracking"]
    }
}

# =============================================================================
# PREMIUM FEATURES DETAIL
# =============================================================================

# Premium'da sunulan özellikler (Basic'te YOK)
PREMIUM_FEATURES = [
    {
        "id": "ai_agent",
        "name": "Kişisel AI Asistan",
        "description": "Claude Opus 4.5 - En güçlü AI modeliyle çalışan özel asistanınız",
        "icon": "🤖",
        "highlight": True,  # Ana özellik - en çok öne çıkar
        "badge": "🔥 En Popüler",
        "details": [
            "7/24 ulaşılabilir AI danışman",
            "Başvuru stratejisi oluşturma",
            "Motivation letter yazım desteği",
            "Interview hazırlık soruları",
            "Kişiselleştirilmiş program önerileri",
            "Anlık soru-cevap"
        ],
        "value_prop": "Bir danışmana ₺50,000+ ödemeyin, AI asistanınız her zaman yanınızda",
        "demo_available": True
    },
    {
        "id": "document_checklist",
        "name": "Akıllı Belge Takip Sistemi",
        "description": "Her üniversitenin istediği belgeleri tek yerden takip edin",
        "icon": "📋",
        "highlight": True,  # İkinci ana özellik
        "badge": "⏱️ Zaman Kazandırır",
        "details": [
            "Üniversiteye özel belge listesi",
            "Hangi format kabul ediliyor (PDF, DOCX...)",
            "Dosya boyutu kontrolü",
            "İlerleme takibi (%)",
            "Eksik belge uyarıları",
            "Belge yükleme ve saklama"
        ],
        "value_prop": "Saatler süren araştırmayı 30 saniyeye indirin",
        "demo_available": True
    },
    {
        "id": "deadline_tracking",
        "name": "Deadline Hatırlatıcı",
        "description": "Başvuru tarihlerini asla kaçırmayın",
        "icon": "⏰",
        "highlight": True,
        "badge": "📅 Asla Kaçırma",
        "details": [
            "Tüm başvuru deadlineları tek yerde",
            "Email ile otomatik hatırlatma",
            "7 gün / 3 gün / 1 gün kala uyarı",
            "Google Calendar entegrasyonu",
            "Renk kodlu aciliyet gösterimi"
        ],
        "value_prop": "Deadline kaçırma stresine son verin",
        "demo_available": False
    },
    {
        "id": "cv_review",
        "name": "AI CV Analizi",
        "description": "CV'nizi AI ile analiz edin ve güçlendirin",
        "icon": "📄",
        "highlight": False,
        "details": [
            "Eksik bölüm tespiti",
            "ATS (Applicant Tracking System) uyumluluk",
            "Anahtar kelime optimizasyonu",
            "Program bazlı öneriler",
            "Rakip CV'lerle karşılaştırma"
        ],
        "value_prop": "CV'nizi profesyonel danışman seviyesine çıkarın"
    },
    {
        "id": "motivation_review",
        "name": "Motivation Letter Analizi",
        "description": "Etkileyici motivation letter yazmanıza yardımcı olur",
        "icon": "✍️",
        "highlight": False,
        "details": [
            "Yapı ve akış analizi",
            "Üniversiteye özelleştirme önerileri",
            "Güçlü ve zayıf yön tespiti",
            "Kelime sayısı ve ton kontrolü",
            "Başarılı örneklerle karşılaştırma"
        ],
        "value_prop": "İlk paragraftan etkileyici ol"
    },
    {
        "id": "document_storage",
        "name": "Güvenli Belge Saklama",
        "description": "Tüm belgelerinizi güvenle saklayın ve yönetin",
        "icon": "🔐",
        "highlight": False,
        "details": [
            "1GB güvenli depolama",
            "Şifrelenmiş dosya saklama",
            "Tek tıkla erişim",
            "Birden fazla başvuruda kullanım",
            "PDF olarak toplu indirme"
        ],
        "value_prop": "Belgeleriniz her zaman elinizin altında"
    }
]

# Basic'te ZATEN var olan özellikler (free)
BASIC_FEATURES = [
    {
        "id": "unlimited_matching",
        "name": "Sınırsız Üniversite Eşleştirmesi",
        "description": "Tüm üniversite eşleştirmelerini ücretsiz gör",
        "icon": "🎯",
        "included": True
    },
    {
        "id": "cv_parsing",
        "name": "CV Parsing",
        "description": "CV'ni yükle, bilgilerin otomatik çıkarılsın",
        "icon": "📄",
        "included": True
    },
    {
        "id": "skill_mapping",
        "name": "Akıllı Skill Eşleştirmesi",
        "description": "JS=JavaScript gibi synonym mapping",
        "icon": "🔗",
        "included": True
    },
    {
        "id": "match_scores",
        "name": "Eşleşme Skorları",
        "description": "Her üniversite için detaylı skor analizi",
        "icon": "📊",
        "included": True
    }
]

# =============================================================================
# AI AGENT PROMPTS (Claude Opus 4.5)
# =============================================================================

AI_AGENT_SYSTEM_PROMPT = """Sen University Match AI'ın Premium AI Asistanısın. 
Claude Opus 4.5 modeliyle çalışıyorsun - en gelişmiş AI danışman.

GÖREVLER:
1. Öğrencilere yüksek lisans başvuru sürecinde yardım et
2. Motivation letter yazımında destek ol
3. CV optimizasyonu öner
4. Interview hazırlığı yap
5. Üniversite seçimi konusunda stratejik tavsiyeler ver

YAKLAŞIM:
- Profesyonel ama samimi ol
- Somut, uygulanabilir öneriler ver
- Öğrencinin stresini azalt
- Başarı hikayeleri paylaş
- Her zaman pozitif ama gerçekçi ol

ÖNEMLİ: Premium kullanıcıyla konuşuyorsun. Onlara özel, kişiselleştirilmiş deneyim sun.
"""

AI_AGENT_CAPABILITIES = [
    {
        "id": "strategy",
        "name": "Başvuru Stratejisi",
        "prompt_prefix": "Başvuru stratejisi oluştur: ",
        "examples": [
            "Hangi üniversitelere başvurmalıyım?",
            "Benim profilimle en uygun programlar hangileri?",
            "Safe/Match/Reach okul dağılımım nasıl olmalı?"
        ]
    },
    {
        "id": "motivation",
        "name": "Motivation Letter",
        "prompt_prefix": "Motivation letter için yardım et: ",
        "examples": [
            "MIT için motivation letter nasıl yazmalıyım?",
            "Opening paragraph önerisi",
            "Bu taslağı değerlendir..."
        ]
    },
    {
        "id": "cv",
        "name": "CV Optimizasyonu",
        "prompt_prefix": "CV optimizasyonu için: ",
        "examples": [
            "CV'mde eksik ne var?",
            "Proje deneyimimi nasıl anlatmalıyım?",
            "Akademik CV mi profesyonel CV mi?"
        ]
    },
    {
        "id": "interview",
        "name": "Interview Prep",
        "prompt_prefix": "Interview hazırlığı: ",
        "examples": [
            "En sık sorulan sorular neler?",
            "'Why this program' sorusuna nasıl cevap vereyim?",
            "Teknik interview için hazırlık"
        ]
    },
    {
        "id": "general",
        "name": "Genel Danışmanlık",
        "prompt_prefix": "",
        "examples": [
            "Vize süreci nasıl işliyor?",
            "Burs imkanları neler?",
            "Ne zaman başvurmalıyım?"
        ]
    }
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_user_tier(user_id):
    """Kullanıcının tier'ını al (veritabanından)"""
    # TODO: Gerçek veritabanı entegrasyonu
    # Şimdilik mock
    return "basic"

def check_feature_access(user_tier, feature_id):
    """Kullanıcının bir özelliğe erişimi var mı?"""
    tier_config = PRICING_TIERS.get(user_tier, PRICING_TIERS["basic"])
    features = tier_config.get("features", {})
    return features.get(feature_id, False)

def get_remaining_limit(user_id, limit_type):
    """Kullanıcının kalan limitini al"""
    # TODO: Gerçek limit tracking
    tier = get_user_tier(user_id)
    tier_config = PRICING_TIERS.get(tier, PRICING_TIERS["basic"])
    limits = tier_config.get("limits", {})
    max_limit = limits.get(limit_type, 0)
    
    if max_limit == -1:
        return {"unlimited": True, "remaining": -1}
    
    # Mock: Günlük kullanımı takip et
    used_today = 0  # TODO: Redis veya DB'den al
    remaining = max(0, max_limit - used_today)
    
    return {
        "unlimited": False,
        "max": max_limit,
        "used": used_today,
        "remaining": remaining
    }

def require_premium(feature_id):
    """Premium feature için decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: Gerçek auth'dan user_id al
            user_id = request.headers.get('X-User-ID', 'anonymous')
            user_tier = get_user_tier(user_id)
            
            if not check_feature_access(user_tier, feature_id):
                return jsonify({
                    "success": False,
                    "error": "premium_required",
                    "message": f"Bu özellik Premium üyelik gerektirir",
                    "feature": feature_id,
                    "upgrade_url": "/pricing",
                    "current_tier": user_tier
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================================================
# PRICING PAGE DATA
# =============================================================================

def get_pricing_page_data():
    """Pricing sayfası için tüm data"""
    return {
        "tiers": PRICING_TIERS,
        "features": PREMIUM_FEATURES,
        "ai_agent": {
            "model": "Claude Opus 4.5",
            "capabilities": AI_AGENT_CAPABILITIES,
            "highlight": "En gelişmiş AI modeli ile kişisel danışmanlık"
        },
        "social_proof": {
            "users": "2,500+",
            "universities": "20+",
            "success_rate": "89%",
            "testimonials": [
                {
                    "name": "Ahmet Y.",
                    "university": "ETH Zurich",
                    "quote": "AI asistan sayesinde motivation letter'ımı 3 günde tamamladım!",
                    "image": None
                },
                {
                    "name": "Elif K.",
                    "university": "MIT",
                    "quote": "Document checklist olmasaydı kesin bir şeyi unutacaktım",
                    "image": None
                }
            ]
        },
        "guarantee": {
            "type": "money_back",
            "days": 7,
            "text": "7 gün içinde memnun kalmazsanız paranızı iade ediyoruz"
        },
        "urgency": {
            "active": True,
            "message": "🔥 Şu an %30 indirim - Bu ay sonuna kadar",
            "original_price": 29,
            "discount_price": 19
        }
    }

def get_upgrade_prompt(user_tier, triggered_by):
    """Kullanıcıya upgrade prompt'u göster"""
    if user_tier == "premium":
        return None
    
    prompts = {
        "document_checklist": {
            "title": "📋 Hangi belgeler gerekli bilmek ister misin?",
            "message": "Premium ile her üniversitenin istediği belgeleri gör, takip et",
            "cta": "Belge Takibini Aç",
            "highlight_feature": "document_checklist",
            "urgency": "Başvuru sürecini 10x hızlandır"
        },
        "ai_help": {
            "title": "🤖 AI Asistan ile çalışmak ister misin?",
            "message": "Claude Opus 4.5 - En gelişmiş AI ile kişisel danışmanlık",
            "cta": "AI Asistanı Dene",
            "highlight_feature": "ai_agent",
            "urgency": "Danışmanlık masrafından ₺50,000+ tasarruf"
        },
        "deadline": {
            "title": "⏰ Deadline'ları takip etmek zor mu?",
            "message": "Premium ile otomatik hatırlatmalar al",
            "cta": "Asla Kaçırma",
            "highlight_feature": "deadline_tracking",
            "urgency": "Email ile otomatik hatırlatma"
        },
        "cv_review": {
            "title": "📄 CV'ni güçlendirmek ister misin?",
            "message": "AI analizi ile CV'ni optimize et",
            "cta": "CV Analizi Yap",
            "highlight_feature": "cv_review",
            "urgency": "ATS uyumlu CV = Daha yüksek şans"
        },
        "motivation": {
            "title": "✍️ Motivation letter'da takıldın mı?",
            "message": "AI desteği ile etkileyici letter yaz",
            "cta": "Yardım Al",
            "highlight_feature": "motivation_review",
            "urgency": "İlk paragraf her şeyi belirler"
        }
    }
    
    return prompts.get(triggered_by, prompts["ai_help"])


# =============================================================================
# FLASK API ENDPOINTS (app.py'ye import edilecek)
# =============================================================================

def register_pricing_routes(app):
    """Pricing route'larını Flask app'e kaydet"""
    
    @app.route('/api/pricing', methods=['GET'])
    def get_pricing():
        """Pricing sayfası için tüm bilgileri döndür"""
        return jsonify({
            "success": True,
            "data": get_pricing_page_data()
        })
    
    @app.route('/api/pricing/tiers', methods=['GET'])
    def get_tiers():
        """Sadece tier bilgilerini döndür"""
        return jsonify({
            "success": True,
            "tiers": PRICING_TIERS
        })
    
    @app.route('/api/pricing/features', methods=['GET'])
    def get_features():
        """Premium ve Basic özellikleri döndür"""
        return jsonify({
            "success": True,
            "premium_features": PREMIUM_FEATURES,
            "basic_features": BASIC_FEATURES
        })
    
    @app.route('/api/user/tier', methods=['GET'])
    def get_user_tier_endpoint():
        """Kullanıcının mevcut tier'ını döndür"""
        user_id = request.headers.get('X-User-ID', 'anonymous')
        tier = get_user_tier(user_id)
        tier_config = PRICING_TIERS.get(tier, PRICING_TIERS["basic"])
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "tier": tier,
            "tier_name": tier_config["name"],
            "badge": tier_config["badge"],
            "features": tier_config["features"],
            "limits": tier_config.get("limits", {}),
            "upgrade_available": tier != "premium"
        })
    
    @app.route('/api/user/can-access/<feature_id>', methods=['GET'])
    def check_access(feature_id):
        """Kullanıcının bir özelliğe erişimi var mı kontrol et"""
        user_id = request.headers.get('X-User-ID', 'anonymous')
        tier = get_user_tier(user_id)
        has_access = check_feature_access(tier, feature_id)
        
        response = {
            "success": True,
            "feature": feature_id,
            "has_access": has_access,
            "user_tier": tier
        }
        
        if not has_access:
            response["upgrade_prompt"] = get_upgrade_prompt(tier, feature_id)
            response["upgrade_url"] = "/pricing"
        
        return jsonify(response)
    
    @app.route('/api/upgrade/prompt', methods=['POST'])
    def trigger_upgrade_prompt():
        """Belirli bir context için upgrade prompt'u döndür"""
        data = request.json or {}
        triggered_by = data.get('triggered_by', 'ai_help')
        user_id = request.headers.get('X-User-ID', 'anonymous')
        tier = get_user_tier(user_id)
        
        prompt = get_upgrade_prompt(tier, triggered_by)
        
        if not prompt:
            return jsonify({
                "success": True,
                "show_prompt": False,
                "message": "Already premium"
            })
        
        return jsonify({
            "success": True,
            "show_prompt": True,
            "prompt": prompt,
            "pricing_url": "/pricing"
        })
    
    @app.route('/api/ai-agent/chat', methods=['POST'])
    @require_premium('ai_agent')
    def ai_agent_chat():
        """Premium AI Agent ile sohbet (Claude Opus 4.5)"""
        data = request.json
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        capability = data.get('capability', 'general')
        
        if not message:
            return jsonify({"success": False, "error": "Message required"}), 400
        
        # Capability'ye göre prompt prefix ekle
        cap_config = next((c for c in AI_AGENT_CAPABILITIES if c['id'] == capability), None)
        if cap_config:
            message = cap_config.get('prompt_prefix', '') + message
        
        # TODO: Gerçek Claude API çağrısı
        # Şimdilik mock response
        return jsonify({
            "success": True,
            "response": {
                "message": f"[AI Agent Demo] Mesajınız alındı: '{message[:50]}...' - Gerçek implementasyon için Claude API entegrasyonu gerekli.",
                "capability": capability,
                "model": "claude-opus-4-20250514"
            },
            "usage": {
                "messages_today": 5,
                "limit": 100,
                "remaining": 95
            }
        })
    
    @app.route('/api/ai-agent/capabilities', methods=['GET'])
    def get_ai_capabilities():
        """AI Agent'ın yapabileceklerini listele"""
        return jsonify({
            "success": True,
            "capabilities": AI_AGENT_CAPABILITIES,
            "model": "Claude Opus 4.5",
            "description": "En gelişmiş AI modeli ile kişisel danışmanlık"
        })

