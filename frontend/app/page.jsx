"use client";

import Link from "next/link";
import Navbar from "./components/Navbar";

export default function Home() {
  return (
    <div className="bg-white text-gray-800 min-h-screen flex flex-col">

      <Navbar />
      <Hero />
      <Features />
      <Footer />

    </div>
  );
}

<Navbar />

/* ---------- HERO ---------- */

function Hero() {
  return (
    <div className="bg-gradient-to-b from-blue-50 to-white text-center py-16 px-6">

      <h2 className="text-4xl font-bold text-blue-900 mb-4">
        AI-Powered Grievance Reporting System
      </h2>

      <p className="text-gray-600 max-w-2xl mx-auto">
        Describe your issue in simple language. Our AI structures the complaint,
        assigns the correct department and ensures faster resolution with full transparency.
      </p>

    </div>
  );
}

/* ---------- FEATURES ---------- */

function Features() {
  return (
    <div className="grid md:grid-cols-3 gap-8 px-8 py-16 max-w-6xl mx-auto text-center">

      <Feature
        icon="📝"
        title="Simple Submission"
        desc="Write complaints naturally without worrying about format or department."
      />

      <Feature
        icon="🤖"
        title="AI Smart Routing"
        desc="AI analyzes grievance content and routes it to the correct authority."
      />

      <Feature
        icon="📊"
        title="Transparent Tracking"
        desc="Track grievance progress with complete visibility."
      />

    </div>
  );
}

function Feature({ icon, title, desc }) {
  return (
    <div className="p-6 border rounded shadow-sm hover:shadow-lg hover:-translate-y-1 transition">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="font-bold text-blue-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  );
}

/* ---------- FOOTER ---------- */

function Footer() {
  return (
    <div className="bg-blue-900 text-white text-center py-6 text-sm mt-auto">
      © 2026 Nyaya-Grievance Portal | AI Powered CPGRAMS 2.0
    </div>
  );
}
