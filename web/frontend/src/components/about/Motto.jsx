import React from "react";

const Motto = () => {
  return (
    <>
      {/* Sección del lema con un diseño elegante */}
      <section className="text-center mb-20 bg-[#1e293b] p-12 rounded-lg shadow-lg transform transition duration-300 hover:scale-105">
        <h2 className="text-4xl font-semibold mb-6 text-[#B388FF]">
          Nuestro Lema
        </h2>
        <p className="text-2xl italic text-[#9575CD]">
          "No hablamos de futuro, lo creamos."
        </p>
      </section>
    </>
  );
};

export default Motto;
