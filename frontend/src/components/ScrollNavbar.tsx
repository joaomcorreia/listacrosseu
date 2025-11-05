"use client";

import Link from "next/link";
import { useEffect, useState, useRef } from "react";
import { HOW_SLUGS } from "@/i18n/howitworks";
import { UI as FORMS_UI, FORMS_SLUG } from "@/i18n/forms";
import { useSiteSettings } from "@/hooks/useSiteSettings";

interface ScrollNavbarProps {
  lang: string;
  t: {
    search: string;
    countries: string;
    pricing: string;
    aiDesign: string;
    categories?: string;
  };
}

export default function ScrollNavbar({ lang, t }: ScrollNavbarProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isLanguageDropdownOpen, setIsLanguageDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { settings } = useSiteSettings();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsLanguageDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const UI = {
    en: { search: "Search", countries: "Countries", categories: "Categories", pricing: "Pricing", aiDesign: "AI Design", howItWorks: "How it works", admin: "Admin" },
    fr: { search: "Recherche", countries: "Pays", categories: "Catégories", pricing: "Tarifs", aiDesign: "IA Design", howItWorks: "Comment ça marche", admin: "Admin" },
    nl: { search: "Zoeken", countries: "Landen", categories: "Categorieën", pricing: "Prijzen", aiDesign: "AI Design", howItWorks: "Hoe het werkt", admin: "Admin" },
    pt: { search: "Pesquisa", countries: "Países", categories: "Categorias", pricing: "Preços", aiDesign: "Design IA", howItWorks: "Como funciona", admin: "Admin" },
    de: { search: "Suche", countries: "Länder", categories: "Kategorien", pricing: "Preise", aiDesign: "KI Design", howItWorks: "So funktioniert es", admin: "Admin" },
    es: { search: "Buscar", countries: "Países", categories: "Categorías", pricing: "Precios", aiDesign: "Diseño IA", howItWorks: "Cómo funciona", admin: "Admin" },
  } as const;

  // Get forms label for current language
  const langUppercase = lang.toUpperCase() as keyof typeof FORMS_UI;
  const formsLabel = FORMS_UI[langUppercase]?.navLabel || FORMS_UI.EN.navLabel;

  const languages = {
    eu: { flag: "🇪🇺", name: "European Union", code: "EU" },
    en: { flag: "🇬🇧", name: "English", code: "EN" },
    fr: { flag: "🇫🇷", name: "Français", code: "FR" },
    nl: { flag: "🇳🇱", name: "Nederlands", code: "NL" },
    pt: { flag: "🇵🇹", name: "Português", code: "PT" },
    de: { flag: "🇩🇪", name: "Deutsch", code: "DE" },
    es: { flag: "🇪🇸", name: "Español", code: "ES" },
  } as const;

  const langKey = lang as keyof typeof UI;
  const text = UI[langKey] || UI.en;

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? "bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm" 
          : "bg-transparent"
      }`}
    >
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link 
          href={`/${lang}`} 
          className={`flex items-center gap-3 font-bold text-xl transition-colors duration-300 ${
            isScrolled ? "text-gray-900" : "text-white"
          }`}
        >
          {settings.logo && (
            <img 
              src={settings.logo} 
              alt="ListAcross EU Logo" 
              className="h-8 w-auto"
            />
          )}
          ListAcross EU
        </Link>

        <nav className="flex items-center gap-6 text-sm">
          <Link 
            href={`/${lang}/search`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.search}
          </Link>
          <Link 
            href={`/${lang}/countries`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.countries}
          </Link>
          <Link 
            href={`/${lang}/categories`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.categories}
          </Link>
          <Link 
            href={`/${lang}/pricing`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.pricing}
          </Link>
          <Link 
            href={`/${lang}/ai-design`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.aiDesign}
          </Link>
          <Link 
            href={`/${lang}/${HOW_SLUGS[lang.toUpperCase() as keyof typeof HOW_SLUGS] || 'how-it-works'}`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.howItWorks}
          </Link>
          <Link 
            href={`/${lang}/${FORMS_SLUG[langUppercase] || FORMS_SLUG.EN}`} 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {formsLabel}
          </Link>
          <Link 
            href="/admin" 
            className={`hover:underline transition-colors duration-300 ${
              isScrolled ? "text-gray-700 hover:text-gray-900" : "text-white/90 hover:text-white"
            }`}
          >
            {text.admin}
          </Link>
        </nav>

        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsLanguageDropdownOpen(!isLanguageDropdownOpen)}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
              isScrolled
                ? "hover:bg-gray-100 text-gray-700 border border-gray-200"
                : "hover:bg-white/10 text-white border border-white/30"
            }`}
          >
            <span className="text-lg">{languages[lang as keyof typeof languages]?.flag || "🌐"}</span>
            <svg
              className={`w-4 h-4 transition-transform duration-200 ${
                isLanguageDropdownOpen ? "rotate-180" : ""
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {isLanguageDropdownOpen && (
            <div className={`absolute right-0 mt-2 py-2 w-48 rounded-lg shadow-lg border z-50 ${
              isScrolled
                ? "bg-white border-gray-200"
                : "bg-white/95 backdrop-blur-md border-white/20"
            }`}>
              {Object.entries(languages).map(([code, lang_data]) => (
                <Link
                  key={code}
                  href={`/${code}`}
                  onClick={() => setIsLanguageDropdownOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2 text-sm transition-colors duration-200 ${
                    code === lang
                      ? "bg-blue-50 text-blue-700"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <span className="text-lg">{lang_data.flag}</span>
                  <span className="font-medium">{lang_data.name}</span>
                  {code === lang && (
                    <svg className="w-4 h-4 ml-auto text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}