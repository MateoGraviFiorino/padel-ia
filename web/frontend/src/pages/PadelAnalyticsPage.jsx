import React, { useState } from "react";
import NavBar from "../components/NadelNavBar";
import HeroSection from "../components/PadelHeroSection";
import VideoUploadSection from "../components/VideoUploadSection";
import AnalyticsDashboard from "../components/AnalyticsDashboard";
import Footer from "../components/Footer";

export default function PadelAnalyticsPage() {
  const [matchData, setMatchData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleVideoProcessed = (data) => {
    setMatchData(data);
    setIsProcessing(false);
  };

  const handleVideoUpload = () => {
    setIsProcessing(true);
  };

  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        <HeroSection />
        <VideoUploadSection 
          onVideoUpload={handleVideoUpload}
          onVideoProcessed={handleVideoProcessed}
          isProcessing={isProcessing}
        />
        {matchData && <AnalyticsDashboard matchData={matchData} />}
        <Footer />
      </div>
    </>
  );
}
