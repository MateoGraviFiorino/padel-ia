import React from "react";
import { motion } from "framer-motion";
import { Play, BarChart3, Target, Zap } from "lucide-react";

const PadelHeroSection = () => {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen p-10">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-green-400/20 to-blue-500/20"></div>
        <div className="absolute top-20 left-20 w-32 h-32 bg-green-400/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-20 w-40 h-40 bg-blue-400/30 rounded-full blur-3xl"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center">
        {/* Badge */}
        <motion.div
          className="inline-flex items-center space-x-2 bg-green-500/20 border border-green-400/30 text-green-300 px-4 py-2 rounded-full mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Zap className="w-4 h-4" />
          <span className="text-sm font-medium">Powered by AI</span>
        </motion.div>

        {/* Main Title */}
        <motion.h1
          className="text-5xl sm:text-7xl lg:text-8xl text-center tracking-wide text-white mb-8"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Análisis de{" "}
          <span className="bg-gradient-to-r from-green-400 to-blue-600 text-transparent bg-clip-text">
            Padel
          </span>{" "}
          con IA
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          className="text-xl text-center text-gray-300 max-w-4xl leading-relaxed mb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.0, delay: 0.3 }}
        >
          Analiza tus partidos de padel con tecnología de vanguardia. 
          Detecta jugadores, cuenta golpes, mide velocidad y obtén estadísticas 
          detalladas para mejorar tu juego.
        </motion.p>

        {/* Features Grid */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <div className="flex flex-col items-center p-6 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm">
            <Play className="w-12 h-12 text-green-400 mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Análisis de Video</h3>
            <p className="text-gray-400 text-center text-sm">
              Sube tu video y obtén análisis automático
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm">
            <Target className="w-12 h-12 text-blue-400 mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Detección de Jugadores</h3>
            <p className="text-gray-400 text-center text-sm">
              Identifica y rastrea a cada jugador
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm">
            <BarChart3 className="w-12 h-12 text-purple-400 mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Estadísticas Detalladas</h3>
            <p className="text-gray-400 text-center text-sm">
              Métricas completas de rendimiento
            </p>
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.9 }}
        >
          <button className="bg-gradient-to-r from-green-500 to-blue-500 text-white py-4 px-8 rounded-full shadow-lg transform hover:scale-105 hover:from-green-600 hover:to-blue-600 transition-all duration-300 font-semibold text-lg">
            Comenzar Análisis
          </button>
          <button className="border border-white/30 text-white py-4 px-8 rounded-full hover:bg-white/10 transition-all duration-300 font-semibold text-lg">
            Ver Demo
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default PadelHeroSection;
