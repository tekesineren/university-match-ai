# 🚀 Başlangıç Rehberi - Adım Adım

Bu rehber, projeyi sıfırdan nasıl kullanacağını gösterir. Hiçbir şey bilmiyorsan bile takip edebilirsin!

---

## 📋 İhtiyacın Olanlar (İndirme Linkleri)

### 1. Python (Backend için)
- **İndir:** https://www.python.org/downloads/
- **Kurulum:** İndirdiğin dosyayı çalıştır, "Add Python to PATH" işaretle, "Install Now" tıkla
- **Kontrol:** Terminal'de `python --version` yaz (Python 3.8+ olmalı)

### 2. Node.js (Web App için)
- **İndir:** https://nodejs.org/
- **LTS versiyonu** seç (uzun süre desteklenen)
- **Kurulum:** İndirdiğin dosyayı çalıştır, "Next" ile devam et
- **Kontrol:** Terminal'de `node --version` yaz

### 3. Git (Zaten var gibi görünüyor, ama kontrol et)
- **Kontrol:** Terminal'de `git --version` yaz
- **Yoksa:** https://git-scm.com/downloads

---

## 🎯 Seçenek 1: Sadece Backend API Kullanmak

### Adım 1: Projeyi İndir
```bash
cd C:\Users\user\master-application-agent
```

### Adım 2: Backend Klasörüne Git
```bash
cd backend
```

### Adım 3: Gerekli Paketleri Yükle
```bash
pip install -r requirements.txt
```

### Adım 4: Backend'i Başlat
```bash
python app.py
```

**Çıktı:**
```
 * Running on http://127.0.0.1:5000
```

### Adım 5: Test Et (Yeni Terminal Aç)
Tarayıcıda şu adrese git:
```
http://localhost:5000/api/universities
```

Üniversite listesini görmelisin! ✅

---

## 🌐 Seçenek 2: Web App ile Kullanmak (Önerilen)

### Adım 1: Backend'i Çalıştır
Yukarıdaki "Seçenek 1" adımlarını yap, backend çalışıyor olsun.

### Adım 2: Yeni Terminal Aç
Backend çalışırken, **yeni bir terminal penceresi** aç.

### Adım 3: Web App Klasörüne Git
```bash
cd C:\Users\user\master-application-agent\web-app
```

### Adım 4: Node Paketlerini Yükle (İlk Defa)
```bash
npm install
```

**Not:** Bu işlem 2-5 dakika sürebilir, sabırlı ol! ☕

### Adım 5: Web App'i Başlat
```bash
npm run dev
```

**Çıktı:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Adım 6: Tarayıcıda Aç
Tarayıcında şu adrese git:
```
http://localhost:5173
```

**Web arayüzü görünecek!** 🎉

---

## 📱 Seçenek 3: iOS App (İleri Seviye)

iOS app için Xcode ve Mac gerekir. Şimdilik web app ile başla, iOS'u sonra yapabilirsin.

---

## 🧪 İlk Test - Üniversite Eşleştirme

### Web App'te:
1. **GPA gir** (örn: 3.5)
2. **Language test seç** (TOEFL veya IELTS)
3. **Score gir** (örn: 95)
4. **Background seç** (örn: robotics, engineering)
5. **Work experience gir** (örn: 1.5 yıl)
6. **"Find My Match"** butonuna tıkla

**Sonuç:** Üniversiteler High/Medium/Low match olarak sıralanacak! 🎯

---

## 🛠️ Sorun Giderme

### "python: command not found"
- Python yüklü değil veya PATH'e eklenmemiş
- Python'u yeniden yükle, "Add to PATH" seçeneğini işaretle

### "pip: command not found"
- Python ile birlikte gelir, `python -m pip install -r requirements.txt` dene

### "npm: command not found"
- Node.js yüklü değil
- Node.js'i yeniden yükle

### "Port 5000 already in use"
- Backend zaten çalışıyor veya başka bir program kullanıyor
- O programı kapat veya farklı port kullan

### "Port 5173 already in use"
- Web app zaten çalışıyor
- Tarayıcıda `http://localhost:5173` adresine git

---

## 📚 Sonraki Adımlar

1. **CV Yükle:** Web app'te CV'ni yükle, otomatik analiz et
2. **Premium Features:** `backend/premium.py` dosyasını incele
3. **Stripe Entegrasyonu:** Para kazanmak için Stripe hesabı aç
4. **Deploy:** Railway, Vercel gibi platformlara deploy et

---

## 🆘 Yardım Lazım?

- **GitHub Issues:** https://github.com/tekesineren/university-match-ai/issues
- **README'yi Oku:** `README.md` dosyasında detaylı bilgi var
- **Backend Kod:** `backend/app.py` dosyasını incele

---

**İyi şanslar! 🚀**

