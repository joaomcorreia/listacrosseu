'use client';

import { useState } from 'react';

// 27 EU languages configuration
const EU_LANGUAGES = [
    { code: 'bg', name: 'Bulgarian', nativeName: 'Български', flag: '🇧🇬' },
    { code: 'hr', name: 'Croatian', nativeName: 'Hrvatski', flag: '🇭🇷' },
    { code: 'cs', name: 'Czech', nativeName: 'Čeština', flag: '🇨🇿' },
    { code: 'da', name: 'Danish', nativeName: 'Dansk', flag: '🇩🇰' },
    { code: 'nl', name: 'Dutch', nativeName: 'Nederlands', flag: '🇳🇱' },
    { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
    { code: 'et', name: 'Estonian', nativeName: 'Eesti', flag: '🇪🇪' },
    { code: 'fi', name: 'Finnish', nativeName: 'Suomi', flag: '🇫🇮' },
    { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪' },
    { code: 'el', name: 'Greek', nativeName: 'Ελληνικά', flag: '🇬🇷' },
    { code: 'hu', name: 'Hungarian', nativeName: 'Magyar', flag: '🇭🇺' },
    { code: 'ga', name: 'Irish', nativeName: 'Gaeilge', flag: '🇮🇪' },
    { code: 'it', name: 'Italian', nativeName: 'Italiano', flag: '🇮🇹' },
    { code: 'lv', name: 'Latvian', nativeName: 'Latviešu', flag: '🇱🇻' },
    { code: 'lt', name: 'Lithuanian', nativeName: 'Lietuvių', flag: '🇱🇹' },
    { code: 'mt', name: 'Maltese', nativeName: 'Malti', flag: '🇲🇹' },
    { code: 'pl', name: 'Polish', nativeName: 'Polski', flag: '🇵🇱' },
    { code: 'pt', name: 'Portuguese', nativeName: 'Português', flag: '🇵🇹' },
    { code: 'ro', name: 'Romanian', nativeName: 'Română', flag: '🇷🇴' },
    { code: 'sk', name: 'Slovak', nativeName: 'Slovenčina', flag: '🇸🇰' },
    { code: 'sl', name: 'Slovenian', nativeName: 'Slovenščina', flag: '🇸🇮' },
    { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸' },
    { code: 'sv', name: 'Swedish', nativeName: 'Svenska', flag: '🇸🇪' },
    // Additional regional languages
    { code: 'ca', name: 'Catalan', nativeName: 'Català', flag: '🏴󠁥󠁳󠁣󠁴󠁿' },
    { code: 'eu', name: 'Basque', nativeName: 'Euskera', flag: '🏴󠁥󠁳󠁰󠁶󠁿' },
    { code: 'gl', name: 'Galician', nativeName: 'Galego', flag: '🏴󠁥󠁳󠁧󠁡󠁿' }
];

interface LanguageSelectorProps {
    selectedLanguage: string;
    onLanguageChange: (languageCode: string) => void;
    className?: string;
    showFlag?: boolean;
    showNativeName?: boolean;
}

export default function LanguageSelector({
    selectedLanguage,
    onLanguageChange,
    className = '',
    showFlag = true,
    showNativeName = true
}: LanguageSelectorProps) {
    const [isOpen, setIsOpen] = useState(false);

    const selectedLang = EU_LANGUAGES.find(lang => lang.code === selectedLanguage) || EU_LANGUAGES[5]; // Default to English

    return (
        <div className={`relative inline-block text-left ${className}`}>
            <div>
                <button
                    type="button"
                    className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    onClick={() => setIsOpen(!isOpen)}
                    aria-expanded="true"
                    aria-haspopup="true"
                >
                    <div className="flex items-center space-x-2">
                        {showFlag && <span className="text-lg">{selectedLang.flag}</span>}
                        <span>{showNativeName ? selectedLang.nativeName : selectedLang.name}</span>
                    </div>
                    <svg className="-mr-1 ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                </button>
            </div>

            {isOpen && (
                <div className="origin-top-right absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50 max-h-96 overflow-y-auto">
                    <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                        {EU_LANGUAGES.map((language) => (
                            <button
                                key={language.code}
                                className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 flex items-center space-x-3 ${selectedLanguage === language.code ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
                                    }`}
                                role="menuitem"
                                onClick={() => {
                                    onLanguageChange(language.code);
                                    setIsOpen(false);
                                }}
                            >
                                <span className="text-lg">{language.flag}</span>
                                <div className="flex flex-col">
                                    <span className="font-medium">{language.nativeName}</span>
                                    <span className="text-xs text-gray-500">{language.name}</span>
                                </div>
                                {selectedLanguage === language.code && (
                                    <span className="ml-auto text-blue-600">✓</span>
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Overlay for mobile */}
            {isOpen && (
                <div
                    className="fixed inset-0 z-40 lg:hidden"
                    onClick={() => setIsOpen(false)}
                />
            )}
        </div>
    );
}

// Export language utilities
export { EU_LANGUAGES };
export type Language = typeof EU_LANGUAGES[0];