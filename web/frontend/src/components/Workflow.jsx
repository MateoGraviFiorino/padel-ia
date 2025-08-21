import React from "react";
import { CheckCircle2 } from "lucide-react";
import codeImg from "../assets/code.jpg";
import { checklistItems } from "../constants/index.jsx";

const Workflow = () => {
  return (
    <div className="mt-20">
      {/* Título principal con gradiente */}
      <h2 className="text-3xl sm:text-5xl lg:text-6xl text-center mt-6 tracking-wide text-white">
        Mejorá la experiencia de
        <span className="bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
          {" "}tus usuarios
        </span>
      </h2>

      <div className="mt-10 flex flex-wrap justify-center items-center">
        {/* Imagen del código con animación */}
        <div className="relative p-4 w-full lg:w-1/2">
          <img
            src={codeImg}
            alt="Code"
            className="rounded-lg shadow-lg transform hover:scale-105 transition duration-300 ease-in-out"
          />
        </div>

        {/* Listado de items con recuadros e íconos */}
        <div className="pt-12 w-full lg:w-1/2">
          {checklistItems.map((item, index) => (
            <div
              key={index}
              className="flex items-start mb-8 p-4 bg-neutral-900 rounded-lg shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"  // Recuadro y sombra con animación hover
            >
              <div className="text-green-400 mx-4 h-12 w-12 p-2 flex justify-center items-center rounded-full shadow-lg transform hover:scale-110 transition duration-300">
                <CheckCircle2 size={24} />
              </div>
              <div>
                <h5 className="mt-1 mb-2 text-xl font-semibold text-white">
                  {item.title}
                </h5>
                <p className="text-neutral-400">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Workflow;