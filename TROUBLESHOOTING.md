# Troubleshooting Guide

## CV Upload - 403 Error

### Problem
When uploading a CV, you see: "⚠ CV analiz edilemedi (403). Backend çalışıyor mu?"

### Solutions

#### 1. **Backend Çalışmıyor**

**Check:**
```bash
# Backend klasörüne gidin
cd backend

# Backend'in çalıştığını kontrol edin
# Terminal'de şunu görmelisiniz:
#  * Running on http://127.0.0.1:5000
```

**Fix:**
```bash
# Backend'i başlatın
cd backend
python app.py
```

Backend'in `http://localhost:5000` adresinde çalıştığından emin olun.

---

#### 2. **CORS Hatası**

**Check:**
Browser console'da (F12) şu hatayı görüyorsanız:
```
Access to fetch at 'http://localhost:5000/api/parse-cv' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Fix:**
Backend'inizde CORS ayarlarının doğru olduğundan emin olun. `backend/app.py` dosyasında:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

Ardından backend'i yeniden başlatın:
```bash
# Terminal'de Ctrl+C ile durdurun
# Sonra tekrar başlatın:
python app.py
```

---

#### 3. **Rate Limit Aşıldı**

**Check:**
Eğer ücretsiz tier kullanıyorsanız:
- Günlük 5 request limiti var
- Aylık 1 CV analizi limiti var

**Fix:**

**Option A: Limitleri Sıfırlama (Development için)**
```bash
# Backend klasöründe users.json dosyasını silin
cd backend
rm users.json  # Linux/Mac
del users.json  # Windows
```

**Option B: Limitleri Artırma (Development için)**
`backend/premium.py` dosyasını açın ve free tier limitlerini artırın:

```python
TIER_LIMITS = {
    'free': {
        'requests_per_day': 100,  # 5'ten 100'e çıkarın
        'cv_analyses_per_month': 100,  # 1'den 100'e çıkarın
        ...
    }
}
```

Sonra backend'i yeniden başlatın.

---

#### 4. **Port Çakışması**

**Check:**
Backend başlatırken şu hatayı görüyorsanız:
```
OSError: [Errno 48] Address already in use
```

**Fix:**

**Option A: Kullanılan Portu Bul ve Kapat**
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows PowerShell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Option B: Farklı Port Kullan**
`backend/app.py` dosyasının sonunda:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 5000 yerine 5001
```

Ve frontend'te API URL'ini güncelleyin veya `vite.config.js` dosyasında proxy ayarını değiştirin.

---

#### 5. **Dosya Formatı**

**Check:**
- PDF veya DOCX formatında mı?
- Dosya boyutu çok büyük mü? (Önerilen: 10MB altı)
- Dosya bozuk olabilir mi?

**Fix:**
- PDF veya DOCX formatında bir CV kullanın
- Farklı bir CV dosyası deneyin
- Dosya boyutunu kontrol edin

---

#### 6. **API URL Yanlış**

**Check:**
Browser console'da (F12) API URL'ini kontrol edin:
```javascript
console.log('API URL:', apiUrl)
```

**Fix:**

**Development için:**
`web-app/vite.config.js` dosyasında proxy ayarının olduğundan emin olun:

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
```

---

#### 7. **Python Kütüphaneleri Eksik**

**Check:**
Backend terminal'de şu hatayı görüyorsanız:
```
ModuleNotFoundError: No module named 'PyPDF2'
```

**Fix:**
```bash
cd backend
pip install -r requirements.txt
```

Eğer `requirements.txt` dosyası yoksa:
```bash
pip install flask flask-cors PyPDF2 python-docx
```

---

## Quick Diagnostic Steps

1. **Backend çalışıyor mu?**
   - Tarayıcıda açın: http://localhost:5000/api/health
   - "OK" yazısı görmelisiniz

2. **Frontend backend'e bağlanabiliyor mu?**
   - Browser console'u açın (F12)
   - CV yükleme sırasında network tab'ını kontrol edin
   - Request'in başarılı olup olmadığını görün

3. **CORS hatası var mı?**
   - Browser console'da CORS hatası mesajı var mı?
   - Backend'de CORS ayarları doğru mu?

4. **Rate limit aşıldı mı?**
   - `backend/users.json` dosyasını kontrol edin
   - Limit aşıldıysa sıfırlayın

---

## Common Error Messages

### "CV analiz edilemedi (403)"
- Backend çalışmıyor olabilir
- CORS hatası olabilir
- Rate limit aşılmış olabilir

### "CV analiz edilemedi (500)"
- Backend'de bir hata var
- Python kütüphaneleri eksik olabilir
- Dosya formatı sorunlu olabilir

### "CV analiz edilemedi (429)"
- Rate limit aşıldı
- `users.json` dosyasını silin veya limitleri artırın

### "Backend'e bağlanılamadı"
- Backend çalışmıyor
- Port yanlış
- Firewall sorunu olabilir

---

## Still Having Issues?

1. Backend terminal loglarını kontrol edin
2. Browser console'da (F12) hata mesajlarını kontrol edin
3. Network tab'ında request/response detaylarını inceleyin
4. Backend'i yeniden başlatın
5. Frontend'i yeniden başlatın

