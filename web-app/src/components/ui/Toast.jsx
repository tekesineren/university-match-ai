import { Toaster } from 'react-hot-toast'

export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: 'var(--toast-bg, #fff)',
          color: 'var(--toast-color, #1f2937)',
          padding: '16px',
          borderRadius: '12px',
          boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        },
        success: {
          iconTheme: {
            primary: '#10b981',
            secondary: '#fff',
          },
          style: {
            border: '1px solid #10b981',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444',
            secondary: '#fff',
          },
          style: {
            border: '1px solid #ef4444',
          },
        },
        loading: {
          iconTheme: {
            primary: '#6366f1',
            secondary: '#fff',
          },
        },
      }}
    />
  )
}

export { toast } from 'react-hot-toast'
