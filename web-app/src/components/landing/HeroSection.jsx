import { motion } from 'framer-motion'
import { ArrowRight, Sparkles, GraduationCap, Globe, Award, ChevronDown } from 'lucide-react'

export default function HeroSection({ onGetStarted, onManualEntry }) {
  const stats = [
    { value: '500+', label: 'Üniversite' },
    { value: '50+', label: 'Ülke' },
    { value: '10K+', label: 'Başarılı Eşleşme' },
    { value: '%95', label: 'Memnuniyet' },
  ]

  const floatingIcons = [
    { Icon: GraduationCap, delay: 0, position: 'top-20 left-[10%]' },
    { Icon: Globe, delay: 0.5, position: 'top-40 right-[15%]' },
    { Icon: Award, delay: 1, position: 'bottom-32 left-[20%]' },
    { Icon: Sparkles, delay: 1.5, position: 'top-32 right-[25%]' },
  ]

  return (
    <section className="relative min-h-screen overflow-hidden gradient-bg">
      {floatingIcons.map(({ Icon, delay, position }, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 0.2, y: 0 }}
          transition={{ delay, duration: 1 }}
          className={`absolute ${position} hidden md:block`}
        >
          <motion.div
            animate={{ y: [0, -20, 0] }}
            transition={{ duration: 4 + index, repeat: Infinity, ease: 'easeInOut' }}
          >
            <Icon className="w-12 h-12 text-white/30" />
          </motion.div>
        </motion.div>
      ))}

      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-white/10 dark:to-gray-950/50" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm 
                       rounded-full px-4 py-2 mb-8 border border-white/20"
          >
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span className="text-white/90 text-sm font-medium">
              AI Destekli Üniversite Eşleştirme
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white 
                       leading-tight tracking-tight mb-6"
          >
            Hayalindeki Üniversiteyi
            <br />
            <span className="bg-gradient-to-r from-amber-300 via-orange-300 to-amber-300 
                           bg-clip-text text-transparent">
              Keşfet
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto mb-10"
          >
            CV'ni yükle, yapay zeka profil analizini yapsın ve sana en uygun 
            yüksek lisans programlarını bulsun. Dakikalar içinde sonuç al.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
          >
            <motion.button
              onClick={onGetStarted}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="group flex items-center gap-2 px-8 py-4 bg-white text-primary-600 
                       font-semibold rounded-2xl shadow-lg shadow-black/20
                       hover:shadow-xl hover:shadow-black/30 transition-all duration-300"
            >
              CV Yükle ve Başla
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </motion.button>

            <motion.button
              onClick={onManualEntry}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 px-8 py-4 bg-white/10 text-white 
                       font-semibold rounded-2xl backdrop-blur-sm
                       border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              Manuel Giriş
            </motion.button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8 max-w-3xl mx-auto"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: 0.5 + index * 0.1 }}
                className="text-center"
              >
                <div className="text-3xl sm:text-4xl font-bold text-white mb-1">
                  {stat.value}
                </div>
                <div className="text-sm text-white/70">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <ChevronDown className="w-8 h-8 text-white/50" />
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
