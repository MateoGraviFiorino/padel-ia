import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const HeroSection = () => {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen p-10"> {/* Asegurar altura completa */}
      {/* Título principal con animación */}
      <motion.h1
        className="text-5xl sm:text-7xl lg:text-8xl text-center tracking-wide text-white"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Impulsa tu empresa con{" "}
        <span className="bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
          Inteligencia Artificial
        </span>
      </motion.h1>

      {/* Descripción animada */}
      <motion.p
        className="mt-10 text-xl text-center text-gray-300 max-w-4xl leading-relaxed"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.0, delay: 0.5 }}
      >
        Analizamos tus oportunidades y desarrollamos soluciones de vanguardia
        para hacer de tu negocio más productivo y eficiente.
      </motion.p>

      {/* Botón CTA */}
      <motion.div
        className="flex justify-center my-10"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 1.0 }}
      >
        <Link
          to="/contact"
          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-8 mx-3 rounded-full shadow-lg transform hover:scale-110 hover:bg-gradient-to-l hover:from-pink-500 hover:to-purple-500 transition duration-300"
        >
          ¡Inicia acá tu camino con nosotros!
        </Link>
      </motion.div>
    </div>
  );
};

export default HeroSection;
