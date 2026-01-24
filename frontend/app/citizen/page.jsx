"use client";

import Link from "next/link";

export default function CitizenHome() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <Navbar />

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

/* ---------- NAVBAR ---------- */

function Navbar() {
  return (
    <div className="bg-white shadow py-4 px-6 flex justify-between items-center">
      <h1 className="text-xl font-bold text-blue-900">Nyaya-Grievance</h1>

      <div className="flex gap-8 text-sm font-medium items-center text-blue-900">
        <Link href="/" className="hover:underline">
          Home
        </Link>
        <Link href="/about" className="hover:underline">
          About
        </Link>
        <Link href="/profile" className="hover:underline">
          Profile
        </Link>
        <Link href="/" className="hover:underline">
          Logout
        </Link>
      </div>
    </div>
  );
}


/* ---------- FOOTER ---------- */

function Footer() {
  return (
    <div className="text-center py-4 text-xs text-gray-500">
      © 2026 Nyaya-Grievance Portal
    </div>
  );
}
