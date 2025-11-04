"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const EU_COUNTRIES = [
    { code: "de", name: "Germany" },
    { code: "gr", name: "Greece" },
    { code: "hu", name: "Hungary" },
    { code: "ie", name: "Ireland" },
    { code: "it", name: "Italy" },
    { code: "lv", name: "Latvia" },
    { code: "lt", name: "Lithuania" },
    { code: "lu", name: "Luxembourg" },
    { code: "mt", name: "Malta" },
    { code: "nl", name: "Netherlands" },
    { code: "pl", name: "Poland" },
    { code: "pt", name: "Portugal" },
    { code: "ro", name: "Romania" },
    { code: "sk", name: "Slovakia" },
    { code: "si", name: "Slovenia" },
    { code: "es", name: "Spain" },
    { code: "se", name: "Sweden" },
    { code: "fi", name: "Finland" },
    { code: "fr", name: "France" },
    { code: "be", name: "Belgium" },
    { code: "bg", name: "Bulgaria" },
    { code: "hr", name: "Croatia" },
    { code: "cy", name: "Cyprus" },
    { code: "cz", name: "Czech Republic" },
    { code: "dk", name: "Denmark" },
    { code: "ee", name: "Estonia" },
    { code: "at", name: "Austria" }
];

export default function FlagCarousel() {
    const [isPaused, setIsPaused] = useState(false);
    const router = useRouter();

    const handleFlagClick = (countryCode: string) => {
        router.push(`/country/${countryCode.toLowerCase()}`);
    };

    return (
        <div className="w-full bg-gradient-to-r from-blue-50 to-blue-100 py-4 shadow-sm border-b border-blue-200">
            <div className="relative overflow-hidden">
                {/* Scrolling Container */}
                <div
                    className="flex items-center space-x-6 animate-scroll"
                    onMouseEnter={() => setIsPaused(true)}
                    onMouseLeave={() => setIsPaused(false)}
                    style={{
                        animationPlayState: isPaused ? 'paused' : 'running',
                    }}
                >
                    {/* Double the array for seamless infinite scroll */}
                    {[...EU_COUNTRIES, ...EU_COUNTRIES].map((country, index) => (
                        <div
                            key={`${country.code}-${index}`}
                            className="flex-shrink-0 group cursor-pointer"
                            onClick={() => handleFlagClick(country.code)}
                        >
                            <div className="flex flex-col items-center p-3 rounded-xl transition-all duration-300 hover:bg-white hover:shadow-lg hover:scale-110 group-hover:transform">
                                <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-blue-200 group-hover:border-blue-400 transition-colors shadow-sm">
                                    <img
                                        src={`/images/flags/${country.code}.svg`}
                                        alt={`${country.name} flag`}
                                        className="w-full h-full object-cover"
                                        onError={(e) => {
                                            // Fallback to a placeholder or EU flag
                                            const target = e.target as HTMLImageElement;
                                            target.src = '/images/flags/eu.svg';
                                        }}
                                    />
                                </div>
                                <span className="text-xs font-medium text-slate-600 mt-1 text-center leading-tight group-hover:text-blue-600 transition-colors">
                                    {country.name}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Gradient Overlays for smooth edge effect */}
                <div className="absolute left-0 top-0 w-16 h-full bg-gradient-to-r from-blue-50 to-transparent pointer-events-none"></div>
                <div className="absolute right-0 top-0 w-16 h-full bg-gradient-to-l from-blue-100 to-transparent pointer-events-none"></div>
            </div>

            {/* CSS Animation */}
            <style jsx>{`
        @keyframes scroll {
          from {
            transform: translateX(0);
          }
          to {
            transform: translateX(-50%);
          }
        }
        
        .animate-scroll {
          animation: scroll 30s linear infinite;
          animation-play-state: running;
        }
      `}</style>
        </div>
    );
}