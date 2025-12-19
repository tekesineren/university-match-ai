# 🎓 HYNOPS - University Match AI

> **Son Güncelleme:** 19 Aralık 2024
> **Proje Sahibi:** @tekesineren
> **Domain:** hynops.com
> **GitHub:** https://github.com/tekesineren/university-match-ai

---

## 📋 PROJE ÖZETİ

Yüksek lisans başvurusu yapacak öğrenciler için AI destekli üniversite eşleştirme ve başvuru yönetim platformu.

### Temel Özellikler
1. **Üniversite Eşleştirme** - Profil bazlı akıllı eşleştirme algoritması
2. **CV Parsing** - PDF/DOCX'den otomatik bilgi çıkarma
3. **Skill Synonym Mapping** - JS=JavaScript=Node.js tarzı normalizasyon
4. **AI Agent Sistemi** - Claude Opus 4.5 ile kişisel danışmanlık
5. **Document Checklist** - Her üniversite için gerekli belge takibi
6. **Token Sistemi** - Kullanım bazlı fiyatlandırma

---

## 💰 İŞ MODELİ

### Tier Yapısı

| Tier | Fiyat | Özellikler |
|------|-------|------------|
| **Basic** | Ücretsiz | Sınırsız eşleştirme, CV parsing, skill mapping |
| **Premium** | $19/ay | Document checklist, deadline tracking, AI agents |

### Token Sistemi (Premium için)

| Paket | Token | Fiyat | Birim Fiyat |
|-------|-------|-------|-------------|
| Starter | 50K | $5 | $0.10/1K |
| Standard | 200K (+20K bonus) | $15 | $0.075/1K |
| Pro | 500K (+100K bonus) | $30 | $0.06/1K |

### Kar Marjı
- Anthropic API maliyeti + **%33 margin** = Bizim fiyat
- Örnek: Claude 3.5 Sonnet output $15/1M → Biz $20/1M

---

## 🏗️ TEKNİK MİMARİ

### Backend (Python/Flask)
```
backend/
├── app.py              # Ana API + UNIVERSITIES database
├── pricing.py          # Tier sistemi + premium features
├── token_system.py     # Token tracking + AI agents
├── premium.py          # Rate limiting + user tiers
├── stripe_integration.py # Ödeme entegrasyonu
├── email_service.py    # Email bildirimleri
└── requirements.txt    # Dependencies
```

### Frontend (React/Vite)
```
web-app/
├── src/
│   ├── App.jsx         # Ana uygulama
│   ├── components/
│   │   ├── Pricing.jsx      # ⚠️ GÜNCELLENMELİ (eski fiyatlar)
│   │   ├── CVUpload.jsx     # CV yükleme
│   │   ├── InputForm.jsx    # Manuel form
│   │   ├── ResultsView.jsx  # Sonuç görüntüleme
│   │   └── ... 
│   └── utils/
│       └── cvParser.js      # Client-side CV parsing
└── package.json
```

### iOS App (Swift + Expo)
```
ios-app/           # Native Swift
ios-app-expo/      # React Native/Expo
```

---

## 🔌 API ENDPOINTS

### Core (Herkes)
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/health` | GET | Health check |
| `/api/universities` | GET | Tüm üniversiteler |
| `/api/match` | POST | Eşleştirme yap |
| `/api/parse-cv` | POST | CV parse et |

### Skills
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/skills/normalize` | POST | Skill normalize et |
| `/api/skills/extract` | POST | Metinden skill çıkar |
| `/api/skills/synonyms` | GET | Tüm synonym mapping |

### Pricing & Tokens
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/pricing` | GET | Pricing page data |
| `/api/tokens/balance` | GET | Token bakiyesi |
| `/api/tokens/packages` | GET | Satın alınabilir paketler |
| `/api/agents` | GET | Tüm AI agentlar |
| `/api/agents/<id>/chat` | POST | Agent ile sohbet |

---

## 🤖 AI AGENTS

| Agent | Model | Kullanım |
|-------|-------|----------|
| ✍️ Motivation Letter | Claude 3.5 Sonnet | Letter yazımı |
| 📄 CV Optimizer | Claude 3.5 Sonnet | CV analizi |
| 🎤 Interview Prep | Claude 3.5 Haiku | Mülakat hazırlık |
| 🎯 Application Strategist | Claude 3.5 Sonnet | Strateji oluşturma |
| 💬 General Advisor | Claude 3.5 Haiku | Genel sorular |

---

## 📊 VERİTABANI YAPISI

### UNIVERSITIES (app.py içinde)
```python
{
    "id": 1,
    "name": "ETH Zurich",
    "program": "MSc in Robotics",
    "country": "Switzerland",
    "min_gpa": 3.5,
    "min_language_score": 100,
    "required_background": ["engineering", "robotics"],
    "match_score": 0,
    
    # YENİ - Eklenecek
    "required_documents": [...],
    "optional_documents": [...],
    "deadlines": {...},
    "application_fee": {...}
}
```

### SKILL_SYNONYMS (app.py içinde)
```python
{
    "javascript": ["javascript", "js", "ecmascript", "es6"],
    "python": ["python", "py", "python3"],
    # ... 50+ kategori
}
```

---

## ✅ TAMAMLANAN ÖZELLİKLER

- [x] Üniversite eşleştirme algoritması
- [x] CV parsing (PDF, DOCX)
- [x] Skill synonym mapping (50+ kategori)
- [x] Pricing tier sistemi (Basic/Premium)
- [x] Token bazlı fiyatlandırma
- [x] AI Agent API endpoints
- [x] Rate limiting

---

## 🔄 DEVAM EDEN / YAPILACAK

### Yüksek Öncelik
- [ ] **Frontend Pricing.jsx güncelle** - Yeni tier yapısına göre
- [ ] **UNIVERSITIES'e required_documents ekle** - 20 üniversite
- [ ] **API URL'leri hynops.com yap**
- [ ] **Token UI oluştur** - Balance, usage, purchase

### Orta Öncelik
- [ ] Document checklist frontend UI
- [ ] AI Agent chat frontend UI
- [ ] Stripe gerçek entegrasyonu
- [ ] Email reminder sistemi

### Düşük Öncelik
- [ ] iOS app güncelleme
- [ ] Analytics dashboard
- [ ] Admin panel

---

## 🚀 DEPLOYMENT

### Mevcut
- **Backend:** Replit (hynops.com'a bağlı)
- **Frontend:** Vercel? (belirsiz)
- **Database:** In-memory (app.py içinde)

### Önerilen
- Backend: Replit veya Railway
- Frontend: Vercel
- Database: Supabase (production için)
- Payments: Stripe

---

## 🔑 ENVIRONMENT VARIABLES

```env
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-...

# Stripe (opsiyonel şimdilik)
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=noreply@hynops.com
SENDER_PASSWORD=app_password

# App
FLASK_ENV=production
PORT=5001
```

---

## 📝 NOTLAR

### Son Konuşma Özeti (19 Aralık 2024)
1. CV parsing için synonym mapping eklendi
2. Premium/Basic tier sistemi oluşturuldu
3. Token bazlı AI agent sistemi eklendi
4. %33 margin ile fiyatlandırma

### Kararlar
- Basic'te sınırsız eşleştirme (değer görsünler)
- Premium'da AI agent + document checklist
- Token sistemi Cursor benzeri
- Anthropic fiyat + %33 = Bizim fiyat

---

## 📞 İLETİŞİM

- **Email:** erentekesin@hynops.com
- **GitHub:** @tekesineren
- **Website:** hynops.com

