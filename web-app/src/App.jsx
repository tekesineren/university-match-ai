import { useState, useEffect } from 'react'
import InputForm from './components/InputForm'
import ResultsView from './components/ResultsView'
import CVUpload from './components/CVUpload'
import CoreMetrics from './components/CoreMetrics'
import Pricing from './components/Pricing'
import Success from './components/Success'
import UpdateNotification from './components/UpdateNotification'
import { getApiUrl } from './utils/api'
import './App.css'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [showCVUpload, setShowCVUpload] = useState(true)
  const [cvData, setCvData] = useState(null)
  const [showPricing, setShowPricing] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  // URL'den success sayfasını kontrol et
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    if (params.get('session_id')) {
      setShowSuccess(true)
    }
  }, [])

  // Check for scheduled updates periodically
  useEffect(() => {
    const checkScheduledUpdate = () => {
      const scheduledUpdate = localStorage.getItem('scheduled_update')
      if (scheduledUpdate) {
        const scheduledDate = new Date(scheduledUpdate)
        const now = new Date()
        
        if (scheduledDate <= now) {
          // Scheduled time has arrived, clear it so UpdateNotification can show
          localStorage.removeItem('scheduled_update')
        }
      }
    }

    // Check immediately
    checkScheduledUpdate()

    // Check every minute for scheduled updates
    const interval = setInterval(checkScheduledUpdate, 60 * 1000)

    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError(null)
    
    try {
      // API URL'i belirle
      const apiUrl = getApiUrl()
      
      console.log('API URL:', apiUrl)
      
      // Retry mekanizması - Backend uyku modundaysa uyandırmak için
      let response
      let lastError
      const maxRetries = 3
      const retryDelay = 5000 // 5 saniye
      
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          // İlk denemede backend'i uyandırmak için health check yap
          if (attempt === 1) {
            const healthController = new AbortController()
            const healthTimeout = setTimeout(() => healthController.abort(), 30000)
            await fetch(`${apiUrl.replace('/match', '/health')}`, {
              method: 'GET',
              signal: healthController.signal
            }).catch(() => {}) // Health check hatası önemsiz
            clearTimeout(healthTimeout)
          }
          
          // Ana istek (60 saniye timeout)
          const controller = new AbortController()
          const timeoutId = setTimeout(() => controller.abort(), 60000)
          
          response = await fetch(`${apiUrl}/match`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              gpa: parseFloat(formData.gpa),
              grading_system: formData.gradingSystem,
              language: formData.language,
              language_test_type: formData.languageTestType,
              language_test_score: formData.languageTestScore ? parseFloat(formData.languageTestScore) : null,
              background: formData.background,
              research_experience: parseFloat(formData.researchExperience) || 0,
              work_experience: parseFloat(formData.workExperience) || 0,
              publications: parseInt(formData.publications) || 0,
              recommendation_letters: parseInt(formData.recommendationLetters) || 0,
              country: formData.country,
              undergraduate_university_ranking: formData.undergraduateUniversityRanking,
              gre_score: formData.greScore ? parseInt(formData.greScore) : null,
              gmat_score: formData.gmatScore ? parseInt(formData.gmatScore) : null,
              project_experience: formData.projectExperience,
              competition_achievements: formData.competitionAchievements,
              has_masters_degree: formData.hasMastersDegree,
              masters_university_ranking: formData.mastersUniversityRanking
            }),
            signal: controller.signal
          })
          
          clearTimeout(timeoutId)

          if (response.ok) {
            break // Başarılı, retry döngüsünden çık
          } else {
            throw new Error(`HTTP error! status: ${response.status}`)
          }
        } catch (err) {
          lastError = err
          if (attempt < maxRetries) {
            console.log(`Deneme ${attempt}/${maxRetries} başarısız, ${retryDelay/1000} saniye sonra tekrar denenecek...`)
            await new Promise(resolve => setTimeout(resolve, retryDelay))
          }
        }
      }

      if (!response || !response.ok) {
        throw lastError || new Error('Backend yanıt vermiyor')
      }

      const data = await response.json()
      
      if (data.success) {
        setResults(data)
      } else {
        // Rate limit hatası varsa pricing'e yönlendir
        if (data.rate_limit_exceeded || response.status === 429) {
          setShowPricing(true)
          setError(data.error || 'Günlük limit aşıldı. Premium\'a geçerek sınırsız erişim kazanın!')
        } else {
          setError(data.error || 'Bir hata oluştu')
        }
      }
    } catch (err) {
      console.error('API Error:', err)
      setError(`Backend API'ye bağlanılamadı. Backend uyku modunda olabilir, lütfen 30-60 saniye bekleyip tekrar deneyin. Hata: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResults(null)
    setError(null)
    setShowCVUpload(true)
    setShowForm(false)
    setCvData(null)
  }

  const handleCVUpload = async (file, extractedData = {}) => {
    console.log('📋 handleCVUpload çağrıldı:', { file: file?.name, extractedData })
    
    // Backend'den gelen verileri kullan veya fallback
    const cvData = {
      gpa: extractedData.gpa ? parseFloat(extractedData.gpa).toFixed(2) : '',
      language: extractedData.language || 'english',
      languageTestType: extractedData.language_test_type || '',
      languageTestScore: extractedData.language_test_score ? parseFloat(extractedData.language_test_score).toFixed(0) : '',
      background: extractedData.background || [],
      researchExperience: extractedData.research_experience ? parseFloat(extractedData.research_experience).toFixed(1) : '0',
      workExperience: extractedData.work_experience ? parseFloat(extractedData.work_experience).toFixed(1) : '0',
      publications: extractedData.publications || 0,
      country: extractedData.country || 'turkey',
      gradingSystem: extractedData.grading_system || '4.0',
      recommendationLetters: '0',
      undergraduateUniversityRanking: '',
      greScore: null,
      gmatScore: null,
      projectExperience: 'none',
      competitionAchievements: 'none',
      hasMastersDegree: false,
      mastersUniversityRanking: ''
    }

    console.log('📊 CV Data hazırlandı:', cvData)

    setCvData(cvData)
    
    // Eksik bilgiler varsa kullanıcıya göster ve formu doldur
    const missingFields = []
    if (!cvData.gpa) missingFields.push('GPA')
    if (!cvData.languageTestScore) missingFields.push('Dil Skoru')
    if (cvData.background.length === 0) missingFields.push('Background')
    
    console.log('⚠️ Eksik alanlar:', missingFields)
    
    // Eksik bilgiler varsa formu göster ve çıkarılan verileri doldur
    if (missingFields.length > 0) {
      console.log('📝 Eksik bilgiler var, form açılıyor...')
      setShowCVUpload(false)
      setShowForm(true)
      // Form component'ine verileri geç (InputForm'da pre-fill yapılacak)
      return
    }
    
    // Tüm bilgiler mevcut - otomatik analiz yap
    console.log('✅ Tüm bilgiler mevcut, analiz başlatılıyor...')
    setShowCVUpload(false)
    
    // Otomatik analiz ve sonuçları göster
    setTimeout(() => {
      console.log('🚀 handleSubmit çağrılıyor...')
      handleSubmit(cvData)
    }, 500)
  }

  const handleManualEntry = () => {
    setShowCVUpload(false)
    setShowForm(true)
  }

  // 3 temel parametreyi hesapla
  const calculateCoreMetrics = () => {
    // CV'den gelen veriler varsa onları kullan
    if (cvData) {
      const gpa = parseFloat(cvData.gpa) || 0
      const langScore = parseFloat(cvData.languageTestScore) || 0
      // Normalize dil skoru (TOEFL için)
      const normalizedLang = cvData.languageTestType === 'toefl' 
        ? (langScore / 120) * 100 
        : langScore
      
      // Background match - seçilen background sayısına göre
      const backgroundMatch = (cvData.background?.length || 0) * 10
      
      return {
        gpa: gpa,
        languageScore: normalizedLang,
        backgroundMatch: Math.min(backgroundMatch, 100)
      }
    }
    
    if (!results || !results.results) {
      return { gpa: 0, languageScore: 0, backgroundMatch: 0 }
    }
    
    // Sonuçlardan hesapla - high_match üniversitelerinden
    const { high_match = [] } = results.results
    const top3 = high_match.slice(0, 3)
    
    if (top3.length === 0) return { gpa: 0, languageScore: 0, backgroundMatch: 0 }
    
    const avgMatch = top3.reduce((sum, m) => sum + (m.match_score || 0), 0) / top3.length
    
    // Match score'dan tahmin et (30% GPA, 20% Language, 15% Background)
    const estimatedGPA = (avgMatch / 100) * 30 * (4.0 / 30) // 0-4.0 arası
    const estimatedLang = (avgMatch / 100) * 20 * (100 / 20) // 0-100 arası
    const estimatedBg = (avgMatch / 100) * 15 * (100 / 15) // 0-100 arası
    
    return {
      gpa: estimatedGPA,
      languageScore: estimatedLang,
      backgroundMatch: estimatedBg
    }
  }

  const coreMetrics = calculateCoreMetrics()

  // Success sayfası gösteriliyorsa sadece onu göster
  if (showSuccess) {
    return <Success />
  }

  return (
    <div className="App">
      <UpdateNotification 
        onUpdate={() => {
          console.log('Update triggered')
        }}
        onSchedule={(scheduleData) => {
          console.log('Update scheduled:', scheduleData)
        }}
      />

      {showPricing && (
        <Pricing onClose={() => setShowPricing(false)} />
      )}

      {showCVUpload && !results && (
        <CVUpload 
          onCVUpload={handleCVUpload}
          onManualEntry={handleManualEntry}
        />
      )}

      {showForm && !results && (
        <div className={`form-page ${showForm ? 'slide-up' : ''}`}>
          <button className="back-button" onClick={() => {
            setShowForm(false)
            setShowCVUpload(true)
          }}>
            ← CV Yükleme Ekranına Dön
          </button>
          <header className="app-header">
            <h1>🎓 Hynops</h1>
            <p>AI destekli üniversite eşleştirme ve başvuru yönetimi</p>
          </header>
          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}
          <InputForm onSubmit={handleSubmit} loading={loading} initialData={cvData} />
        </div>
      )}

      {results && (
        <div className="results-page">
          <CoreMetrics 
            gpa={coreMetrics.gpa}
            languageScore={coreMetrics.languageScore}
            backgroundMatch={coreMetrics.backgroundMatch}
          />
          <ResultsView 
            results={results} 
            onReset={handleReset}
            onShowPricing={() => setShowPricing(true)}
          />
        </div>
      )}
    </div>
  )
}

export default App

