import React from "react";
import { services } from "../../constants";

const Services = () => {
  return (
    <>
      {/* Sección de Servicios */}
      <div className="text-center mt-10">
        <h1 className="text-4xl sm:text-6xl lg:text-7xl tracking-wide">
          En{" "}
          <span className="bg-gradient-to-r from-[#9575CD] to-[#B388FF] text-transparent bg-clip-text">
            Vanguard
          </span>{" "}
          ofrecemos
          </h1>
          <p className="mt-6 text-xl lg:text-2xl text-[#9E9E9E] max-w-8xl mx-auto"> {/* Aumentar tamaño del texto */}
            Vanguard es una empresa líder en consultoría de inteligencia artificial. Nuestro equipo de expertos se compromete a desarrollar soluciones innovadoras y personalizadas que se adapten a las necesidades únicas de tu negocio.
          </p>
      </div>

      {/* Tarjetas de Servicios */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-12 mt-16"> {/* Aumentar el gap */}
      {services.map((service, index) => (
        <div
          key={index}
          className="p-8 rounded-lg shadow-lg text-center transform hover:scale-105 transition duration-300 bg-[#212121]" 
        >
            <h2 className="text-3xl text-[#B388FF] mb-6">{service.title}</h2>
            <p className="text-lg text-[#9E9E9E]">{service.description}</p>
          </div>
        ))}
      </div>
    </>
  );
};

export default Services;
