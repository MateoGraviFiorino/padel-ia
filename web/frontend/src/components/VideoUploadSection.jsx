import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, Play, FileVideo, Loader2, Trophy, Users, Target } from "lucide-react";
import padelApi from "../services/padelApi";

const VideoUploadSection = ({ onVideoUpload, onVideoProcessed, isProcessing }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [useRealApi, setUseRealApi] = useState(false);
  const [videoResult, setVideoResult] = useState(null); // 👈 Nuevo estado para guardar el resultado
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
    if (file.type.startsWith("video/")) {
      setSelectedFile(file);
    } else {
      alert("Por favor selecciona un archivo de video válido");
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
      let result;
      if (useRealApi) {
        // Usar API real
        result = await padelApi.uploadAndProcessVideo(selectedFile, setUploadProgress);
      } else {
        // Usar simulación para desarrollo
        result = await padelApi.simulateVideoProcessing(selectedFile, setUploadProgress);
      }

      setVideoResult(result); // 👈 Guardamos el resultado en estado
      onVideoProcessed(result);

    } catch (error) {
      console.error("Error processing video:", error);
      alert("Error al procesar el video. Por favor intenta de nuevo.");
    } finally {
      setUploadProgress(0);
      setSelectedFile(null);
    }
  };

  const testApiConnection = async () => {
    try {
      const health = await padelApi.checkHealth();
      console.log("API Health:", health);
      alert("API conectada exitosamente!");
      setUseRealApi(true);
    } catch (error) {
      console.error("API connection failed:", error);
      alert("No se pudo conectar con la API. Usando modo simulación.");
      setUseRealApi(false);
    }
  };

  return (
    <section className="py-20">
      <div className="max-w-4xl mx-auto">
        {/* ... tu código de upload tal cual ... */}

        {/* ✅ Nuevo bloque: mostrar video procesado */}
        {videoResult?.processed_video_filename && (
          <motion.div
            className="mt-12"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h3 className="text-2xl font-bold text-white mb-4">
              Video Procesado con Análisis de IA
            </h3>
            <video
              src={`http://localhost:8000/videos/${videoResult.processed_video_filename}`}
              controls
              style={{ width: "100%", borderRadius: "12px" }}
            />
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default VideoUploadSection;
