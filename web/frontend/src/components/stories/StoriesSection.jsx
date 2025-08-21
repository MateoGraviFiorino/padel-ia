import React from "react";
import { ArrowRight } from "lucide-react";
import { caseStudies } from "../../constants";

export default function CaseStudiesSection() {
  return (
    <section className="w-full py-3 md:py-10 lg:py-10">
      <div className="container mx-auto px-4 md:px-6">
        <h2 className="text-4xl sm:text-6xl lg:text-7xl text-center tracking-wide animate-fadeIn mb-8">
         Nuestros Casos de Éxito
        </h2>
        <p className="text-gray-500 md:text-xl lg:text-base xl:text-xl text-center pb-10 mb-12">
         Conoce cómo nuestras soluciones innovadoras han impulsado el crecimiento y la transformación de empresas en una amplia variedad de sectores.
        </p>
        <div className="space-y-32">
          {caseStudies.map((study) => (
            <div
              key={study.id}
              className="flex flex-col items-start bg-radial-gradient-from-top-left from-v-soap via-v-primary to-v-pale-violet rounded-lg shadow-md overflow-hidden w-full max-w-4xl mx-auto transition-all duration-300 ease-in-out transform hover:scale-95 "
            >
              <img
                src={study.image}
                alt={`${study.company} case study`}
                className="w-full h-64 object-cover"
              />
              <div className="p-6">
                <h3 className="text-2xl text-v-text font-bold mb-2">
                  {study.company}
                </h3>
                <p className="text-v-raisin-black mb-4">{study.description}</p>
                <a
                  href={study.link}
                  className="inline-flex items-center text-blue-900 hover:text-blue-700 transition-colors"
                >
                  Read Case Study
                  <ArrowRight className="ml-2 h-4 w-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
