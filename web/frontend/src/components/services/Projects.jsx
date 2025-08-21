import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { projects } from "../../constants";

const Projects = () => {
  return (
    <>
      {/* Sección de Proyectos (Agrandar las tarjetas del carrusel) */}
      <div className="text-center mt-20">
        <h2 className="text-4xl sm:text-5xl lg:text-6xl tracking-wide">
          Nuestros{" "}
          <span className="bg-gradient-to-r from-[#9575CD] to-[#B388FF] text-transparent bg-clip-text">
            Casos de Éxito
          </span>
        </h2>
        <p className="mt-6 text-xl lg:text-2xl text-[#9E9E9E] max-w-6xl mx-auto">
          Descubre algunos de nuestros proyectos más destacados y cómo hemos ayudado a diversas empresas a alcanzar sus objetivos con soluciones de inteligencia artificial personalizadas
        </p>
      </div>

      {/* Swiper Carrusel Moderno con la Paleta de Colores Existente */}
      <Swiper
        modules={[Navigation, Pagination, Autoplay]}
        spaceBetween={30}
        slidesPerView={1}
        navigation
        pagination={{ clickable: true }}
        autoplay={{ delay: 5000 }}
        className="mt-16"
      >
        {projects.map((project, index) => (
          <SwiperSlide key={index}>
            <div className="p-16 rounded-lg shadow-xl text-center bg-[#212121] bg-opacity-80 relative overflow-hidden transform hover:scale-105 transition duration-300"> {/* Aumentamos el padding */}
              <div className="relative z-10">
                <div className="w-full h-64 mb-6 bg-[#424242]"></div> {/* Aumentamos el tamaño del placeholder de la imagen */}
                <h3 className="text-4xl text-[#B388FF] font-semibold mb-2"> {/* Aumentamos el tamaño del título */}
                  {project.title}
                </h3>
                <p className="text-xl text-[#9E9E9E]">{project.description}</p> {/* Aumentamos el tamaño del texto */}
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </>
  );
};

export default Projects;
