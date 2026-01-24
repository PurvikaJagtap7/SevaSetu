"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import CitizenNavbar from "../components/CitizenNavbar";
import Footer from "../components/Footer";

export default function GrievancePage() {
  const router = useRouter();

  const [form, setForm] = useState({
    category: "",
    city: "",
    state: "",
    place: "",
    area: "",
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
  if (!form.grievance || !form.city || !form.state) {
    alert("Please fill required fields (City, State, and Grievance)");
    return;
  }

  const formWithAddress = {
    ...form,
    address: `${form.area ? form.area + ", " : ""}${form.place ? form.place + ", " : ""}${form.city}, ${form.state}`,
    imageName: form.image ? form.image.name : null   // 👈 only store name
  };

  sessionStorage.setItem("grievanceData", JSON.stringify(formWithAddress));
  router.push("/review");
};

  
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <CitizenNavbar />

      <div className="flex justify-center px-4 mt-8 mb-10 flex-1">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8">

          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-2">
            Grievance Details
          </h2>

          {/* Location */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold mb-3 text-gray-700">
              Location of Issue *
            </h3>

            <div className="grid grid-cols-2 gap-4 mb-3">
              <div>
                <label className="block text-sm font-medium mb-1">City *</label>
                <input
                  name="city"
                  onChange={handleChange}
                  placeholder="e.g., Mumbai"
                  className="w-full border p-3 text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">State *</label>
                <input
                  name="state"
                  onChange={handleChange}
                  placeholder="e.g., Maharashtra"
                  className="w-full border p-3 text-sm"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Place / Locality</label>
                <input
                  name="place"
                  onChange={handleChange}
                  placeholder="e.g., Andheri West"
                  className="w-full border p-3 text-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Area / Street</label>
                <input
                  name="area"
                  onChange={handleChange}
                  placeholder="e.g., SV Road, near Metro"
                  className="w-full border p-3 text-sm"
                />
              </div>
            </div>

            <p className="text-xs text-gray-500 mt-2">
              Helps authorities locate the issue quickly.
            </p>
          </div>

          {/* Image Upload */}
          <label className="block text-sm font-semibold mb-2">
            Upload Photo
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

          {form.image && (
            <p className="text-sm text-green-600 mb-4">
              ✓ {form.image.name} selected
            </p>
          )}

          {/* Grievance */}
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
            className="w-full bg-blue-900 text-white py-3 text-sm font-semibold hover:bg-blue-800 transition-colors"
          >
            Process Grievance
          </button>

        </div>
      </div>

      <Footer />
    </div>
  );
}
