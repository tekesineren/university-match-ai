import { Capacitor } from '@capacitor/core'

/**
 * Capacitor ortamında mı çalışıyoruz kontrol et
 */
export const isNativeApp = () => {
  return Capacitor.isNativePlatform()
}

/**
 * API base URL'ini ortama göre belirle
 * - Capacitor (iOS app): Doğrudan production backend URL'i kullan
 * - Web development: Vite proxy kullan (/api)
 * - Web production: Production backend URL'i kullan
 */
export const getApiUrl = () => {
  // Env variable varsa her zaman onu kullan
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }

  // Capacitor native app ise doğrudan production URL kullan
  if (isNativeApp()) {
    return 'https://hynops.com/api'
  }

  // Web development modunda Vite proxy kullan
  if (import.meta.env.DEV) {
    return '/api'
  }

  // Web production
  return 'https://hynops.com/api'
}
