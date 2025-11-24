import { useState } from 'react'
import './UpdateSchedule.css'

function UpdateSchedule({ onSchedule, onCancel }) {
  const [selectedOption, setSelectedOption] = useState(null)
  const [customDate, setCustomDate] = useState('')
  const [customTime, setCustomTime] = useState('')

  const handleOptionSelect = (option) => {
    setSelectedOption(option)
    if (option !== 'custom') {
      setCustomDate('')
      setCustomTime('')
    }
  }

  const handleSchedule = () => {
    if (!selectedOption) {
      alert('Lütfen bir seçenek seçin')
      return
    }

    if (selectedOption === 'custom') {
      if (!customDate || !customTime) {
        alert('Lütfen tarih ve saat seçin')
        return
      }

      const [year, month, day] = customDate.split('-')
      const [hour, minute] = customTime.split(':')
      const scheduleDate = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hour),
        parseInt(minute),
        0
      )

      if (scheduleDate <= new Date()) {
        alert('Gelecekteki bir tarih seçmelisiniz')
        return
      }

      onSchedule({
        type: 'custom',
        date: scheduleDate
      })
    } else {
      onSchedule({
        type: selectedOption
      })
    }
    
    // Close the schedule modal
    onCancel?.()
  }

  // Calculate min date/time (now + 1 minute)
  const getMinDateTime = () => {
    const now = new Date()
    now.setMinutes(now.getMinutes() + 1)
    return {
      date: now.toISOString().split('T')[0],
      time: now.toTimeString().slice(0, 5)
    }
  }

  const minDateTime = getMinDateTime()

  return (
    <div className="update-schedule-overlay">
      <div className="update-schedule">
        <div className="update-icon">⏰</div>
        <h2>Güncellemeyi Planla</h2>
        <p className="schedule-description">
          Güncellemeyi ne zaman yapmak istersiniz?
        </p>

        <div className="schedule-options">
          <label className={`schedule-option ${selectedOption === '15min' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="schedule"
              value="15min"
              checked={selectedOption === '15min'}
              onChange={() => handleOptionSelect('15min')}
            />
            <div className="option-content">
              <span className="option-icon">⏱️</span>
              <div>
                <div className="option-title">15 Dakika Sonra</div>
                <div className="option-time">
                  {new Date(Date.now() + 15 * 60 * 1000).toLocaleTimeString('tr-TR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            </div>
          </label>

          <label className={`schedule-option ${selectedOption === '60min' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="schedule"
              value="60min"
              checked={selectedOption === '60min'}
              onChange={() => handleOptionSelect('60min')}
            />
            <div className="option-content">
              <span className="option-icon">⏰</span>
              <div>
                <div className="option-title">1 Saat Sonra</div>
                <div className="option-time">
                  {new Date(Date.now() + 60 * 60 * 1000).toLocaleTimeString('tr-TR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            </div>
          </label>

          <label className={`schedule-option ${selectedOption === 'never' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="schedule"
              value="never"
              checked={selectedOption === 'never'}
              onChange={() => handleOptionSelect('never')}
            />
            <div className="option-content">
              <span className="option-icon">🚫</span>
              <div>
                <div className="option-title">Hiçbir Zaman</div>
                <div className="option-time">Bu güncellemeyi gösterme</div>
              </div>
            </div>
          </label>

          <label className={`schedule-option ${selectedOption === 'custom' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="schedule"
              value="custom"
              checked={selectedOption === 'custom'}
              onChange={() => handleOptionSelect('custom')}
            />
            <div className="option-content">
              <span className="option-icon">📅</span>
              <div>
                <div className="option-title">Özel Zaman</div>
                <div className="option-time">Kendi zamanınızı seçin</div>
              </div>
            </div>
          </label>
        </div>

        {selectedOption === 'custom' && (
          <div className="custom-datetime">
            <div className="datetime-row">
              <label>
                <span className="datetime-label">📅 Tarih</span>
                <input
                  type="date"
                  value={customDate}
                  onChange={(e) => setCustomDate(e.target.value)}
                  min={minDateTime.date}
                  className="datetime-input"
                />
              </label>
              <label>
                <span className="datetime-label">🕐 Saat</span>
                <input
                  type="time"
                  value={customTime}
                  onChange={(e) => setCustomTime(e.target.value)}
                  min={customDate === minDateTime.date ? minDateTime.time : undefined}
                  className="datetime-input"
                />
              </label>
            </div>
            {customDate && customTime && (
              <div className="datetime-preview">
                Güncelleme zamanı:{' '}
                <strong>
                  {new Date(
                    `${customDate}T${customTime}`
                  ).toLocaleString('tr-TR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </strong>
              </div>
            )}
          </div>
        )}

        <div className="schedule-actions">
          <button
            className="schedule-button-primary"
            onClick={handleSchedule}
          >
            Planla
          </button>
          <button
            className="schedule-button-secondary"
            onClick={onCancel}
          >
            İptal
          </button>
        </div>

        <button
          className="schedule-close"
          onClick={onCancel}
          aria-label="Close"
        >
          ×
        </button>
      </div>
    </div>
  )
}

export default UpdateSchedule

