import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, Play, FileVideo, Loader2, CheckCircle } from "lucide-react";
import padelApi from "../services/padelApi";

const VideoUploadSection = ({ onVideoUpload, onVideoProcessed, isProcessing }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [useRealApi, setUseRealApi] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file.type.startsWith('video/')) {
      setSelectedFile(file);
    } else {
      alert('Por favor selecciona un archivo de video válido');
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    onVideoUpload();
    
    try {
      if (useRealApi) {
        // Usar API real
        const result = await padelApi.uploadAndProcessVideo(selectedFile, setUploadProgress);
        onVideoProcessed(result);
      } else {
        // Usar simulación para desarrollo
        const result = await padelApi.simulateVideoProcessing(selectedFile, setUploadProgress);
        onVideoProcessed(result);
      }
    } catch (error) {
      console.error('Error processing video:', error);
      alert('Error al procesar el video. Por favor intenta de nuevo.');
    } finally {
      setUploadProgress(0);
      setSelectedFile(null);
    }
  };

  const testApiConnection = async () => {
    try {
      const health = await padelApi.checkHealth();
      console.log('API Health:', health);
      alert('API conectada exitosamente!');
      setUseRealApi(true);
    } catch (error) {
      console.error('API connection failed:', error);
      alert('No se pudo conectar con la API. Usando modo simulación.');
      setUseRealApi(false);
    }
  };

  return (
    <section className="py-20">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Analiza tu Partido
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Sube un video de tu partido de padel y obtén análisis detallado 
            con estadísticas de rendimiento, conteo de golpes y más.
          </p>
        </motion.div>

        {/* API Connection Test */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <button
            onClick={testApiConnection}
            className="text-sm text-gray-400 hover:text-white transition-colors duration-200 underline"
          >
            {useRealApi ? '✅ API Conectada' : '🔌 Probar Conexión API'}
          </button>
        </motion.div>

        <motion.div
          className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8 md:p-12"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
        >
          {/* Upload Area */}
          <div
            className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
              dragActive 
                ? 'border-green-400 bg-green-400/10' 
                : 'border-gray-600 hover:border-gray-500'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {!selectedFile ? (
              <>
                <Upload className="w-16 h-16 text-gray-400 mx-auto mb-6" />
                <h3 className="text-2xl font-semibold text-white mb-4">
                  Arrastra tu video aquí
                </h3>
                <p className="text-gray-400 mb-6">
                  O haz clic para seleccionar un archivo
                </p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-3 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300"
                >
                  Seleccionar Video
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="video/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </>
            ) : (
              <div className="space-y-6">
                <div className="flex items-center justify-center space-x-3">
                  <FileVideo className="w-8 h-8 text-green-400" />
                  <span className="text-white font-medium">{selectedFile.name}</span>
                </div>
                <p className="text-gray-400">
                  Archivo seleccionado: {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
                <button
                  onClick={handleUpload}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-3 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isProcessing ? (
                    <div className="flex items-center space-x-2">
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Procesando...</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2">
                      <Play className="w-5 h-5" />
                      <span>Analizar Video</span>
                    </div>
                  )}
                </button>
              </div>
            )}
          </div>

          {/* Progress Bar */}
          {isProcessing && (
            <motion.div
              className="mt-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                <span>
                  {useRealApi ? 'Procesando video con IA...' : 'Simulando procesamiento...'}
                </span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <motion.div
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${uploadProgress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </motion.div>
          )}

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 pt-12 border-t border-white/10">
            <div className="text-center">
              <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Play className="w-6 h-6 text-green-400" />
              </div>
              <h4 className="text-white font-semibold mb-2">Análisis Automático</h4>
              <p className="text-gray-400 text-sm">
                Procesamiento inteligente con IA
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-6 h-6 text-blue-400" />
              </div>
              <h4 className="text-white font-semibold mb-2">Resultados Precisos</h4>
              <p className="text-gray-400 text-sm">
                Estadísticas detalladas y confiables
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-6 h-6 text-purple-400" />
              </div>
              <h4 className="text-white font-semibold mb-2">Tiempo Real</h4>
              <p className="text-gray-400 text-sm">
                Análisis rápido y eficiente
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default VideoUploadSection;
