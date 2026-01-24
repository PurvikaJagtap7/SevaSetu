import "./globals.css";

export const metadata = {
  title: "Nyaya-Grievance",
  description: "AI Powered Public Grievance Redressal Portal inspired by CPGRAMS",
  icons:{
    icon:"/logo.jpeg",

  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
