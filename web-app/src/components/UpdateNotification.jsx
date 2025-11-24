import { useState, useEffect } from 'react'
import UpdateSchedule from './UpdateSchedule'
import './UpdateNotification.css'

const CURRENT_VERSION = '1.1' // This should match README.md version

function UpdateNotification({ onUpdate, onSchedule }) {
  const [showSchedule, setShowSchedule] = useState(false)
  const [latestVersion, setLatestVersion] = useState(null)
  const [isChecking, setIsChecking] = useState(true)
  const [showNotification, setShowNotification] = useState(false)

  useEffect(() => {
    checkForUpdates()
  }, [])

  const checkForUpdates = async () => {
    setIsChecking(true)
    
    // Get current version from localStorage
    const currentVersion = localStorage.getItem('app_version') || CURRENT_VERSION
    
    try {
      // Try to fetch version from GitHub API or a version endpoint
      // For now, we'll check against a version file or use the version from package.json
      // In production, you might want to create a /version endpoint on your backend
      
      // Simulate version check - in production, replace with actual API call
      const response = await fetch('/version.json', { cache: 'no-cache' })
        .catch(() => null)
      
      let fetchedVersion = CURRENT_VERSION
      
      if (response && response.ok) {
        const data = await response.json()
        fetchedVersion = data.version || CURRENT_VERSION
      } else {
        // Fallback: check if there's a newer version stored in localStorage (for testing)
        // In production, you'd fetch from your API
        fetchedVersion = CURRENT_VERSION
      }
      
      setLatestVersion(fetchedVersion)
      
      // Compare versions
      if (compareVersions(fetchedVersion, currentVersion) > 0) {
        // Check if user has dismissed or scheduled this update
        const dismissedUntil = localStorage.getItem('update_dismissed_until')
        const scheduledUpdate = localStorage.getItem('scheduled_update')
        
        if (dismissedUntil && new Date(dismissedUntil) > new Date()) {
          // Update is dismissed until a certain time
          setIsChecking(false)
          return
        }
        
        if (scheduledUpdate) {
          const scheduledDate = new Date(scheduledUpdate)
          if (scheduledDate > new Date()) {
            // Update is scheduled for later
            setIsChecking(false)
            return
          }
        }
        
        // Show update notification
        setIsChecking(false)
        setShowNotification(true)
      } else {
        setIsChecking(false)
        setShowNotification(false)
      }
    } catch (error) {
      console.error('Error checking for updates:', error)
      setIsChecking(false)
    }
  }

  const compareVersions = (v1, v2) => {
    const parts1 = v1.split('.').map(Number)
    const parts2 = v2.split('.').map(Number)
    
    for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
      const part1 = parts1[i] || 0
      const part2 = parts2[i] || 0
      
      if (part1 > part2) return 1
      if (part1 < part2) return -1
    }
    
    return 0
  }

  const handleUpdateNow = () => {
    localStorage.setItem('app_version', latestVersion)
    localStorage.removeItem('update_dismissed_until')
    localStorage.removeItem('scheduled_update')
    onUpdate?.()
    window.location.reload()
  }

  const handleScheduleUpdate = (scheduleData) => {
    onSchedule?.(scheduleData)
    
    if (scheduleData.type === 'never') {
      // Dismiss forever (until next major version)
      localStorage.setItem('update_dismissed_until', new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString())
    } else if (scheduleData.type === 'custom' && scheduleData.date) {
      localStorage.setItem('scheduled_update', scheduleData.date.toISOString())
    } else if (scheduleData.type === '15min') {
      localStorage.setItem('scheduled_update', new Date(Date.now() + 15 * 60 * 1000).toISOString())
    } else if (scheduleData.type === '60min') {
      localStorage.setItem('scheduled_update', new Date(Date.now() + 60 * 60 * 1000).toISOString())
    }
    
    setShowSchedule(false)
  }

  const currentVersion = localStorage.getItem('app_version') || CURRENT_VERSION
  
  // Don't show if no update available or still checking
  if (isChecking || !latestVersion || compareVersions(latestVersion, currentVersion) <= 0 || !showNotification) {
    return null
  }

  if (showSchedule) {
    return (
      <UpdateSchedule
        onSchedule={handleScheduleUpdate}
        onCancel={() => setShowSchedule(false)}
      />
    )
  }

  return (
    <div className="update-notification-overlay">
      <div className="update-notification">
        <div className="update-icon">🚀</div>
        <h2>Yeni Güncelleme Mevcut!</h2>
        <p className="update-version">
          Versiyon <strong>{currentVersion}</strong> → <strong>{latestVersion}</strong>
        </p>
        <p className="update-description">
          Yeni özellikler ve iyileştirmeler için uygulamayı güncelleyin.
        </p>
        
        <div className="update-actions">
          <button 
            className="update-button-primary"
            onClick={handleUpdateNow}
          >
            Şimdi Güncelle
          </button>
          <button 
            className="update-button-secondary"
            onClick={() => setShowSchedule(true)}
          >
            Sonra Güncelle
          </button>
        </div>
        
        <button 
          className="update-close"
          onClick={() => {
            // Dismiss for 24 hours
            localStorage.setItem('update_dismissed_until', new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString())
            setShowNotification(false)
          }}
          aria-label="Close"
        >
          ×
        </button>
      </div>
    </div>
  )
}

export default UpdateNotification

