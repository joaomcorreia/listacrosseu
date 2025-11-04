'use client';

import { useState, useRef, useEffect } from 'react';
import { useLanguageSwitcher } from '@/lib/useLanguageSwitcher';
import { SUPPORTED_LOCALES, type Locale } from '@/lib/i18n';

// Language display names and flags
const LANGUAGE_INFO: Record<Locale, { name: string; flag: string; nativeName: string }> = {
  en: { name: 'English', flag: '🇬🇧', nativeName: 'English' },
  es: { name: 'Spanish', flag: '🇪🇸', nativeName: 'Español' },
  fr: { name: 'French', flag: '🇫🇷', nativeName: 'Français' },
  de: { name: 'German', flag: '🇩🇪', nativeName: 'Deutsch' },
  nl: { name: 'Dutch', flag: '🇳🇱', nativeName: 'Nederlands' },
  pt: { name: 'Portuguese', flag: '🇵🇹', nativeName: 'Português' },
  it: { name: 'Italian', flag: '🇮🇹', nativeName: 'Italiano' },
  pl: { name: 'Polish', flag: '🇵🇱', nativeName: 'Polski' },
  cs: { name: 'Czech', flag: '🇨🇿', nativeName: 'Čeština' },
  sk: { name: 'Slovak', flag: '🇸🇰', nativeName: 'Slovenčina' },
  hu: { name: 'Hungarian', flag: '🇭🇺', nativeName: 'Magyar' },
  ro: { name: 'Romanian', flag: '🇷🇴', nativeName: 'Română' },
  bg: { name: 'Bulgarian', flag: '🇧🇬', nativeName: 'Български' },
  hr: { name: 'Croatian', flag: '🇭🇷', nativeName: 'Hrvatski' },
  sl: { name: 'Slovenian', flag: '🇸🇮', nativeName: 'Slovenščina' },
  et: { name: 'Estonian', flag: '🇪🇪', nativeName: 'Eesti' },
  lv: { name: 'Latvian', flag: '🇱🇻', nativeName: 'Latviešu' },
  lt: { name: 'Lithuanian', flag: '🇱🇹', nativeName: 'Lietuvių' },
  mt: { name: 'Maltese', flag: '🇲🇹', nativeName: 'Malti' },
  cy: { name: 'Welsh', flag: '🏴󠁧󠁢󠁷󠁬󠁳󠁿', nativeName: 'Cymraeg' },
  fi: { name: 'Finnish', flag: '🇫🇮', nativeName: 'Suomi' },
  se: { name: 'Swedish', flag: '🇸🇪', nativeName: 'Svenska' },
  da: { name: 'Danish', flag: '🇩🇰', nativeName: 'Dansk' },
  no: { name: 'Norwegian', flag: '🇳🇴', nativeName: 'Norsk' },
  is: { name: 'Icelandic', flag: '🇮🇸', nativeName: 'Íslenska' },
  ie: { name: 'Irish', flag: '🇮🇪', nativeName: 'Gaeilge' },
  lu: { name: 'Luxembourgish', flag: '🇱🇺', nativeName: 'Lëtzebuergesch' },
};

interface LanguageSwitcherProps {
  displayMode?: 'flag' | 'text' | 'both';
  showDropdown?: boolean;
  className?: string;
}

export default function LanguageSwitcher({ 
  displayMode = 'both', 
  showDropdown = true,
  className = ''
}: LanguageSwitcherProps) {
  const { currentLocale, switchLanguage } = useLanguageSwitcher();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentLangInfo = LANGUAGE_INFO[currentLocale];

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLanguageChange = (locale: Locale) => {
    switchLanguage(locale);
    setIsOpen(false);
  };

  if (!showDropdown) {
    // Simple display mode without dropdown
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <span className="text-gray-500">🌐</span>
        {displayMode !== 'text' && <span>{currentLangInfo.flag}</span>}
        {displayMode !== 'flag' && <span className="text-sm font-medium">{currentLangInfo.nativeName}</span>}
      </div>
    );
  }

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md transition-colors duration-200"
        aria-label="Select language"
      >
        <span className="text-gray-500">🌐</span>
        {displayMode !== 'text' && <span>{currentLangInfo.flag}</span>}
        {displayMode !== 'flag' && <span>{currentLangInfo.nativeName}</span>}
        <span className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg border border-gray-200 z-50 max-h-80 overflow-y-auto">
          <div className="py-1">
            {SUPPORTED_LOCALES.map((locale) => {
              const langInfo = LANGUAGE_INFO[locale];
              const isActive = locale === currentLocale;
              
              return (
                <button
                  key={locale}
                  onClick={() => handleLanguageChange(locale)}
                  className={`w-full text-left px-4 py-2 text-sm transition-colors duration-150 flex items-center space-x-3 ${
                    isActive 
                      ? 'bg-blue-50 text-blue-700 font-medium' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <span className="text-lg">{langInfo.flag}</span>
                  <div className="flex-1">
                    <div className="font-medium">{langInfo.nativeName}</div>
                    <div className="text-xs text-gray-500">{langInfo.name}</div>
                  </div>
                  {isActive && (
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}