'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { getAvailableLanguages, getLanguageName, Language } from '@/lib/i18n';

interface LanguageSwitcherProps {
  currentLang: Language;
}

export default function LanguageSwitcher({ currentLang }: LanguageSwitcherProps) {
  const pathname = usePathname();
  const languages = getAvailableLanguages();

  // Remove the current language from the pathname to get the base path
  const basePath = pathname.replace(`/${currentLang}`, '') || '/';

  return (
    <div className="relative inline-block">
      <div className="flex space-x-1">
        {languages.map((lang) => (
          <Link
            key={lang}
            href={`/${lang}${basePath}`}
            className={`px-2 py-1 text-sm rounded transition-colors ${
              lang === currentLang
                ? 'bg-blue-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
            title={getLanguageName(lang)}
          >
            {lang.toUpperCase()}
          </Link>
        ))}
      </div>
    </div>
  );
}