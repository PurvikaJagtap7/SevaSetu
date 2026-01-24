"use client";

import Link from "next/link";
import CitizenNavbar from "../components/CitizenNavbar";  
import Footer from "../components/Footer";

export default function CitizenHome() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <CitizenNavbar />

      <div className="flex flex-col items-center justify-center flex-1 px-6">

        <h2 className="text-2xl font-bold text-blue-900 mb-2 text-center">
          What would you like to do?
        </h2>

        <p className="text-sm text-gray-600 mb-12 text-center max-w-md">
          Submit a new complaint or track the status of an existing grievance easily.
        </p>

        <div className="flex flex-col md:flex-row gap-10">

          <Link href="/grievance">
            <div className="w-full md:w-72 h-40 bg-white border shadow-md flex flex-col items-center justify-center cursor-pointer hover:shadow-xl hover:-translate-y-1 transition">
              <div className="text-4xl mb-3">📝</div>
              <p className="text-lg font-semibold text-blue-900">
                Submit New Grievance
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Describe your issue in simple language
              </p>
            </div>
          </Link>

          <Link href="/track">
            <div className="w-full md:w-72 h-40 bg-white border shadow-md flex flex-col items-center justify-center cursor-pointer hover:shadow-xl hover:-translate-y-1 transition">
              <div className="text-4xl mb-3">📍</div>
              <p className="text-lg font-semibold text-blue-900">
                Track Grievance
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Check status using your grievance ID
              </p>
            </div>
          </Link>

        </div>
      </div>

      <Footer />
    </div>
  );
}

