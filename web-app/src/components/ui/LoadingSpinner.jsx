import { motion } from 'framer-motion'

export function LoadingSpinner({ size = 'md', color = 'primary' }) {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
    xl: 'w-16 h-16 border-4',
  }

  const colors = {
    primary: 'border-primary-500/30 border-t-primary-500',
    white: 'border-white/30 border-t-white',
    gray: 'border-gray-400/30 border-t-gray-400',
  }

  return (
    <div
      className={`${sizes[size]} ${colors[color]} rounded-full animate-spin`}
    />
  )
}

export function LoadingDots({ color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-500',
    white: 'bg-white',
    gray: 'bg-gray-400',
  }

  return (
    <div className="flex items-center gap-1">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className={`w-2 h-2 rounded-full ${colors[color]}`}
          initial={{ opacity: 0.3, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{
            duration: 0.5,
            repeat: Infinity,
            repeatType: 'reverse',
            delay: i * 0.15,
          }}
        />
      ))}
    </div>
  )
}

export function LoadingOverlay({ message = 'Loading...' }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center 
                 bg-black/50 backdrop-blur-sm"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white dark:bg-gray-900 rounded-2xl p-8 shadow-2xl
                   flex flex-col items-center gap-4"
      >
        <LoadingSpinner size="lg" />
        <p className="text-gray-600 dark:text-gray-300 font-medium">{message}</p>
      </motion.div>
    </motion.div>
  )
}

export function SkeletonLoader({ className = '' }) {
  return (
    <div className={`relative overflow-hidden bg-gray-200 dark:bg-gray-800 rounded-lg ${className}`}>
      <motion.div
        className="absolute inset-0 -translate-x-full bg-gradient-to-r 
                   from-transparent via-white/20 to-transparent"
        animate={{ translateX: '100%' }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
    </div>
  )
}

export function PageLoader() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center gradient-bg">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center gap-6"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-16 h-16 rounded-full border-4 border-white/30 border-t-white"
        />
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-white text-xl font-semibold"
        >
          University Match AI
        </motion.h2>
        <LoadingDots color="white" />
      </motion.div>
    </div>
  )
}
