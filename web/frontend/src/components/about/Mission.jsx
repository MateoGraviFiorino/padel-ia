import React from "react";

const Mission = () => {
  return (
    <>
      {/* Sección de la misión con un diseño suave y colores acogedores */}
      <section className="mb-20 p-12 bg-gradient-to-r from-pink-100 via-blue-100 to-purple-100 rounded-lg shadow-lg transform transition duration-300 hover:scale-105">
        <h2 className="text-4xl text-gray-800 font-semibold mb-6">
          Nuestra Misión
        </h2>
        <p className="text-xl text-gray-700 leading-relaxed">
          Nos comprometemos a transformar el presente mediante soluciones de
          inteligencia artificial accesibles, eficientes y con un enfoque
          humano. Creemos firmemente en un futuro donde
          la tecnología sea un puente hacia un mundo más inclusivo, equitativo
          y lleno de posibilidades.
        </p>
      </section>
    </>
  );
};

export default Mission;
