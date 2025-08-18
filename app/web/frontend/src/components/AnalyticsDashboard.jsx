import React from "react";
import { motion } from "framer-motion";
import { 
  BarChart3, 
  Clock, 
  Play, 
  Target, 
  TrendingUp, 
  Users,
  Zap,
  Activity
} from "lucide-react";

const AnalyticsDashboard = ({ matchData }) => {
  if (!matchData) return null;

  const formatDuration = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const formatFPS = (fps) => {
    return `${fps.toFixed(1)} FPS`;
  };

  const stats = [
    {
      icon: Target,
      label: "Total de Golpes",
      value: matchData.total_hits,
      color: "from-green-500 to-green-600",
      bgColor: "bg-green-500/20",
      borderColor: "border-green-500/30"
    },
    {
      icon: Clock,
      label: "Duración",
      value: formatDuration(matchData.video_duration),
      color: "from-blue-500 to-blue-600",
      bgColor: "bg-blue-500/20",
      borderColor: "border-blue-500/30"
    },
    {
      icon: Play,
      label: "Frames Totales",
      value: matchData.total_frames.toLocaleString(),
      color: "from-purple-500 to-purple-600",
      bgColor: "bg-purple-500/20",
      borderColor: "border-purple-500/30"
    },
    {
      icon: Activity,
      label: "FPS",
      value: formatFPS(matchData.fps),
      color: "from-orange-500 to-orange-600",
      bgColor: "bg-orange-500/20",
      borderColor: "border-orange-500/30"
    }
  ];

  return (
    <motion.section
      className="py-20"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.h2
            className="text-4xl md:text-5xl font-bold text-white mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Resultados del Análisis
          </motion.h2>
          <motion.p
            className="text-xl text-gray-300 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            Estadísticas detalladas de tu partido de padel
          </motion.p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              className={`${stat.bgColor} ${stat.borderColor} border rounded-2xl p-6 backdrop-blur-sm`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-400">{stat.label}</p>
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Detailed Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Player Performance */}
          <motion.div
            className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-8"
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <Users className="w-6 h-6 text-blue-400" />
              <h3 className="text-2xl font-bold text-white">Rendimiento por Jugador</h3>
            </div>
            
            <div className="space-y-4">
              {Object.entries(matchData.hits_per_player).map(([player, hits], index) => (
                <div key={player} className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <span className="text-white font-medium">{player}</span>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-blue-400">{hits}</p>
                    <p className="text-sm text-gray-400">golpes</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Match Summary */}
          <motion.div
            className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-8"
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="flex items-center space-x-3 mb-6">
              <BarChart3 className="w-6 h-6 text-green-400" />
              <h3 className="text-2xl font-bold text-white">Resumen del Partido</h3>
            </div>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                <div className="flex items-center space-x-3">
                  <Zap className="w-5 h-5 text-yellow-400" />
                  <span className="text-gray-300">Intensidad del Juego</span>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-white">
                    {((matchData.total_hits / matchData.video_duration) * 60).toFixed(1)}
                  </p>
                  <p className="text-sm text-gray-400">golpes/min</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                <div className="flex items-center space-x-3">
                  <TrendingUp className="w-5 h-5 text-green-400" />
                  <span className="text-gray-300">Eficiencia</span>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-white">
                    {((matchData.total_hits / matchData.total_frames) * 100).toFixed(1)}%
                  </p>
                  <p className="text-sm text-gray-400">de frames activos</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                <div className="flex items-center space-x-3">
                  <Play className="w-5 h-5 text-purple-400" />
                  <span className="text-gray-300">Archivo</span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-white truncate max-w-32">
                    {matchData.filename}
                  </p>
                  <p className="text-sm text-gray-400">video procesado</p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Action Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6 mt-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <button className="bg-gradient-to-r from-green-500 to-blue-500 text-white py-4 px-8 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300 font-semibold text-lg">
            Descargar Reporte
          </button>
          <button className="border border-white/30 text-white py-4 px-8 rounded-full hover:bg-white/10 transition-all duration-300 font-semibold text-lg">
            Analizar Otro Video
          </button>
        </motion.div>
      </div>
    </motion.section>
  );
};

export default AnalyticsDashboard;
