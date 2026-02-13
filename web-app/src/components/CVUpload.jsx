import { useState, useRef } from 'react'
import { validateCVFile, extractTextFromFile, validateCVContent } from '../utils/cvParser'
import { getApiUrl } from '../utils/api'
import './CVUpload.css'

// Helper function for status error messages
function getStatusErrorMessage(status) {
  switch (status) {
    case 403:
      return 'Erişim reddedildi. Backend çalışıyor mu ve CORS ayarları doğru mu?'
    case 404:
      return 'API endpoint bulunamadı. Backend doğru portta çalışıyor mu?'
    case 429:
      return 'Rate limit aşıldı. Biraz bekleyin veya users.json dosyasını sıfırlayın.'
    case 500:
      return 'Backend hatası. Backend loglarını kontrol edin.'
    default:
      return 'Bilinmeyen hata. Backend çalışıyor mu?'
  }
}

function CVUpload({ onCVUpload, onManualEntry }) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleDragEnter = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = async (file) => {
    setError(null)
    console.log('📄 CV yükleme başladı:', file.name, file.type, file.size)
    
    // 1. Dosya validasyonu
    const validation = validateCVFile(file)
    if (!validation.valid) {
      console.error('❌ Dosya validasyonu başarısız:', validation.error)
      setError(validation.error)
      return
    }
    
    setIsProcessing(true)
    setUploadedFile(file)
    
    try {
      // 2. Dosyayı backend'e gönder ve parse et
      const formData = new FormData()
      formData.append('cv', file)
      
      // API URL'i belirle
      const apiUrl = getApiUrl()
      
      console.log('🌐 API URL:', apiUrl)
      console.log('📤 Backend\'e gönderiliyor...')
      
      const response = await fetch(`${apiUrl}/parse-cv`, {
        method: 'POST',
        body: formData
      })
      
      console.log('📥 Response status:', response.status, response.statusText)
      
      if (!response.ok) {
        let errorMessage = `CV analiz edilemedi (${response.status}). `
        
        try {
          const errorData = await response.json()
          if (errorData.error) {
            errorMessage += errorData.error
          } else {
            errorMessage += getStatusErrorMessage(response.status)
          }
          
          // Rate limit hatası için özel mesaj
          if (response.status === 429 || errorData.rate_limit_exceeded) {
            errorMessage += '\n\n💡 Çözüm: Backend klasöründe users.json dosyasını silerek limitleri sıfırlayabilirsiniz.'
          }
          
          // 403 hatası için detaylı açıklama
          if (response.status === 403) {
            errorMessage += '\n\n🔧 Olası Çözümler:\n'
            errorMessage += '1. Backend çalışıyor mu? (http://localhost:5000/api/health kontrol edin)\n'
            errorMessage += '2. CORS ayarları doğru mu? Backend\'i yeniden başlatmayı deneyin\n'
            errorMessage += '3. Rate limit aşıldı mı? users.json dosyasını silin'
          }
        } catch (e) {
          const errorText = await response.text()
          errorMessage += getStatusErrorMessage(response.status)
          if (errorText) {
            console.error('❌ Response error:', errorText)
          }
        }
        
        throw new Error(errorMessage)
      }
      
      const data = await response.json()
      console.log('✅ Backend response:', data)
      
      if (!data.success) {
        console.error('❌ Backend success=false:', data.error)
        throw new Error(data.error || 'CV içeriği analiz edilemedi')
      }
      
      // 3. CV içeriği validasyonu
      if (data.extracted_text) {
        const contentValidation = validateCVContent(data.extracted_text)
        if (!contentValidation.valid) {
          console.warn('⚠️ CV içerik validasyonu başarısız:', contentValidation.error)
          setError(contentValidation.error)
          setIsProcessing(false)
          // Dosyayı silme, kullanıcı manuel giriş yapabilir
          return
        }
      }
      
      console.log('✅ CV başarıyla parse edildi:', data.extracted_data)
      
      // 4. Başarılı - CV verilerini gönder
      setIsProcessing(false)
      onCVUpload(file, data.extracted_data || {})
      
    } catch (err) {
      console.error('❌ CV parsing error:', err)
      console.error('Error details:', {
        message: err.message,
        stack: err.stack,
        name: err.name
      })
      
      // Daha detaylı hata mesajı
      let errorMessage = err.message || 'CV analiz edilirken bir hata oluştu.'
      
      if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        errorMessage = `🔴 Backend'e bağlanılamadı!

Çözüm adımları:
1. Backend çalışıyor mu? Terminal'de 'cd backend && python app.py' çalıştırın
2. http://localhost:5000/api/health adresini tarayıcıda açın
3. Backend'in 5000 portunda çalıştığını doğrulayın

Lütfen manuel giriş yapın veya backend'i başlattıktan sonra tekrar deneyin.`
      }
      
      setError(errorMessage)
      setIsProcessing(false)
      // Dosyayı silme, kullanıcı tekrar deneyebilir
    }
  }

  return (
    <div className="cv-upload-container">
      <div className="cv-upload-header">
        <h1>🎓 Master Application Agent</h1>
        <p className="subtitle">CV'nizi yükleyin, size en uygun üniversiteleri bulalım</p>
      </div>

      <div 
        className={`cv-upload-area ${isDragging ? 'dragging' : ''} ${uploadedFile ? 'uploaded' : ''}`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !uploadedFile && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        {!uploadedFile ? (
          <>
            <div className="upload-icon">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <h2>CV'nizi buraya sürükleyin</h2>
            <p>veya tıklayarak seçin</p>
            <div className="file-formats">
              <span>PDF, DOC, DOCX</span>
            </div>
          </>
        ) : (
          <>
            <div className="upload-success">
              <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <h2>{isProcessing ? 'CV Analiz Ediliyor...' : 'CV Başarıyla Yüklendi!'}</h2>
            <p className="file-name">{uploadedFile.name}</p>
            <p className="processing">
              {isProcessing ? 'CV içeriği çıkarılıyor ve doğrulanıyor...' : 'Bilgileriniz analiz ediliyor...'}
            </p>
            {error && (
              <div className="error-message-cv" style={{ 
                marginTop: '15px', 
                padding: '10px', 
                background: '#fee2e2', 
                color: '#dc2626', 
                borderRadius: '8px',
                fontSize: '0.9rem'
              }}>
                ⚠️ {error}
              </div>
            )}
          </>
        )}
      </div>

      <div className="auto-info">
        <div className="info-icon">✨</div>
        <p>
          <strong>Otomatik Analiz:</strong> CV'nizden tüm bilgiler otomatik olarak çıkarılacak 
          (GPA, dil skorları, araştırma/iş deneyimi, background, yayınlar). 
          Hiçbir şey manuel girmenize gerek kalmayacak!
        </p>
      </div>

      <button 
        className="manual-entry-btn"
        onClick={onManualEntry}
        disabled={uploadedFile !== null}
      >
        📝 Manuel Giriş Yap
      </button>
    </div>
  )
}

export default CVUpload

