import React from "react";
import NavBar from "../components/NavBar";
import HeroSection from "../components/HeroSection";
import FeatureSection from "../components/FeatureSection";
import Workflow from "../components/Workflow";
import Pricing from "../components/Pricing";
import Footer from "../components/Footer";

export default function MainPage() {
  return (
    <>
      <NavBar></NavBar>
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <HeroSection />
        <FeatureSection />
        <Workflow />
        {/* <Pricing /> */}
        {/* <Footer /> */}
      </div>
    </>
  );
}
