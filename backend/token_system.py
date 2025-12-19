"""
Token-Based AI Agent System
- Token bazlı kullanım ve fiyatlandırma
- Anthropic maliyeti + %33 margin
- Gerçek zamanlı kullanım takibi
- Motivation Letter Agent ve diğer özel agentlar
"""

from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os
import json

# =============================================================================
# ANTHROPIC PRICING (Aralık 2024 - Güncel)
# =============================================================================
# https://www.anthropic.com/pricing

ANTHROPIC_PRICING = {
    # Claude 3.5 Sonnet (hızlı, uygun maliyetli)
    "claude-3-5-sonnet-20241022": {
        "input_per_1m": 3.00,   # $3.00 per 1M input tokens
        "output_per_1m": 15.00,  # $15.00 per 1M output tokens
        "name": "Claude 3.5 Sonnet",
        "description": "Hızlı ve akıllı - Günlük kullanım için ideal",
        "tier": "standard"
    },
    # Claude 3.5 Haiku (en hızlı, en ucuz)
    "claude-3-5-haiku-20241022": {
        "input_per_1m": 1.00,   # $1.00 per 1M input tokens
        "output_per_1m": 5.00,   # $5.00 per 1M output tokens
        "name": "Claude 3.5 Haiku",
        "description": "En hızlı - Basit görevler için",
        "tier": "fast"
    },
    # Claude 3 Opus (en güçlü)
    "claude-3-opus-20240229": {
        "input_per_1m": 15.00,  # $15.00 per 1M input tokens
        "output_per_1m": 75.00,  # $75.00 per 1M output tokens
        "name": "Claude 3 Opus",
        "description": "En güçlü - Karmaşık görevler için",
        "tier": "premium"
    },
    # Claude Opus 4 (en yeni, en güçlü) - yaklaşık fiyat
    "claude-opus-4-20250514": {
        "input_per_1m": 15.00,
        "output_per_1m": 75.00,
        "name": "Claude Opus 4.5",
        "description": "En gelişmiş AI - Premium exclusive",
        "tier": "premium"
    }
}

# =============================================================================
# OUR PRICING (Anthropic + %33 Margin)
# =============================================================================

MARGIN_PERCENTAGE = 0.33  # %33 kar marjı

def calculate_our_pricing():
    """Anthropic fiyatının üzerine %33 margin ekle"""
    our_pricing = {}
    for model_id, anthropic_price in ANTHROPIC_PRICING.items():
        our_pricing[model_id] = {
            "input_per_1m": round(anthropic_price["input_per_1m"] * (1 + MARGIN_PERCENTAGE), 2),
            "output_per_1m": round(anthropic_price["output_per_1m"] * (1 + MARGIN_PERCENTAGE), 2),
            "name": anthropic_price["name"],
            "description": anthropic_price["description"],
            "tier": anthropic_price["tier"],
            # Kullanıcıya gösterilecek basit fiyat
            "display_price": f"${round(anthropic_price['output_per_1m'] * (1 + MARGIN_PERCENTAGE) / 1000, 4)}/1K tokens"
        }
    return our_pricing

OUR_PRICING = calculate_our_pricing()

# =============================================================================
# TOKEN PACKAGES (Kullanıcıların satın alabileceği paketler)
# =============================================================================

TOKEN_PACKAGES = {
    "starter": {
        "id": "starter",
        "name": "Starter Pack",
        "tokens": 50_000,  # 50K tokens
        "price": 5.00,  # $5
        "price_per_1k": 0.10,
        "description": "İlk deneme için ideal",
        "badge": "🎯",
        "popular": False,
        "bonus_tokens": 0
    },
    "standard": {
        "id": "standard", 
        "name": "Standard Pack",
        "tokens": 200_000,  # 200K tokens
        "price": 15.00,  # $15
        "price_per_1k": 0.075,
        "description": "Bir başvuru sezonu için",
        "badge": "⭐",
        "popular": True,
        "bonus_tokens": 20_000,  # +20K bonus
        "savings": "25% tasarruf"
    },
    "pro": {
        "id": "pro",
        "name": "Pro Pack",
        "tokens": 500_000,  # 500K tokens
        "price": 30.00,  # $30
        "price_per_1k": 0.06,
        "description": "Ciddi başvuru yapanlar için",
        "badge": "🚀",
        "popular": False,
        "bonus_tokens": 100_000,  # +100K bonus
        "savings": "40% tasarruf"
    },
    "unlimited_monthly": {
        "id": "unlimited_monthly",
        "name": "Unlimited Monthly",
        "tokens": -1,  # Sınırsız
        "price": 49.00,  # $49/ay
        "price_per_1k": 0,
        "description": "Sınırsız kullanım (fair use)",
        "badge": "♾️",
        "popular": False,
        "bonus_tokens": 0,
        "fair_use_limit": 2_000_000,  # 2M/ay soft limit
        "billing": "monthly"
    }
}

