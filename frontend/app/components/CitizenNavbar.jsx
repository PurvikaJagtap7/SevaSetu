"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";

export default function CitizenNavbar() {
  const pathname = usePathname();
  const router = useRouter();

  const navItem = (href, label) => (
    <Link
      href={href}
      className={`px-3 py-1.5 rounded text-sm font-medium transition
        ${
          pathname === href
            ? "bg-blue-100 text-blue-900"
            : "text-blue-900 hover:bg-blue-50"
        }`}
    >
      {label}
    </Link>
  );

  const handleLogout = () => {
    router.push("/");
  };

  return (
    <div className="sticky top-0 bg-white shadow z-50">
      <div className="flex justify-between items-center px-6 h-16 max-w-7xl mx-auto">

        {/* LOGO */}
        <Link href="/" className="flex items-center">
          <div className="relative h-12 w-44">
            <Image
              src="/logo.jpeg"
              alt="Nyaya Grievance Logo"
              fill
              className="object-contain"
              priority
            />
          </div>
        </Link>

        {/* NAV ITEMS */}
        <div className="flex gap-6 items-center">
          {navItem("/citizen", "Home")}
          {navItem("/about", "About")}
          {navItem("/profile", "Profile")}

          <button
            onClick={handleLogout}
            className="text-sm font-medium text-red-600 hover:underline"
          >
            Log Out
          </button>
        </div>

      </div>
    </div>
  );
}
