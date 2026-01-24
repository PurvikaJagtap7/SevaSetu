"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function GrievancePage() {
  const router = useRouter();

  const [form, setForm] = useState({
    category: "",
    address: "",
    urgency: "",
    grievance: "",
    image: null,
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === "image") {
      setForm({ ...form, image: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };


  const handleSubmit = () => {
  if (!form.grievance || !form.address) {
    alert("Please fill required fields");
    return;
  }

  // Store form data for review page
  localStorage.setItem("grievanceData", JSON.stringify(form));

  router.push("/review");
};


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* Header */}
      <div className="bg-blue-900 text-white py-4 text-center text-lg font-semibold">
        Submit New Grievance
      </div>

      <div className="flex justify-center px-4 mt-8 mb-10">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8">

          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-2">
            Grievance Details
          </h2>

          {/* Category */}
          <label className="block text-sm font-semibold mb-1">
            Category <span className="text-gray-500">(optional hint)</span>
          </label>
          <select
            name="category"
            onChange={handleChange}
            className="w-full border p-3 text-sm mb-5"
          >
            <option value="">Select Category</option>
            <option>Infrastructure</option>
            <option>Water & Sanitation</option>
            <option>Electricity</option>
            <option>Health</option>
            <option>Public Safety</option>
            <option>Other</option>
          </select>

          {/* Address */}
          <label className="block text-sm font-semibold mb-1">
            Location / Address of Issue *
          </label>
          <input
            name="address"
            onChange={handleChange}
            placeholder="Area, street, landmark, city..."
            className="w-full border p-3 text-sm mb-2"
          />
          <p className="text-xs text-gray-500 mb-4">
            Helps authorities locate the issue quickly.
          </p>

          {/* Urgency */}
          <label className="block text-sm font-semibold mb-2">
            How urgent does this feel?
          </label>
          <div className="flex flex-col md:flex-row gap-4 mb-6 text-sm">
            <label className="flex items-center gap-2">
              <input type="radio" name="urgency" value="low" onChange={handleChange} />
              Not Urgent
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" name="urgency" value="medium" onChange={handleChange} />
              Needs Attention
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" name="urgency" value="high" onChange={handleChange} />
              Urgent Public Safety Issue
            </label>
          </div>

          {/* Image Upload */}
          <label className="block text-sm font-semibold mb-2">
            Upload Photo (optional)
          </label>

          <label className="flex flex-col items-center justify-center w-full h-36 border-2 border-dashed border-blue-300 cursor-pointer bg-blue-50 hover:bg-blue-100 mb-6">
            <div className="text-center">
              <p className="text-3xl mb-2">📷</p>
              <p className="text-sm text-gray-700 font-medium">
                Click to upload or drag and drop image
              </p>
              <p className="text-xs text-gray-500">PNG, JPG up to 5MB</p>
            </div>
            <input
              type="file"
              name="image"
              accept="image/*"
              onChange={handleChange}
              className="hidden"
            />
          </label>

          {/* Grievance Text */}
          <label className="block text-sm font-semibold mb-1">
            Describe Your Grievance *
          </label>

          <textarea
            rows="7"
            name="grievance"
            onChange={handleChange}
            placeholder="Explain your issue in simple language..."
            className="w-full border p-4 text-sm resize-none mb-6 text-black placeholder-gray-400"
          />

          <button
            onClick={handleSubmit}
            className="w-full bg-blue-900 text-white py-3 text-sm font-semibold"
          >
            Process Grievance
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-900 text-white text-center py-3 text-xs">
        © 2026 Nyaya-Grievance Portal
      </div>
    </div>
  );
}
