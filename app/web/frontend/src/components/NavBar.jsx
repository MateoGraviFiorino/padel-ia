import React, { useState } from "react";
import { Menu, X } from "lucide-react";
import logo from "../assets/vanguard-logo.png";
import { navItems } from "../constants/";
import { Outlet, Link } from "react-router-dom";

const NavBar = () => {
  // state para abrir la lista en el caso de pantalla restringida (o mobile)
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const toggleNavBar = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };
  return (
    // Barra de navegación
    <nav className="sticky top-0 z-50 py-3 backdrop-blur-lg border-b border-neutral-700/80">
      {/* Container donde se vuelcan los elementos de la barra */}
      <div className="container px-4 mx-auto relative text-sm">
        {/* Se centran los elementos horizontal y verticalmente */}
        <div className="flex justify-between items-center">
          {/* div que contiene el ícono nombre de la empresa */}
          <div className="flex items-center flex-shrink-0">
            <img className="h-10 w-10 mr-2" src={logo} alt="logo" />
            <span className="text-xl tracking-tight">Vanguard</span>
          </div>
          {/* lista con las secciones de la página */}
          <div className="flex-grow flex justify-center">
            <ul className="hidden lg:flex ml-14 space-x-12">
              {navItems.map((item, index) => (
                <li key={index}>
                  <Link to={item.href}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </div>
          {/* Placeholder div that mimics the width of the logo div */}
          <div className="hidden lg:flex items-center flex-shrink-0">
            <div className="h-10 w-20 mr-2"></div>
            <span className="invisible text-xl tracking-tight">Vanguard</span>
          </div>
          <div className="lg:hidden md:flex flex-col justify-end">
            <button onClick={toggleNavBar}>
              {mobileDrawerOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
        {mobileDrawerOpen && (
          <div className="fixed right-0 z-20 bg-neutral-900 w-full p-12 flex flex-col justify-center items-center lg:hidden">
            <ul>
              {navItems.map((item, index) => (
                <li key={index} className="py-4">
                  <Link to={item.href}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
