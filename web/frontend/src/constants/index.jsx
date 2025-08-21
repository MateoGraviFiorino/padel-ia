import { BotMessageSquare } from "lucide-react";
import { Workflow } from "lucide-react";
import { BrainCircuit } from "lucide-react";
import { Lightbulb } from "lucide-react";
import { Star } from "lucide-react";
import { HeartHandshake } from "lucide-react";
import { MessageCircle } from "lucide-react";
import { Mail } from "lucide-react";

import leader1 from "../assets/profile-pictures/tomas_navarro.png";
import leader2 from "../assets/profile-pictures/guido_lorenzetti.jpeg";
import leader3 from "../assets/profile-pictures/augusto_farias.jpeg";
import leader4 from "../assets/profile-pictures/user3.jpg";
import leader5 from "../assets/profile-pictures/mateo_gravi_fiorino.jpg";
import leader6 from "../assets/profile-pictures/user3.jpg";
import leader7 from "../assets/profile-pictures/user3.jpg";


// Cambiar las imagenes por assets
export const caseStudies = [
  {
    id: 1,
    company: "One Million Capital",
    image: "",//"/api/placeholder/800/400?text=Financial+AI+Analytics",
    description:
      "One Million Capital optimizó su análisis de riesgo y aumentó sus retornos de inversión en un 15% mediante la implementación de nuestros modelos de IA predictiva.",
    link: "#",
  },
  {
    id: 2,
    company: "EcoSmart Solutions",
    image: "/api/placeholder/800/400?text=Smart+Energy+Management",
    description:
      "EcoSmart Solutions redujo el consumo energético de sus clientes en un 30% utilizando nuestros algoritmos de IA para optimizar sistemas de gestión energética en edificios inteligentes.",
    link: "#",
  },
  {
    id: 3,
    company: "MediCore Innovations",
    image: "/api/placeholder/800/400?text=AI+in+Healthcare",
    description:
      "MediCore Innovations mejoró la precisión de diagnóstico en un 25% y redujo los tiempos de espera en un 40% mediante la implementación de nuestro sistema de IA para análisis de imágenes médicas.",
    link: "#",
  },
];

export const navItems = [
  { label: "Inicio", href: "/home" },
  { label: "Servicios", href: "/services" },
  { label: "Contáctanos", href: "/contact" },
  { label: "Sobre nosotros", href: "/about" },
  { label: "Trabaja con Nosotros", href:  "mailto:software.vanguard@gmail.com" },
];

export const features = [
  {
    icon: <BotMessageSquare />,
    text: "Agentes",
    description:
      "Mejorá la atención al cliente, ahorre tiempo y dinero mediante asistentes que resuelvan problemas por usted.",
  },
  {
    icon: <Workflow />,
    text: "Automatizaciones",
    description:
      "No pierda tiempo realizando tareas repetitivas, la automatizacion es el futuro.",
  },
  {
    icon: <BrainCircuit />,
    text: "Inteligencia Artificial",
    description:
      "Utilizamos soluciones de inteligencia artificial para poder ofrecer el mejor servicio al menor costo.",
  },
];

export const checklistItems = [
  {
    title: "Disponibilidad 24/7",
    description:
      "Permite escalabilidad mundial, atienda clientes de todo el mundo a toda hora.",
  },
  {
    title: "Respuesta inmediata",
    description: "Soluciones en tiempo real y sin tiempos de espera.",
  },
  {
    title: "Interacciones personalizadas",
    description: "Puede adoptar distintos roles profesionales.",
  },
  {
    title: "Automatización de tareas",
    description: "Permite al usuario realizar acciones sin supervisión humana.",
  },
];

export const pricingOptions = [
  {
    title: "Free",
    price: "$0",
    features: [
      "Private board sharing",
      "5 Gb Storage",
      "Web Analytics",
      "Private Mode",
    ],
  },
  {
    title: "Pro",
    price: "$10",
    features: [
      "Private board sharing",
      "10 Gb Storage",
      "Web Analytics (Advance)",
      "Private Mode",
    ],
  },
  {
    title: "Enterprise",
    price: "$200",
    features: [
      "Private board sharing",
      "Unlimited Storage",
      "High Performance Network",
      "Private Mode",
    ],
  },
];

export const resourcesLinks = [
  { href: "#", text: "Getting Started" },
  { href: "#", text: "Documentation" },
  { href: "#", text: "Tutorials" },
  { href: "#", text: "API Reference" },
  { href: "#", text: "Community Forums" },
];

export const platformLinks = [
  { href: "#", text: "Features" },
  { href: "#", text: "Supported Devices" },
  { href: "#", text: "System Requirements" },
  { href: "#", text: "Downloads" },
  { href: "#", text: "Release Notes" },
];

export const communityLinks = [
  { href: "#", text: "Events" },
  { href: "#", text: "Meetups" },
  { href: "#", text: "Conferences" },
  { href: "#", text: "Hackathons" },
  { href: "#", text: "Jobs" },
];

