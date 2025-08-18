import React from "react";
import NavBar from "../components/NavBar";
import Footer from "../components/Footer";
import StoriesSection from "../components/stories/StoriesSection";

export default function SuccessPage() {
  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <StoriesSection></StoriesSection>
        {/* <Footer /> */}
      </div>
    </>
  );
}
