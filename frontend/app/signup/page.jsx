"use client";

import Link from "next/link";
import { useState } from "react";
import Navbar from "../components/Navbar";

export default function SignupPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    mobile: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const validate = () => {
    let err = {};

    if (!form.name) err.name = "Name is required";

    if (!form.email) err.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email))
      err.email = "Invalid email format";

    if (!form.mobile) err.mobile = "Mobile number is required";

    if (!form.password) err.password = "Password is required";
    else if (form.password.length < 6)
      err.password = "Password must be at least 6 characters";

    setErrors(err);
    return Object.keys(err).length === 0;
  };

  const handleRegister = () => {
    if (validate()) {
      alert("Validated (later → API call)");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      
      {/* Navbar */}
      <Navbar/>

      <div className="flex items-center justify-center flex-1 px-4">
        <div className="bg-white w-full max-w-md border shadow-md p-6">

          <h2 className="text-xl font-bold text-blue-900 mb-6 border-b pb-2">
            USER REGISTRATION
          </h2>

          <label className="block text-sm font-semibold mb-1">Full Name</label>
          <input
            name="name"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.name && <p className="text-red-600 text-xs mb-2">{errors.name}</p>}

          <label className="block text-sm font-semibold mb-1">Email</label>
          <input
            name="email"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.email && <p className="text-red-600 text-xs mb-2">{errors.email}</p>}

          <label className="block text-sm font-semibold mb-1">Mobile Number</label>
          <input
            name="mobile"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.mobile && <p className="text-red-600 text-xs mb-2">{errors.mobile}</p>}

          <label className="block text-sm font-semibold mb-1">Password</label>
          <input
            name="password"
            type="password"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.password && <p className="text-red-600 text-xs mb-3">{errors.password}</p>}

          <button
            onClick={handleRegister}
            className="w-full bg-blue-900 text-white py-2 text-sm font-semibold"
          >
            REGISTER
          </button>

          <Link href="/login?role=citizen">
            <p className="text-center mt-4 text-blue-900 text-sm cursor-pointer underline">
              Already Registered? Login
            </p>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-900 text-white text-center py-3 text-xs">
        © 2026 Nyaya-Grievance Portal
      </div>
    </div>
  );
}
