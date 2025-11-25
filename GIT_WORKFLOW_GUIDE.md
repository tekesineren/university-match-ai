# 🔀 Git Branch, Commit ve Push Workflow Rehberi

> **University Match AI - Git Workflow Guide**  
> Branch oluşturma, commit ve push işlemleri için adım adım komutlar

---

## 📋 İçindekiler

1. [Hızlı Başlangıç](#-hızlı-başlangıç-5-dakika)
2. [Detaylı Adımlar](#-detaylı-adımlar)
3. [Yaygın Senaryolar](#-yaygın-senaryolar)
4. [Güvenlik Kontrolleri](#-güvenlik-kontrolleri)
5. [Sorun Giderme](#-sorun-giderme)

---

## ⚡ Hızlı Başlangıç (5 Dakika)

### Temel Git Workflow

```bash
# 1. Yeni branch oluştur ve geç
git checkout -b feature/ios-app-setup

# 2. Değişiklikleri ekle
git add .

# 3. Commit yap
git commit -m "feat: Add iOS app setup guide and examples"

# 4. Push et
git push origin feature/ios-app-setup
```

**✅ Tamamlandı!** Artık GitHub'da branch'iniz mevcut.

---

## 📝 Detaylı Adımlar

### Adım 1: Mevcut Durumu Kontrol Et

```bash
# Hangi branch'te olduğunuzu kontrol edin
git branch

# Değişiklikleri kontrol edin
git status

# Son commit'leri görün
git log --oneline -5
```

**Çıktı Örneği:**
```
* main
  feature/backend-api

Changes not staged for commit:
  modified:   ios-app/Models.swift
  modified:   ios-app/APIService.swift
  new file:   ios-app/REST_API_EXAMPLE.md
```

### Adım 2: Yeni Branch Oluştur

#### Yöntem 1: Branch Oluştur ve Geç (Tek Komut)

```bash
git checkout -b feature/ios-app-setup
```

**Branch İsimlendirme Önerileri:**
- `feature/` - Yeni özellik için: `feature/ios-app-setup`
- `fix/` - Bug fix için: `fix/api-error-handling`
- `docs/` - Dokümantasyon için: `docs/ios-guide`
- `refactor/` - Kod iyileştirme için: `refactor/api-service`

#### Yöntem 2: Önce Oluştur, Sonra Geç

```bash
# Branch oluştur (henüz geçmez)
git branch feature/ios-app-setup

# Branch'e geç
git checkout feature/ios-app-setup
```

#### Yöntem 3: Main'den Yeni Branch (Güncel Kod ile)

```bash
# Önce main'e geç
git checkout main

# Main'i güncelle (remote'tan çek)
git pull origin main

# Yeni branch oluştur ve geç
git checkout -b feature/ios-app-setup
```

### Adım 3: Değişiklikleri Stage'e Ekle

#### Tüm Değişiklikleri Ekle

```bash
# Tüm değişiklikleri ekle
git add .
```

#### Belirli Dosyaları Ekle

```bash
# Tek dosya
git add ios-app/Models.swift

# Birden fazla dosya
git add ios-app/Models.swift ios-app/APIService.swift

# Pattern ile (tüm .md dosyaları)
git add *.md

# Klasör ile
git add ios-app/
```

#### İnteraktif Ekleme (Seçici)

```bash
# Her değişikliği tek tek onaylayarak ekle
git add -i

# Veya
git add -p
```

### Adım 4: Commit Mesajı Yazma

#### Basit Commit

```bash
git commit -m "feat: Add iOS app REST API examples"
```

#### Detaylı Commit (Multi-line)

```bash
git commit -m "feat: Add iOS app REST API examples

- Add REST_API_EXAMPLE.md with complete code samples
- Update Models.swift with full UserProfile model
- Update APIService.swift with error handling
- Add login form example with state management

Closes #123"
```

#### Commit Mesajı Formatı (Conventional Commits)

**Format:** `<type>: <subject>`

**Type'lar:**
- `feat:` - Yeni özellik
- `fix:` - Bug fix
- `docs:` - Dokümantasyon değişiklikleri
- `style:` - Formatting (kod değişikliği yok)
- `refactor:` - Kod refactoring
- `test:` - Test ekleme/düzenleme
- `chore:` - Build process, tooling vb.

**Örnekler:**
```bash
git commit -m "feat: Add iOS icon and launch screen guide"
git commit -m "fix: Correct API error handling in APIService"
git commit -m "docs: Update iOS setup guide with Xcode instructions"
git commit -m "refactor: Improve Models.swift structure"
```

### Adım 5: Remote'a Push Etme

#### İlk Push (Branch'i Oluştur)

```bash
# Branch'i remote'a push et ve upstream ayarla
git push -u origin feature/ios-app-setup

# veya kısa hali
git push --set-upstream origin feature/ios-app-setup
```

**Açıklama:**
- `-u` veya `--set-upstream`: Remote branch'i track etmek için
- İlk push'tan sonra sadece `git push` yeterli olur

#### Sonraki Push'lar

```bash
# Upstream ayarlıysa sadece
git push

# Veya açıkça belirt
git push origin feature/ios-app-setup
```

### Adım 6: Pull Request Oluşturma

1. **GitHub'a gidin**
2. Branch'inize gidin: `feature/ios-app-setup`
3. **"Compare & pull request"** butonuna tıklayın
4. PR açıklaması yazın
5. **"Create pull request"** tıklayın

---

## 🎯 Yaygın Senaryolar

### Senaryo 1: Feature Branch Oluşturma ve Push

```bash
# 1. Main'de olduğunuzdan emin olun
git checkout main

# 2. Main'i güncelle
git pull origin main

# 3. Yeni feature branch oluştur
git checkout -b feature/ios-icon-setup

# 4. Değişiklikleri yap (dosyaları düzenle)

# 5. Değişiklikleri ekle
git add .

# 6. Commit yap
git commit -m "feat: Add iOS icon and launch screen guide"

# 7. Push et
git push -u origin feature/ios-icon-setup
```

### Senaryo 2: Birden Fazla Commit

```bash
# Branch oluştur
git checkout -b feature/multiple-commits

# İlk değişiklik
git add ios-app/Models.swift
git commit -m "feat: Update Models.swift with UserProfile"

# İkinci değişiklik
git add ios-app/APIService.swift
git commit -m "feat: Add error handling to APIService"

# Üçüncü değişiklik
git add ios-app/REST_API_EXAMPLE.md
git commit -m "docs: Add REST API examples guide"

# Tüm commit'leri push et
git push -u origin feature/multiple-commits
```

### Senaryo 3: Commit Mesajını Düzeltme (Son Commit)

```bash
# Son commit mesajını değiştir
git commit --amend -m "feat: Add iOS app setup guide (corrected)"

# Eğer push ettiyseniz, force push gerekir (dikkatli kullanın!)
git push --force origin feature/ios-app-setup
```

### Senaryo 4: Remote'tan Güncelleme (Merge Conflict Olmadan)

```bash
# Main branch'e geç
git checkout main

# Remote'tan güncellemeleri çek
git pull origin main

# Feature branch'inize geri dön
git checkout feature/ios-app-setup

# Main'deki değişiklikleri feature branch'inize merge et
git merge main
```

### Senaryo 5: Uncommitted Değişiklikleri Saklama (Stash)

```bash
# Değişiklikleri geçici olarak sakla
git stash

# Başka işler yap (branch değiştir, commit yap vb.)

# Sakladığınız değişiklikleri geri getir
git stash pop
```

### Senaryo 6: Branch Silme

```bash
# Local branch'i sil
git branch -d feature/ios-app-setup

# Force delete (unmerged değişiklikler varsa)
git branch -D feature/ios-app-setup

# Remote branch'i sil
git push origin --delete feature/ios-app-setup
```

---

## 🔒 Güvenlik Kontrolleri

### Push Öncesi Kontrol Listesi

```bash
# 1. Hangi dosyalar değişti?
git status

# 2. Hangi değişiklikler yapıldı?
git diff

# 3. Commit'lerinizi görüntüleyin
git log --oneline -5

# 4. Remote'ta neler var?
git fetch origin
git log origin/main..HEAD --oneline
```

### Hassas Bilgiler Kontrolü

**❌ ASLA Commit Etmeyin:**
- API keys
- Passwords
- Private tokens
- Personal information
- `.env` dosyaları
- `node_modules/` klasörü

**Kontrol:**
```bash
# .gitignore dosyasını kontrol edin
cat .gitignore

# Eğer hassas bilgi commit ettiyseniz:
# 1. Git history'den temizleyin (git filter-branch)
# 2. Veya branch'i silip yeniden oluşturun
```

---

## 🐛 Sorun Giderme

### Sorun 1: "Your branch is ahead of 'origin/main'"

**Çözüm:**
```bash
# Remote'a push edin
git push origin feature/ios-app-setup
```

### Sorun 2: "Please commit your changes or stash them"

**Çözüm:**
```bash
# Değişiklikleri commit et
git add .
git commit -m "WIP: Work in progress"

# Veya stash yap
git stash
```

### Sorun 3: "Failed to push some refs"

**Çözüm:**
```bash
# Remote'taki değişiklikleri çek
git pull origin feature/ios-app-setup --rebase

# Sonra tekrar push et
git push origin feature/ios-app-setup
```

### Sorun 4: Merge Conflict

**Çözüm:**
```bash
# 1. Conflict'leri göster
git status

# 2. Conflict'leri çöz (dosyaları düzenle)
# <<<<<<< HEAD
# ... your changes ...
# =======
# ... their changes ...
# >>>>>>> branch-name

# 3. Çözülen dosyaları ekle
git add resolved-file.swift

# 4. Merge'i tamamla
git commit
```

### Sorun 5: Yanlış Branch'e Commit

**Çözüm:**
```bash
# 1. Son commit'i geri al (değişiklikler korunur)
git reset --soft HEAD~1

# 2. Doğru branch'e geç
git checkout feature/correct-branch

# 3. Commit'i tekrar yap
git commit -m "feat: Correct commit message"
```

---

## 📊 Git Komut Referansı

### Branch Komutları

```bash
# Branch listele
git branch                    # Local
git branch -r                 # Remote
git branch -a                 # Tümü

# Branch oluştur
git branch new-branch

# Branch'e geç
git checkout branch-name

# Branch oluştur ve geç
git checkout -b new-branch

# Branch sil
git branch -d branch-name     # Safe delete
git branch -D branch-name     # Force delete
```

### Commit Komutları

```bash
# Stage'e ekle
git add .                     # Tümü
git add file.txt              # Tek dosya
git add folder/               # Klasör

# Commit yap
git commit -m "message"       # Basit
git commit                    # Editor açılır

# Son commit'i düzelt
git commit --amend

# Commit geçmişi
git log                       # Detaylı
git log --oneline             # Kısa
git log --graph --oneline     # Grafikli
```

### Push/Pull Komutları

```bash
# Push
git push                      # Current branch
git push origin branch-name   # Belirli branch
git push -u origin branch     # İlk push (upstream set)

# Pull
git pull                      # Current branch
git pull origin branch-name   # Belirli branch
git pull --rebase             # Rebase ile pull
```

### Durum Kontrolü

```bash
git status                    # Genel durum
git diff                      # Unstaged değişiklikler
git diff --staged             # Staged değişiklikler
git log                       # Commit geçmişi
```

---

## ✅ Best Practices

### 1. Commit Mesajları
- ✅ Açıklayıcı ve kısa olmalı
- ✅ Conventional Commits formatı kullan
- ✅ İngilizce yaz (tutarlılık için)

### 2. Branch Stratejisi
- ✅ Feature branch'ler için `feature/` prefix
- ✅ Her özellik için ayrı branch
- ✅ Branch'leri düzenli olarak temizle

### 3. Commit Sıklığı
- ✅ Mantıklı birimlerde commit yap
- ✅ Çalışan kodu commit et
- ✅ WIP (Work In Progress) commit'leri açıkça belirt

### 4. Push Stratejisi
- ✅ Her feature tamamlandığında push et
- ✅ Günlük çalışmanın sonunda push et
- ✅ Main branch'e direkt push etme, PR kullan

---

## 🎯 Hızlı Referans Kartı

```bash
# Yeni feature için tam workflow
git checkout main
git pull origin main
git checkout -b feature/my-feature
# ... değişiklikler yap ...
git add .
git commit -m "feat: Add my feature"
git push -u origin feature/my-feature
```

---

**Sonraki Adım**: GitHub'da Pull Request oluşturup code review yapabilirsiniz! 🚀

