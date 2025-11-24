import { useState } from 'react'
import './Pricing.css'

function Pricing({ onClose }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: 'forever',
      description: 'Başlamak için mükemmel',
      features: [
        '1 CV analizi/ay',
        '5 üniversite eşleştirme/gün',
        'Temel sonuçlar',
        'Email desteği'
      ],
      buttonText: 'Şu An Kullanıyorsunuz',
      buttonDisabled: true,
      popular: false
    },
    {
      name: 'Premium',
      price: '$9.99',
      period: 'ay',
      description: 'Ciddi başvurular için',
      features: [
        'Sınırsız CV analizi',
        '100 eşleştirme/gün',
        'Detaylı raporlar',
        'PDF export',
        'Öncelikli email desteği',
        'Gelişmiş filtreleme'
      ],
      buttonText: 'Premium\'a Geç',
      tier: 'premium',
      popular: true
    },
    {
      name: 'Pro',
      price: '$29.99',
      period: 'ay',
      description: 'Profesyoneller için',
      features: [
        'Premium\'un tüm özellikleri',
        'Sınırsız eşleştirme',
        'API erişimi',
        'Özel API key',
        'Webhook desteği',
        'Öncelikli teknik destek',
        'Özel entegrasyonlar'
      ],
      buttonText: 'Pro\'ya Geç',
      tier: 'pro',
      popular: false
    }
  ]

  const handleUpgrade = async (tier) => {
    setLoading(true)
    setError(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 
        (import.meta.env.DEV ? '/api' : 'https://master-application-agent-production.up.railway.app/api')
      
      const response = await fetch(`${apiUrl}/checkout/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tier })
      })

      const data = await response.json()

      if (data.success && data.checkout_url) {
        // Stripe Checkout sayfasına yönlendir
        window.location.href = data.checkout_url
      } else {
        setError(data.error || 'Checkout oluşturulamadı')
      }
    } catch (err) {
      console.error('Checkout error:', err)
      setError('Ödeme sayfası açılamadı. Lütfen tekrar deneyin.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="pricing-overlay" onClick={onClose}>
      <div className="pricing-container" onClick={(e) => e.stopPropagation()}>
        <button className="pricing-close" onClick={onClose}>×</button>
        
        <div className="pricing-header">
          <h2>Fiyatlandırma Planları</h2>
          <p>İhtiyacınıza uygun planı seçin</p>
        </div>

        {error && (
          <div className="pricing-error">
            ⚠️ {error}
          </div>
        )}

        <div className="pricing-plans">
          {plans.map((plan, index) => (
            <div 
              key={index} 
              className={`pricing-card ${plan.popular ? 'popular' : ''}`}
            >
              {plan.popular && <div className="popular-badge">En Popüler</div>}
              
              <div className="plan-header">
                <h3>{plan.name}</h3>
                <div className="plan-price">
                  <span className="price">{plan.price}</span>
                  <span className="period">/{plan.period}</span>
                </div>
                <p className="plan-description">{plan.description}</p>
              </div>

              <ul className="plan-features">
                {plan.features.map((feature, idx) => (
                  <li key={idx}>
                    <span className="check-icon">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <button
                className={`plan-button ${plan.popular ? 'popular-button' : ''} ${plan.buttonDisabled ? 'disabled' : ''}`}
                onClick={() => !plan.buttonDisabled && handleUpgrade(plan.tier)}
                disabled={plan.buttonDisabled || loading}
              >
                {loading ? 'Yönlendiriliyor...' : plan.buttonText}
              </button>
            </div>
          ))}
        </div>

        <div className="pricing-footer">
          <p>💳 Güvenli ödeme - Stripe ile korunuyor</p>
          <p>🔄 İstediğiniz zaman iptal edebilirsiniz</p>
          <p>❓ Sorularınız mı var? <a href="mailto:support@masterapplicationagent.com">Bizimle iletişime geçin</a></p>
        </div>
      </div>
    </div>
  )
}

export default Pricing










