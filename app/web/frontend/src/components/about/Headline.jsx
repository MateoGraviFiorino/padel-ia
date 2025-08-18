import React from "react";

const Headline = () => {
  return (
    <>
      {/* Sección principal con un fondo decorativo */}
      <section className="text-center mb-20">
        <h1 className="text-4xl sm:text-6xl lg:text-7xl mb-6 bg-gradient-to-r from-v-pale-violet to-v-primary text-transparent bg-clip-text">
          Sobre Nosotros
        </h1>
        <p className="text-2xl text-v-text max-w-3xl mt-10 text-center max-w-4xl mx-auto">
          No hablamos del futuro, lo construimos.
        </p>
      </section>
    </>
  );
};

export default Headline;