export const valuesBackground = [
  {
    title: "Innovación",
    icon: <Lightbulb />,
    description:
      "Breve descripción de cómo aplicamos este valor en nuestro trabajo diario.",
    backgroundStyle:
      "p-8 bg-radial-gradient-0 from-neutral-800 to-neutral-900 rounded-lg shadow-lg transform transition duration-300 hover:scale-105",
  },
  {
    title: "Excelencia",
    icon: <Star />,
    description:
      "Breve descripción de cómo aplicamos este valor en nuestro trabajo diario.",
    backgroundStyle:
      "p-8 bg-radial-gradient-1 from-neutral-800 to-neutral-900 rounded-lg shadow-lg transform transition duration-300 hover:scale-105",
  },
  {
    title: "Colaboración",
    icon: <HeartHandshake />,
    description:
      "Breve descripción de cómo aplicamos este valor en nuestro trabajo diario.",
    backgroundStyle:
      "p-8 bg-radial-gradient-2 from-neutral-800 to-neutral-900 rounded-lg shadow-lg transform transition duration-300 hover:scale-105",
  },
];

export const LeaderCards = [
  {
    name: "Tomás Navarro",
    role: "CEO",
    image: leader1,
    description:
      "Toma las decisiones estratégicas de nuestra empresa.",
  },
  {
    name: "Guido Lorenzetti",
    role: "CTO",
    image: leader2,
    description:
      "Lidera al equipo constantemente con sus mejoras en tecnología.",
  },
  
  {
    name: "Augusto Farias",
    role: "CFO",
    image: leader3,
    description:
      "Maneja las finanzas y lidera con exactitud nuestros próximos pasos.",
  },
  {
    name: "Alejo Lo Menzo",
    role: "COO",
    image: "",
    description:
      "Toma las decisiones estratégicas para nuestro día a día",
  },
  {
    name: "Mateo Gravi Fiorino",
    role: "DevOps",
    image: leader5,
    description:
      "Infraestructura y automatizaciones.",
  },
  {
    name: "Mateo Rovere",
    role: "Backend",
    image: "",
    description:
      "Desarrollo, investigación e implementación de soluciones.",
  },
  {
    name: "Enzo Ferrari",
    role: "Developer",
    image: "",
    description:
      "Desarrollo, investigación e implementación de soluciones.",
  },
];



export const Contacts = [
  {
    name: "Whatsapp",
    description:
      "Comunícate de manera rápida y directa. Envíanos un mensaje y recibe asistencia inmediata de nuestro asistente virtual.",
    icon: <MessageCircle />,
    link: "https://wa.me/5493412278726",
  },
  {
    name: "Email",
    description:
      "Si prefieres un contacto más formal, envíanos un correo electrónico. Nuestro equipo responderá lo antes posible para resolver tus dudas o inquietudes.",
    icon: <Mail />,
    link: "mailto:software.vanguard@gmail.com",
  },
];

export const services = [
  {
    title: "Consultoría en Inteligencia Artifical",
    description:
      "Te ayudamos a aprovechar el poder de la inteligencia artificial para optimizar tu negocio. Nuestro equipo de expertos identifica la solución perfecta para tus necesidades y te acompaña en cada paso del proceso... Tus competidores ya lo estan usando. Cuando lo vas a implementar?",
  },

];

export const projects = [
  {
    title: "Asistente de IA para WhatsApp",
    description: "Este proyecto representa una solución innovadora para un destacado broker en Rosario, proporcionando un asistente inteligente que ha transformado la gestión de usuarios con tiempos de respuesta casi instantáneos, optimizando así la carga de trabajo del personal. Además, permite el envío de campañas de marketing directamente desde la plataforma y facilita la compra de dólares de manera ágil y segura, convirtiéndose en un recurso invaluable para mejorar la eficiencia y el crecimiento del broker.",
  },
  {
    title: "English Academy con AI",
    description: "English Academy con AI es una innovadora plataforma de aprendizaje desarrollada para un importante instituto de inglés. Utilizando inteligencia artificial, adapta los contenidos a las necesidades de cada estudiante y ofrece análisis de desempeño para identificar áreas de mejora. Con herramientas interactivas como chatbots para practicar conversación y recursos multimedia, los estudiantes aprenden de manera eficiente y divertida, preparándose así para ser hablantes competentes del idioma."
  },
  {
    title: "Human Resources Copilot",
    description: "Human Resources Copilot es una solución de inteligencia artificial diseñada para optimizar el reclutamiento en una importante multinacional del sector. Mediante el uso de algoritmos avanzados, el sistema clasifica automáticamente los perfiles, identificando a los candidatos más adecuados para cada puesto y ahorrando un tiempo valioso en la selección. Además, proporciona informes detallados sobre tendencias en el mercado laboral y la efectividad de las campañas de reclutamiento, lo que permite a la empresa tomar decisiones más informadas y estratégicas.",
  },
  {
    title: "Base de Datos estilo Data Lake",
    description: "La Base de Datos estilo Data Lake es una solución diseñada para un importante supermercado, que centraliza y gestiona grandes volúmenes de datos de ventas, inventarios y comportamiento del cliente en un único repositorio. Este enfoque permite análisis en tiempo real para identificar tendencias, optimizar el inventario y personalizar la experiencia de compra. Además, su arquitectura flexible facilita la integración de nuevas fuentes de datos, mejorando así la toma de decisiones estratégicas basadas en información precisa y actualizada.",
  },
];
