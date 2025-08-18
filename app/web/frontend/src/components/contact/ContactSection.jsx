import React from "react";
import { Contacts } from "../../constants";

const ContactSection = () => {
  return (
    <>
      <section class="">
        <div class="container px-6 py-3 mx-auto">
          <div class="text-center">
            <p class="font-medium text-xl text-v-secondary">Contáctanos</p>

            <h1 class="mt-2 text-4xl font-semibold md:text-4xl">
              Habla con nosotros
            </h1>

            <p class="mt-3 text-v-text">
            Estamos aquí para apoyarte. Nuestro equipo de expertos en inteligencia artificial está listo para ayudarte a transformar tus ideas en soluciones innovadoras. No dudes en ponerte en contacto con nosotros a través de los siguientes medios:
            </p>
          </div>

          <div class="grid grid-cols-1 gap-12 mt-10 md:grid-cols-2 lg:grid-cols-2">
            {Contacts.map((contact, index) => (
              <a
                href={contact.link}
                class="flex flex-col items-center justify-center text-center"
              >
                <span class="p-3 text-v-primary rounded-full bg-blue-100/80 dark:bg-gray-800">
                  {contact.icon}
                </span>

                <h2 class="mt-4 text-2xl font-medium text-v-text dark:text-white">
                  {contact.name}
                </h2>
                <p class="mt-2 text-v-spanish-gray dark:text-gray-400">
                  {contact.description}
                </p>
              </a>
            ))}
          </div>
        </div>
      </section>
    </>
  );
};

export default ContactSection;