# =============================================================================
# AGENT DEFINITIONS (Özelleşmiş AI Agentlar)
# =============================================================================

AGENTS = {
    "motivation_letter": {
        "id": "motivation_letter",
        "name": "Motivation Letter Agent",
        "icon": "✍️",
        "description": "Etkileyici motivation letter yazmanıza yardımcı olur",
        "model": "claude-3-5-sonnet-20241022",  # Maliyet/performans dengesi
        "system_prompt": """Sen bir yüksek lisans başvuru uzmanısın. Öğrencilere motivation letter (statement of purpose) yazma konusunda yardım ediyorsun.

GÖREVLER:
1. Motivation letter yapısı oluşturma
2. Açılış paragrafı yazma
3. Deneyim ve motivasyonu bağlama
4. Üniversiteye özel kişiselleştirme
5. Kapanış ve gelecek hedefleri

YAPISAL KURALLAR:
- 500-1000 kelime arası
- 4-5 paragraf: Hook, Background, Why This Program, Goals, Closing
- Spesifik ol, genel cümlelerden kaçın
- "Passion" kelimesini aşırı kullanma
- Üniversite ve program adını doğru yaz

YAKLAŞIM:
- Öğrencinin güçlü yönlerini öne çıkar
- Zayıf noktaları pozitife çevir
- Her üniversite için farklılaştır
- Somut örnekler kullan
- Akademik ton ama samimi

ÖNEMLİ: Token kullanımını optimize et. Gereksiz uzatma, özlü ve etkili ol.""",
        "capabilities": [
            "Sıfırdan motivation letter yazma",
            "Mevcut taslağı geliştirme",
            "Üniversiteye özelleştirme",
            "Paragraf paragraf feedback",
            "Hook/opening önerileri"
        ],
        "example_prompts": [
            "MIT Computer Science için motivation letter yaz",
            "Bu taslağımı değerlendir: [taslak]",
            "ETH Zurich Robotics programına özel paragraf ekle",
            "Opening paragraph için 3 farklı hook öner"
        ],
        "avg_tokens_per_task": {
            "full_letter": 2500,
            "review": 1500,
            "paragraph": 800,
            "suggestions": 500
        },
        "premium_only": True
    },
    
    "cv_optimizer": {
        "id": "cv_optimizer",
        "name": "CV Optimizer Agent",
        "icon": "📄",
        "description": "CV'nizi ATS uyumlu ve etkili hale getirir",
        "model": "claude-3-5-sonnet-20241022",
        "system_prompt": """Sen bir CV optimizasyon uzmanısın. Akademik ve profesyonel CV'leri yüksek lisans başvuruları için optimize ediyorsun.

GÖREVLER:
1. CV yapısı analizi
2. Eksik bölüm tespiti
3. ATS (Applicant Tracking System) uyumluluk
4. Anahtar kelime optimizasyonu
5. Bullet point geliştirme

AKADEMİK CV YAPISI:
- Contact Info
- Education (GPA dahil)
- Research Experience
- Publications/Projects
- Skills (Technical + Soft)
- Awards/Honors
- Extracurricular

KURALLAR:
- Action verb ile başla (Led, Developed, Implemented)
- Sayısal sonuçlar ekle (%20 improvement gibi)
- Tutarlı format
- 1-2 sayfa (Master's için 1 sayfa ideal)
- Fotoğraf gerekliliği ülkeye göre

Token optimize et. Kısa, actionable feedback ver.""",
        "capabilities": [
            "CV analizi ve scoring",
            "ATS uyumluluk kontrolü",
            "Bullet point geliştirme",
            "Eksik bölüm önerileri",
            "Sektör/program özelleştirme"
        ],
        "avg_tokens_per_task": {
            "full_review": 2000,
            "section_review": 800,
            "bullet_improve": 400
        },
        "premium_only": True
    },
    
    "interview_prep": {
        "id": "interview_prep",
        "name": "Interview Prep Agent",
        "icon": "🎤",
        "description": "Mülakata hazırlanmanıza yardımcı olur",
        "model": "claude-3-5-haiku-20241022",  # Hızlı cevaplar için
        "system_prompt": """Sen bir mülakat koçusun. Öğrencileri yüksek lisans programı mülakatlarına hazırlıyorsun.

GÖREVLER:
1. Sık sorulan sorular ve cevap stratejileri
2. "Tell me about yourself" hazırlığı
3. "Why this program" cevabı
4. Teknik sorular (program bazlı)
5. Mock interview pratiği

MÜLAKAT TÜRLERİ:
- Akademik mülakat (profesör ile)
- Admissions committee
- Teknik mülakat (CS/Engineering)
- Motivasyon odaklı

CEVAP YAPISI (STAR):
- Situation: Bağlam ver
- Task: Görevin ne idi
- Action: Ne yaptın
- Result: Sonuç ne oldu

Kısa, pratik cevaplar ver. Her soru için 2-3 dakikalık cevap hedefle.""",
        "capabilities": [
            "Sık sorulan sorular listesi",
            "STAR metodu ile cevap hazırlama",
            "Mock interview",
            "Teknik soru pratiği",
            "Body language/presentation tips"
        ],
        "avg_tokens_per_task": {
            "question_prep": 600,
            "mock_interview": 1500,
            "feedback": 400
        },
        "premium_only": True
    },
    
    "application_strategist": {
        "id": "application_strategist",
        "name": "Application Strategist",
        "icon": "🎯",
        "description": "Başvuru stratejinizi oluşturur",
        "model": "claude-3-5-sonnet-20241022",
        "system_prompt": """Sen bir yüksek lisans başvuru stratejistisin. Öğrencilere hangi okullara başvuracaklarını ve nasıl bir strateji izleyeceklerini söylüyorsun.

GÖREVLER:
1. Profil analizi
2. Safe/Match/Reach okul dağılımı
3. Program seçimi
4. Timeline oluşturma
5. Burs stratejisi

STRATEJİ PRENSİPLERİ:
- 8-12 okul başvurusu ideal
- 2-3 Safe (kabul olasılığı >70%)
- 4-5 Match (kabul olasılığı 40-70%)
- 2-3 Reach (kabul olasılığı <40%)

DEĞERLENDİRME KRİTERLERİ:
- GPA ve sınıf sıralaması
- Dil puanı (TOEFL/IELTS)
- Araştırma deneyimi
- İş deneyimi
- Yayınlar
- Referans mektupları kalitesi

Somut, uygulanabilir öneriler ver.""",
        "capabilities": [
            "Profil değerlendirme",
            "Okul listesi oluşturma",
            "Timeline planlama",
            "Burs fırsatları",
            "Plan B stratejisi"
        ],
        "avg_tokens_per_task": {
            "full_strategy": 3000,
            "school_recommendation": 1000,
            "timeline": 800
        },
        "premium_only": True
    },
    
    "general_advisor": {
        "id": "general_advisor",
        "name": "General Advisor",
        "icon": "💬",
        "description": "Genel sorularınızı yanıtlar",
        "model": "claude-3-5-haiku-20241022",  # Ucuz, hızlı
        "system_prompt": """Sen bir yüksek lisans danışmanısın. Öğrencilerin genel sorularını yanıtlıyorsun.

Konular:
- Başvuru süreci
- Vize işlemleri
- Burs imkanları
- Yaşam maliyetleri
- Ülke karşılaştırmaları

Kısa ve net cevaplar ver. Gerekirse detaylı agent'lara yönlendir.""",
        "capabilities": [
            "Genel soru-cevap",
            "Kaynak yönlendirme",
            "Süreç açıklama"
        ],
        "avg_tokens_per_task": {
            "quick_answer": 300,
            "detailed_answer": 800
        },
        "premium_only": False  # Basic'te de kullanılabilir (limitli)
    }
}

