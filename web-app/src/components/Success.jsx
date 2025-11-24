import { useEffect, useState } from 'react'
import './Success.css'

function Success() {
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // URL'den session_id'yi al
    const params = new URLSearchParams(window.location.search)
    const id = params.get('session_id')
    setSessionId(id)
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="success-page">
        <div className="success-container">
          <div className="loading-spinner">⏳</div>
          <p>Ödeme işleniyor...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="success-page">
      <div className="success-container">
        <div className="success-icon">✅</div>
        <h1>Ödeme Başarılı!</h1>
        <p>Premium üyeliğiniz aktif edildi.</p>
        <p className="success-message">
          Artık sınırsız CV analizi ve gelişmiş özelliklere erişebilirsiniz.
        </p>
        <div className="success-actions">
          <a href="/" className="success-button">
            Ana Sayfaya Dön
          </a>
          <a href="/#pricing" className="success-button secondary">
            Planları Görüntüle
          </a>
        </div>
        {sessionId && (
          <p className="success-session">
            Session ID: {sessionId}
          </p>
        )}
      </div>
    </div>
  )
}

export default Success

