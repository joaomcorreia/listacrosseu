import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import "../styles/animations.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ListAcrossEU - Europe's Premier Business Directory | 6,331+ Verified Businesses",
  description: "Discover 6,331+ verified businesses across Spain, France, and Germany. Europe's leading multilingual business directory supporting all 27 EU languages with AI-powered search and Listy assistant.",
  keywords: "European businesses, EU directory, Spain France Germany businesses, multilingual directory, European companies, business search Europe",
  openGraph: {
    title: "ListAcrossEU - Europe's Business Directory",
    description: "Connect with 6,331+ verified European businesses across Spain, France, and Germany",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