# =============================================================================
# USAGE TRACKING
# =============================================================================

class TokenTracker:
    """Token kullanımını takip eden sınıf"""
    
    def __init__(self):
        # TODO: Redis veya DB'ye taşı
        self._usage = {}
    
    def get_user_balance(self, user_id):
        """Kullanıcının kalan token bakiyesini al"""
        user_data = self._usage.get(user_id, {})
        return {
            "total_purchased": user_data.get("total_purchased", 0),
            "total_used": user_data.get("total_used", 0),
            "remaining": user_data.get("total_purchased", 0) - user_data.get("total_used", 0),
            "last_purchase": user_data.get("last_purchase"),
            "usage_history": user_data.get("history", [])[-10:]  # Son 10 kullanım
        }
    
    def add_tokens(self, user_id, tokens, package_id, payment_id=None):
        """Kullanıcıya token ekle"""
        if user_id not in self._usage:
            self._usage[user_id] = {
                "total_purchased": 0,
                "total_used": 0,
                "history": [],
                "purchases": []
            }
        
        self._usage[user_id]["total_purchased"] += tokens
        self._usage[user_id]["last_purchase"] = datetime.now().isoformat()
        self._usage[user_id]["purchases"].append({
            "tokens": tokens,
            "package": package_id,
            "payment_id": payment_id,
            "date": datetime.now().isoformat()
        })
        
        return self.get_user_balance(user_id)
    
    def use_tokens(self, user_id, input_tokens, output_tokens, agent_id, model_id):
        """Token kullan ve kaydet"""
        total_tokens = input_tokens + output_tokens
        balance = self.get_user_balance(user_id)
        
        if balance["remaining"] < total_tokens:
            return {
                "success": False,
                "error": "insufficient_tokens",
                "required": total_tokens,
                "remaining": balance["remaining"]
            }
        
        # Maliyet hesapla
        model_pricing = OUR_PRICING.get(model_id, OUR_PRICING["claude-3-5-sonnet-20241022"])
        cost_input = (input_tokens / 1_000_000) * model_pricing["input_per_1m"]
        cost_output = (output_tokens / 1_000_000) * model_pricing["output_per_1m"]
        total_cost = cost_input + cost_output
        
        # Kullanımı kaydet
        self._usage[user_id]["total_used"] += total_tokens
        self._usage[user_id]["history"].append({
            "agent": agent_id,
            "model": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost_usd": round(total_cost, 6),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "tokens_used": total_tokens,
            "cost_usd": round(total_cost, 6),
            "remaining": balance["remaining"] - total_tokens
        }
    
    def get_usage_stats(self, user_id, period_days=30):
        """Kullanım istatistikleri"""
        user_data = self._usage.get(user_id, {})
        history = user_data.get("history", [])
        
        # Son X gün filtreleme
        cutoff = datetime.now() - timedelta(days=period_days)
        recent = [h for h in history if datetime.fromisoformat(h["timestamp"]) > cutoff]
        
        # Agent bazlı kullanım
        by_agent = {}
        for h in recent:
            agent = h["agent"]
            if agent not in by_agent:
                by_agent[agent] = {"tokens": 0, "cost": 0, "count": 0}
            by_agent[agent]["tokens"] += h["total_tokens"]
            by_agent[agent]["cost"] += h["cost_usd"]
            by_agent[agent]["count"] += 1
        
        return {
            "period_days": period_days,
            "total_tokens": sum(h["total_tokens"] for h in recent),
            "total_cost": round(sum(h["cost_usd"] for h in recent), 4),
            "request_count": len(recent),
            "by_agent": by_agent,
            "avg_tokens_per_request": round(sum(h["total_tokens"] for h in recent) / len(recent)) if recent else 0
        }


# Global tracker instance
token_tracker = TokenTracker()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def estimate_tokens(text):
    """Metin için yaklaşık token sayısı tahmin et"""
    # Basit tahmin: ~4 karakter = 1 token (İngilizce için)
    # Türkçe için ~3.5 karakter = 1 token
    return len(text) // 4

def check_token_balance(user_id, estimated_tokens):
    """Kullanıcının yeterli token'ı var mı kontrol et"""
    balance = token_tracker.get_user_balance(user_id)
    return balance["remaining"] >= estimated_tokens

def require_tokens(estimated_tokens):
    """Token kontrolü yapan decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.headers.get('X-User-ID', 'anonymous')
            
            if not check_token_balance(user_id, estimated_tokens):
                balance = token_tracker.get_user_balance(user_id)
                return jsonify({
                    "success": False,
                    "error": "insufficient_tokens",
                    "message": "Yeterli token yok",
                    "required": estimated_tokens,
                    "remaining": balance["remaining"],
                    "purchase_url": "/pricing/tokens"
                }), 402  # Payment Required
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================================================
# FLASK API ROUTES
# =============================================================================

def register_token_routes(app):
    """Token sistemi route'larını Flask app'e kaydet"""
    
    @app.route('/api/tokens/balance', methods=['GET'])
    def get_token_balance():
        """Kullanıcının token bakiyesini döndür"""
        user_id = request.headers.get('X-User-ID', 'anonymous')
        balance = token_tracker.get_user_balance(user_id)
        
        return jsonify({
            "success": True,
            "balance": balance,
            "packages": TOKEN_PACKAGES
        })
    
    @app.route('/api/tokens/packages', methods=['GET'])
    def get_token_packages():
        """Satın alınabilir token paketlerini döndür"""
        return jsonify({
            "success": True,
            "packages": TOKEN_PACKAGES,
            "pricing_info": {
                "margin": f"{MARGIN_PERCENTAGE * 100}%",
                "models": OUR_PRICING
            }
        })
    
    @app.route('/api/tokens/usage', methods=['GET'])
    def get_token_usage():
        """Kullanım istatistiklerini döndür"""
        user_id = request.headers.get('X-User-ID', 'anonymous')
        period = request.args.get('period', 30, type=int)
        
        stats = token_tracker.get_usage_stats(user_id, period)
        balance = token_tracker.get_user_balance(user_id)
        
        return jsonify({
            "success": True,
            "balance": balance,
            "usage": stats
        })
    
    @app.route('/api/tokens/estimate', methods=['POST'])
    def estimate_cost():
        """Bir görev için tahmini token/maliyet hesapla"""
        data = request.json
        agent_id = data.get('agent_id', 'general_advisor')
        task_type = data.get('task_type', 'quick_answer')
        input_text = data.get('input_text', '')
        
        agent = AGENTS.get(agent_id)
        if not agent:
            return jsonify({"success": False, "error": "Agent not found"}), 404
        
        # Tahmini token hesapla
        input_tokens = estimate_tokens(input_text) if input_text else 500
        output_tokens = agent.get('avg_tokens_per_task', {}).get(task_type, 1000)
        total_tokens = input_tokens + output_tokens
        
        # Maliyet hesapla
        model_pricing = OUR_PRICING.get(agent["model"])
        cost = (input_tokens / 1_000_000) * model_pricing["input_per_1m"] + \
               (output_tokens / 1_000_000) * model_pricing["output_per_1m"]
        
        return jsonify({
            "success": True,
            "estimate": {
                "agent": agent_id,
                "model": agent["model"],
                "task_type": task_type,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost_usd": round(cost, 6),
                "cost_display": f"${cost:.4f}"
            }
        })
    
    @app.route('/api/agents', methods=['GET'])
    def get_agents():
        """Tüm mevcut agentları listele"""
        return jsonify({
            "success": True,
            "agents": AGENTS,
            "total": len(AGENTS)
        })
    
    @app.route('/api/agents/<agent_id>', methods=['GET'])
    def get_agent(agent_id):
        """Belirli bir agent'ın detaylarını döndür"""
        agent = AGENTS.get(agent_id)
        if not agent:
            return jsonify({"success": False, "error": "Agent not found"}), 404
        
        return jsonify({
            "success": True,
            "agent": agent,
            "pricing": OUR_PRICING.get(agent["model"])
        })
    
    @app.route('/api/agents/<agent_id>/chat', methods=['POST'])
    def agent_chat(agent_id):
        """Agent ile sohbet - Token bazlı"""
        agent = AGENTS.get(agent_id)
        if not agent:
            return jsonify({"success": False, "error": "Agent not found"}), 404
        
        # Premium kontrolü
        if agent.get("premium_only"):
            user_id = request.headers.get('X-User-ID', 'anonymous')
            # TODO: Premium tier kontrolü
        
        data = request.json
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not message:
            return jsonify({"success": False, "error": "Message required"}), 400
        
        # Token tahmini
        input_tokens = estimate_tokens(message) + estimate_tokens(agent["system_prompt"])
        for h in conversation_history:
            input_tokens += estimate_tokens(h.get('content', ''))
        
        estimated_output = 1000  # Ortalama çıktı
        total_estimated = input_tokens + estimated_output
        
        # Token bakiye kontrolü
        user_id = request.headers.get('X-User-ID', 'anonymous')
        if not check_token_balance(user_id, total_estimated):
            balance = token_tracker.get_user_balance(user_id)
            return jsonify({
                "success": False,
                "error": "insufficient_tokens",
                "message": "Yeterli token yok. Lütfen token satın alın.",
                "estimated_tokens": total_estimated,
                "remaining": balance["remaining"],
                "purchase_url": "/pricing/tokens",
                "packages": TOKEN_PACKAGES
            }), 402
        
        # TODO: Gerçek Claude API çağrısı yapılacak
        # Şimdilik mock response
        mock_response = f"""[{agent['name']} - Demo Response]

Mesajınız: "{message[:100]}..."

Bu bir demo yanıtıdır. Gerçek implementasyon için:
1. Anthropic API key gerekli
2. Token kullanımı gerçek zamanlı takip edilecek
3. Her model için farklı fiyatlandırma uygulanacak

Tahmini token kullanımı:
- Input: ~{input_tokens} tokens
- Output: ~{estimated_output} tokens
- Toplam: ~{total_estimated} tokens
- Maliyet: ~${(total_estimated / 1000000) * OUR_PRICING[agent['model']]['output_per_1m']:.4f}
"""
        
        # Mock için token kullanımı kaydet (gerçekte API response'dan alınacak)
        actual_output_tokens = len(mock_response) // 4
        usage_result = token_tracker.use_tokens(
            user_id,
            input_tokens,
            actual_output_tokens,
            agent_id,
            agent["model"]
        )
        
        return jsonify({
            "success": True,
            "response": {
                "message": mock_response,
                "agent": agent_id,
                "model": agent["model"]
            },
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": actual_output_tokens,
                "total_tokens": input_tokens + actual_output_tokens,
                "cost_usd": usage_result.get("cost_usd", 0)
            },
            "balance": {
                "remaining": usage_result.get("remaining", 0)
            }
        })
    
    @app.route('/api/tokens/add-demo', methods=['POST'])
    def add_demo_tokens():
        """Demo için token ekle (development only)"""
        if os.environ.get('FLASK_ENV') == 'production':
            return jsonify({"success": False, "error": "Not available in production"}), 403
        
        user_id = request.headers.get('X-User-ID', 'anonymous')
        tokens = request.json.get('tokens', 10000)
        
        result = token_tracker.add_tokens(user_id, tokens, 'demo', 'demo-payment')
        
        return jsonify({
            "success": True,
            "message": f"{tokens} demo tokens added",
            "balance": result
        })
    
    @app.route('/api/pricing/models', methods=['GET'])
    def get_model_pricing():
        """Model bazlı fiyatlandırmayı göster"""
        return jsonify({
            "success": True,
            "anthropic_pricing": ANTHROPIC_PRICING,
            "our_pricing": OUR_PRICING,
            "margin": f"{MARGIN_PERCENTAGE * 100}%",
            "note": "Fiyatlar 1M token başına USD"
        })

