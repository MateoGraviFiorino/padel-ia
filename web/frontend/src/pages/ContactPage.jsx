import React from "react";
import NavBar from "../components/NavBar";
import Footer from "../components/Footer";
import ContactSection from "../components/contact/ContactSection";

const ContactPage = () => {
  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <ContactSection />
        {/* <Footer /> */}
      </div>
    </>
  );
};

export default ContactPage;
