import { motion } from 'framer-motion'
import { Menu, X, GraduationCap, Sparkles } from 'lucide-react'
import { useState } from 'react'
import ThemeToggle from '../ui/ThemeToggle'

export default function Navbar({ onShowPricing }) {
  const [isOpen, setIsOpen] = useState(false)

  const navItems = [
    { name: 'Nasıl Çalışır', href: '#how-it-works' },
    { name: 'Özellikler', href: '#features' },
    { name: 'Fiyatlandırma', href: '#', onClick: onShowPricing },
  ]

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-950/80 
                 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <motion.a
            href="/"
            className="flex items-center gap-2 group"
            whileHover={{ scale: 1.02 }}
          >
            <div className="relative">
              <GraduationCap className="w-8 h-8 text-primary-600 dark:text-primary-400" />
              <Sparkles className="absolute -top-1 -right-1 w-3 h-3 text-amber-500" />
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              University<span className="text-primary-600 dark:text-primary-400">Match</span>
            </span>
          </motion.a>

          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <motion.a
                key={item.name}
                href={item.href}
                onClick={item.onClick}
                className="text-gray-600 dark:text-gray-300 hover:text-primary-600 
                         dark:hover:text-primary-400 font-medium transition-colors"
                whileHover={{ y: -2 }}
              >
                {item.name}
              </motion.a>
            ))}
            <ThemeToggle />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary text-sm"
            >
              Başla
            </motion.button>
          </div>

          <div className="flex items-center gap-4 md:hidden">
            <ThemeToggle />
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 text-gray-600 dark:text-gray-300"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800"
        >
          <div className="px-4 py-4 space-y-3">
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                onClick={(e) => {
                  if (item.onClick) {
                    e.preventDefault()
                    item.onClick()
                  }
                  setIsOpen(false)
                }}
                className="block py-2 text-gray-600 dark:text-gray-300 
                         hover:text-primary-600 dark:hover:text-primary-400 font-medium"
              >
                {item.name}
              </a>
            ))}
            <button className="w-full btn-primary text-sm mt-4">
              Başla
            </button>
          </div>
        </motion.div>
      )}
    </motion.nav>
  )
}
