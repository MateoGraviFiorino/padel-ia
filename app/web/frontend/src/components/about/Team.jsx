import React from "react";
import { LeaderCards } from "../../constants";

const Team = () => {
  return (
    <>
      {/* Sección del equipo con un toque más visual */}
      <section class="">
        <div class="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-6">
          <div class="mx-auto mb-8 max-w-screen-sm lg:mb-16">
            <h2 class="mb-4 text-4xl tracking-tight bg-gradient-to-r from-v-secondary to-v-primary text-transparent bg-clip-text">
              Nuestro equipo
            </h2>
            <p class="font-light text-gray-500 sm:text-xl dark:text-gray-400">
              Explore the whole collection of open-source web components and
              elements built with the utility classes from Tailwind
            </p>
          </div>
          <div class="grid gap-8 lg:gap-16 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            {LeaderCards.map((member, index) => (
              <div class="text-center text-gray-500 dark:text-gray-400">
                <img
                  class="mx-auto mb-4 w-36 h-36 rounded-full"
                  src={member.image}
                  alt={index}
                />
                <h3 class="mb-1 text-2xl tracking-tight text-v-soap dark:text-white">
                  <a href="#">{member.name}</a>
                </h3>
                <p>{member.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
};

export default Team;
