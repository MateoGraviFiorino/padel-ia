import React from "react";
import { valuesBackground } from "../../constants";

const Background = () => {
  return (
    <>
      {/* Sección de valores con íconos o imágenes opcionales */}
      <section className="mt-6 lg:mt-15 mb-20">
        <h2 className="text-4xl sm:text-6xl lg:text-7xl mb-20 text-center">
          Nuestros Valores
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {valuesBackground.map((value, index) => (
            <div class="flex items-center justify-center rounded-md">
              <div key={index} className={value.backgroundStyle}>
                <div className="flex mb-4">
                  <div className="flex h-12 w-12 p-2 bg-neutral-700 text-v-primary justify-center items-center rounded-full">
                    {value.icon}
                  </div>
                </div>
                <h3 className="text-2xl font-semibold mb-4 text-v-text">
                  {value.title}
                </h3>
                <p className="text-lg text-v-spanish-gray">
                  {value.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </>
  );
};

export default Background;
