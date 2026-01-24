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
    phone: "",
    urgency: "",
    grievance: "",
    image: null,
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === "image") {
      setForm({ ...form, image: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = async () => {
    // Validation
    if (!form.grievance || !form.city || !form.state) {
      alert("Please fill required fields (City, State, and Grievance)");
      return;
    }

    if (!form.phone) {
      alert("Please provide your WhatsApp number to receive updates");
      return;
    }

    setLoading(true);

    try {
      // Create FormData for Flask backend
      const formData = new FormData();
      formData.append("grievance_text", form.grievance);
      formData.append("city", form.city);
      formData.append("state", form.state);
      formData.append("place", form.place || "");
      formData.append("area", form.area || "");
      formData.append("phone", form.phone);
      formData.append("specificLocation", `${form.area || ""} ${form.place || ""}`.trim());

      if (form.image) {
        formData.append("image", form.image);
      }

      console.log("📤 Sending to Flask backend...");

      // Call Flask backend
      const response = await fetch("http://localhost:5000/process_grievance", {
        method: "POST",
        body: formData,
      });

      console.log("📥 Response status:", response.status);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      console.log("✅ Result:", result);

      if (result.status === "success") {
        // Prepare data for review page
        const formWithAddress = {
          ...form,
          address: `${form.area ? form.area + ", " : ""}${form.place ? form.place + ", " : ""}${form.city}, ${form.state}`,
          imageName: form.image ? form.image.name : null,
          grievance_id: result.grievance_id,
          structured: result.structured,
          department: result.department,
          priority: result.priority,
          image_analysis: result.image_analysis,
          whatsapp_sent: result.whatsapp_sent,
        };

        sessionStorage.setItem("grievanceData", JSON.stringify(formWithAddress));

        // Show success alert
        if (result.whatsapp_sent) {
          alert(
            `✅ Grievance Submitted Successfully!\n\n` +
            `🆔 Grievance ID: ${result.grievance_id}\n` +
            `🏢 Department: ${result.department}\n` +
            `⚠️ Priority: ${result.priority}\n\n` +
            `📱 WhatsApp confirmation sent to ${result.phone_number}`
          );
        } else {
          alert(
            `✅ Grievance Submitted Successfully!\n\n` +
            `🆔 Grievance ID: ${result.grievance_id}\n` +
            `🏢 Department: ${result.department}\n` +
            `⚠️ Priority: ${result.priority}\n\n` +
            `⚠️ WhatsApp notification failed: ${result.whatsapp_error || "Unknown error"}`
          );
        }

        router.push("/review");
      } else {
        throw new Error(result.message || "Unknown error");
      }
    } catch (error) {
      console.error("❌ Submission error:", error);
      alert(
        `❌ Failed to submit grievance\n\n` +
        `Error: ${error.message}\n\n` +
        `Please ensure:\n` +
        `1. Flask server is running on port 5000\n` +
        `2. CORS is enabled in Flask\n` +
        `3. All required fields are filled`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <CitizenNavbar />

      <div className="flex justify-center px-4 mt-8 mb-10 flex-1">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8">
          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-2">
            Grievance Details
          </h2>

          {/* WhatsApp Number */}
          <div className="mb-6">
            <label className="block text-sm font-semibold mb-1">
              WhatsApp Number * 📱
            </label>
            <input
              name="phone"
              type="tel"
              value={form.phone}
              onChange={handleChange}
              placeholder="+91 9876543210"
              className="w-full border p-3 text-sm"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">
              We'll send confirmation and updates on WhatsApp
            </p>
          </div>

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
                  value={form.city}
                  onChange={handleChange}
                  placeholder="e.g., Mumbai"
                  className="w-full border p-3 text-sm"
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">State *</label>
                <input
                  name="state"
                  value={form.state}
                  onChange={handleChange}
                  placeholder="e.g., Maharashtra"
                  className="w-full border p-3 text-sm"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Place / Locality
                </label>
                <input
                  name="place"
                  value={form.place}
                  onChange={handleChange}
                  placeholder="e.g., Andheri West"
                  className="w-full border p-3 text-sm"
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">
                  Area / Street
                </label>
                <input
                  name="area"
                  value={form.area}
                  onChange={handleChange}
                  placeholder="e.g., SV Road, near Metro"
                  className="w-full border p-3 text-sm"
                  disabled={loading}
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
              disabled={loading}
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
            value={form.grievance}
            onChange={handleChange}
            placeholder="Explain your issue in simple language..."
            className="w-full border p-4 text-sm resize-none mb-6 text-black placeholder-gray-400"
            disabled={loading}
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-blue-900 text-white py-3 text-sm font-semibold hover:bg-blue-800 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Process Grievance"}
          </button>
        </div>
      </div>

      <Footer />
    </div>
  );
}