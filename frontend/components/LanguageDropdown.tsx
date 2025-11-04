"use client";

import { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';
import { usePathname } from 'next/navigation';

interface Language {
    code: string;
    name: string;
    flag: string;
}

interface LanguageDropdownProps {
    currentLanguage?: string;
    displayMode: 'flags' | 'names' | 'both';
}

const LANGUAGES: Language[] = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'nl', name: 'Nederlands', flag: '🇳🇱' },
    { code: 'pt', name: 'Português', flag: '🇵🇹' },
];

// Rectangle flag components for better design
const FlagIcon = ({ code }: { code: string }) => {
    const flagMap: Record<string, string> = {
        'en': '/flags/gb.svg',
        'de': '/flags/de.svg',
        'fr': '/flags/fr.svg',
        'es': '/flags/es.svg',
        'nl': '/flags/nl.svg',
        'pt': '/flags/pt.svg',
    };

    // Fallback to emoji if SVG not available
    const emojiMap: Record<string, string> = {
        'en': '🇬🇧',
        'de': '🇩🇪',
        'fr': '🇫🇷',
        'es': '🇪🇸',
        'nl': '🇳🇱',
        'pt': '🇵🇹',
    };

    return (
        <div className="w-6 h-4 rounded-sm overflow-hidden flex items-center justify-center bg-gray-100 border border-gray-200">
            <img
                src={flagMap[code]}
                alt={`${code} flag`}
                className="w-full h-full object-cover"
                onError={(e) => {
                    // Fallback to emoji on error
                    const target = e.target as HTMLElement;
                    target.style.display = 'none';
                    const parent = target.parentElement;
                    if (parent) {
                        parent.innerHTML = `<span class="text-xs">${emojiMap[code]}</span>`;
                    }
                }}
            />
        </div>
    );
};

export default function LanguageDropdown({ currentLanguage = 'en', displayMode = 'both' }: LanguageDropdownProps) {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const pathname = usePathname();

    const currentLang = LANGUAGES.find(lang => lang.code === currentLanguage) || LANGUAGES[0];

    // Function to generate the URL for a different language
    const generateLanguageUrl = (languageCode: string) => {
        // Check if current path is a country URL (e.g., /country/be, /country/es)
        const pathParts = pathname.split('/').filter(part => part); // Remove empty strings

        if (pathParts[0] === 'country' && pathParts[1]) {
            // Country URL - switch to language-based country page
            return `/${languageCode}/countries/${pathParts[1]}`;
        } else if (pathParts[0] && LANGUAGES.some(lang => lang.code === pathParts[0])) {
            // Language-based URL - replace language code
            pathParts[0] = languageCode;
            return '/' + pathParts.join('/');
        } else {
            // Default case - add language code
            return `/${languageCode}${pathname}`;
        }
    };

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const renderLanguageContent = (language: Language, isButton = false) => {
        switch (displayMode) {
            case 'flags':
                return (
                    <div className="flex items-center space-x-2">
                        <FlagIcon code={language.code} />
                        {isButton && <span className="uppercase text-xs font-medium">{language.code}</span>}
                    </div>
                );
            case 'names':
                return <span className="text-sm font-medium">{language.name}</span>;
            case 'both':
            default:
                return (
                    <div className="flex items-center space-x-2">
                        <FlagIcon code={language.code} />
                        <span className="text-sm font-medium">{language.name}</span>
                    </div>
                );
        }
    };

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg text-slate-600 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 border border-gray-200"
                aria-expanded={isOpen}
                aria-haspopup="listbox"
            >
                {renderLanguageContent(currentLang, true)}
                <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {isOpen && (
                <div className="absolute top-full right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50 py-2">
                    <div className="px-3 py-2 text-xs font-medium text-gray-500 uppercase tracking-wide border-b border-gray-100">
                        Select Language
                    </div>
                    {LANGUAGES.map((language) => (
                        <a
                            key={language.code}
                            href={generateLanguageUrl(language.code)}
                            className={`flex items-center justify-between px-3 py-2 text-sm hover:bg-blue-50 transition-colors ${currentLanguage === language.code ? 'bg-blue-50 text-blue-600' : 'text-gray-700'
                                }`}
                            onClick={() => setIsOpen(false)}
                        >
                            {renderLanguageContent(language)}
                            {currentLanguage === language.code && (
                                <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                            )}
                        </a>
                    ))}
                </div>
            )}
        </div>
    );
}