import "../globals.css";
import Link from "next/link";
import ScrollNavbar from "@/components/ScrollNavbar";
import BlogPostsFooter from "@/components/BlogPostsFooter";
import Footer from "@/components/Footer";

const UI = {
  en: { search: "Search", countries: "Countries", categories: "Categories", pricing: "Pricing", aiDesign: "AI Design" },
  fr: { search: "Recherche", countries: "Pays", categories: "Catégories", pricing: "Tarifs", aiDesign: "IA Design" },
  nl: { search: "Zoeken", countries: "Landen", categories: "Categorieën", pricing: "Prijzen", aiDesign: "AI Design" },
  pt: { search: "Pesquisa", countries: "Países", categories: "Categorias", pricing: "Preços", aiDesign: "Design IA" },
  de: { search: "Suche", countries: "Länder", categories: "Kategorien", pricing: "Preise", aiDesign: "KI Design" },
  es: { search: "Buscar", countries: "Países", categories: "Categorías", pricing: "Precios", aiDesign: "Diseño IA" },
};

export default function LangLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { lang: keyof typeof UI };
}) {
  const lang = UI[params.lang] ? params.lang : "en";
  const t = UI[lang];

  return (
    <html lang={lang}>
      <body className="min-h-screen">
        <ScrollNavbar lang={lang} t={t} />
        
        {children}

        <BlogPostsFooter lang={lang} limit={3} />

        <Footer lang={lang} />
      </body>
    </html>
  );
}