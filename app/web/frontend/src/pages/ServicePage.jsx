import React from "react";
import NavBar from "../components/NavBar";
import Footer from "../components/Footer";
import Services from "../components/services/Services";
import Projects from "../components/services/Projects";
import { Link } from "react-router-dom";

const ServicesPage = () => {
  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <Services />
        <Projects />
        {/* Botón de Contacto */}
        <div className="text-center mt-20">
          <Link
            to="/contact"
            className="bg-gradient-to-r from-[#9575CD] to-[#B388FF] py-3 px-8 rounded-md text-white transform hover:scale-105 transition duration-300"
          >
            ¡Contactanos!
          </Link>
        </div>

        <Footer />
      </div>
    </>
  );
};

export default ServicesPage;
