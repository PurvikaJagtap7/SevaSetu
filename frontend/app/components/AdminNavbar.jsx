"use client";

import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";

export default function AdminNavbar() {
  const router = useRouter();
  const pathname = usePathname();

  const navItem = (href, label) => (
    <Link
      href={href}
      className={`px-3 py-1.5 rounded text-sm font-medium transition ${
        pathname === href
          ? "bg-blue-100 text-blue-900"
          : "text-blue-900 hover:bg-blue-50"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <div className="sticky top-0 bg-white shadow z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-3">

        {/* Logo */}
        <Link href="/dashboard" className="text-lg font-bold text-blue-900">
          Nyaya-Grievance (Admin)
        </Link>

        {/* Links */}
        <div className="flex gap-6 items-center">
          {navItem("/dashboard", "Home")}
          {navItem("/about", "About")}
          {navItem("/admin/profile", "Profile")}

          <button
            onClick={() => router.push("/")}
            className="text-sm font-semibold text-red-600 hover:underline"
          >
            Logout
          </button>
        </div>

      </div>
    </div>
  );
}
