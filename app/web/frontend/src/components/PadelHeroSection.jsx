import React from "react";
import { motion } from "framer-motion";
import { Play, BarChart3, Target, Zap, Trophy, Users, Clock } from "lucide-react";

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
          <Trophy className="w-4 h-4" />
          <span className="text-sm font-medium">Análisis Profesional</span>
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
          Revoluciona tu juego de padel con análisis de video inteligente. 
          Detecta jugadores, cuenta golpes, mide velocidad y obtén estadísticas 
          detalladas para mejorar tu rendimiento en la pista.
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
              Sube tu partido y obtén análisis automático en minutos
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm">
            <Users className="w-12 h-12 text-blue-400 mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Detección de Jugadores</h3>
            <p className="text-gray-400 text-center text-sm">
              Identifica y rastrea a cada jugador en tiempo real
            </p>
          </div>
          
          <div className="flex flex-col items-center p-6 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm">
            <BarChart3 className="w-12 h-12 text-purple-400 mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Estadísticas Avanzadas</h3>
            <p className="text-gray-400 text-center text-sm">
              Métricas completas de rendimiento y duración
            </p>
          </div>
        </motion.div>

        {/* Additional Padel-Specific Features */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-4 max-w-5xl mx-auto mb-12"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <div className="flex flex-col items-center p-4 bg-white/5 rounded-xl border border-white/10">
            <Target className="w-8 h-8 text-green-400 mb-2" />
            <span className="text-sm text-gray-300 text-center">Conteo de Golpes</span>
          </div>
          
          <div className="flex flex-col items-center p-4 bg-white/5 rounded-xl border border-white/10">
            <Clock className="w-8 h-8 text-blue-400 mb-2" />
            <span className="text-sm text-gray-300 text-center">Tiempo de Juego</span>
          </div>
          
          <div className="flex flex-col items-center p-4 bg-white/5 rounded-xl border border-white/10">
            <Zap className="w-8 h-8 text-yellow-400 mb-2" />
            <span className="text-sm text-gray-300 text-center">Velocidad de Pelota</span>
          </div>
          
          <div className="flex flex-col items-center p-4 bg-white/5 rounded-xl border border-white/10">
            <Trophy className="w-8 h-8 text-purple-400 mb-2" />
            <span className="text-sm text-gray-300 text-center">Puntuación</span>
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
            Analizar mi Partido
          </button>
          <button className="border border-white/30 text-white py-4 px-8 rounded-full hover:bg-white/10 transition-all duration-300 font-semibold text-lg">
            Ver Ejemplo de Análisis
          </button>
        </motion.div>

        {/* Trust Indicators */}
        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.0, delay: 1.1 }}
        >
          <p className="text-gray-400 text-sm mb-4">Utilizado por jugadores profesionales y clubes de padel</p>
          <div className="flex justify-center space-x-8 text-gray-500">
            <span className="text-xs">🎾 Clubes de Padel</span>
            <span className="text-xs">🏆 Jugadores Profesionales</span>
            <span className="text-xs">📊 Entrenadores</span>
            <span className="text-xs">🎯 Academias</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PadelHeroSection;
