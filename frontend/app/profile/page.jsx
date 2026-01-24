"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import axios from "axios";

export default function ProfilePage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Later this will be real API
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      // 🔁 Replace this URL later with your backend endpoint
      const res = await axios.get("/api/user/profile");

      setUser(res.data);
    } catch (err) {
      // Temporary mock data for now
      setUser({
        name: "Loading User...",
        email: "user@email.com",
        mobile: "+91 0000000000",
        totalGrievances: 0,
      });
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* Header */}
      <div className="bg-white shadow py-4 text-center">
        <h1 className="text-xl font-bold text-blue-900">Nyaya-Grievance</h1>
      </div>

      <div className="flex justify-center px-4 mt-10 mb-12 flex-1">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8">

          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-3">
            Your Profile
          </h2>

          {/* User Info */}
          <div className="grid md:grid-cols-2 gap-6 text-sm">

            <ProfileItem label="Full Name" value={user.name} />
            <ProfileItem label="Email" value={user.email} />
            <ProfileItem label="Mobile Number" value={user.mobile} />
            <ProfileItem
              label="Total Grievances Filed"
              value={user.totalGrievances}
            />

          </div>

          {/* Actions */}
          <div className="mt-10 flex gap-6">
            <Link href="/citizen">
              <button className="bg-blue-900 text-white px-6 py-2 text-sm font-semibold">
                Back to Dashboard
              </button>
            </Link>
          </div>

        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-900 text-white text-center py-3 text-xs">
        © 2026 Nyaya-Grievance Portal
      </div>
    </div>
  );
}

function ProfileItem({ label, value }) {
  return (
    <div>
      <p className="text-gray-500 mb-1">{label}</p>
      <p className="font-semibold text-gray-900">{value}</p>
    </div>
  );
}
