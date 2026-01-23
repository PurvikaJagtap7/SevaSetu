"use client";

import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">

      {/* Header */}
      <div className="bg-white shadow py-4 text-center">
        <h1 className="text-xl font-bold text-blue-900">Nyaya-Grievance</h1>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-12 flex-1">

        <h2 className="text-3xl font-bold text-blue-900 mb-6">
          About This Portal
        </h2>

        <p className="text-gray-700 mb-6 leading-relaxed">
          Nyaya-Grievance is an AI-powered public grievance redressal platform
          inspired by CPGRAMS. This system allows citizens to submit complaints
          in simple language while intelligent AI processing structures the
          complaint, identifies the relevant department and prioritizes it for
          faster resolution.
        </p>

        <p className="text-gray-700 mb-10 leading-relaxed">
          The goal of this platform is to improve transparency, reduce manual
          effort in complaint handling, and ensure that public grievances are
          resolved efficiently with full accountability.
        </p>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 text-center">

          <Feature
            icon="📝"
            title="Easy Submission"
            desc="Citizens can describe issues naturally without worrying about format."
          />

          <Feature
            icon="🤖"
            title="AI Smart Routing"
            desc="AI analyzes and routes complaints to the correct department."
          />

          <Feature
            icon="📊"
            title="Transparent Tracking"
            desc="Users can track grievance progress with clarity and visibility."
          />
        </div>

      </div>

      {/* Footer */}
      <div className="bg-blue-900 text-white text-center py-3 text-xs">
        © 2026 Nyaya-Grievance Portal
      </div>
    </div>
  );
}

function Feature({ icon, title, desc }) {
  return (
    <div className="bg-white p-6 border shadow-sm rounded">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="font-bold text-blue-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  );
}
