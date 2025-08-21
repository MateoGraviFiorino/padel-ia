import React from "react";
import NavBar from "../components/NavBar";
import Headline from "../components/about/Headline";
import Mission from "../components/about/Mission";
import Background from "../components/about/Background";
import Leaders from "../components/about/Leaders";
import Team from "../components/about/Team";
import Motto from "../components/about/Motto";
import Footer from "../components/Footer";
import { BaggageClaim } from "lucide-react";

export default function AboutPage() {
  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <Headline />
        <Mission />
        <Background />
        <Leaders />
        <Team />
        <Motto />
        <Footer />
      </div>
    </>
  );
}
