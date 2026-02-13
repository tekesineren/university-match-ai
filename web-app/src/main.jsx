import React from 'react'
import ReactDOM from 'react-dom/client'
import { Capacitor } from '@capacitor/core'
import { SplashScreen } from '@capacitor/splash-screen'
import { StatusBar, Style } from '@capacitor/status-bar'
import App from './App'
import './index.css'

// Capacitor native ortamda ise platformu hazırla
const initApp = async () => {
  if (Capacitor.isNativePlatform()) {
    try {
      await StatusBar.setStyle({ style: Style.Light })
      await StatusBar.setBackgroundColor({ color: '#667eea' })
    } catch (e) {
      // StatusBar hatası önemsiz
    }
    try {
      await SplashScreen.hide()
    } catch (e) {
      // SplashScreen hatası önemsiz
    }
  }
}

initApp()

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

