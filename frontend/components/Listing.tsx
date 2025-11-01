import { ApiResponse, Breadcrumb, Business, Category, Country, City, Town } from '@/lib/api';
import { translate, Language, getTranslatedPath } from '@/lib/i18n';
import CategoryCard from './CategoryCard';

interface ListingProps {
  data: ApiResponse;
  lang: string;
}

function BreadcrumbNav({ breadcrumbs }: { breadcrumbs: Breadcrumb[] }) {
  return (
    <nav className="flex mb-6" aria-label="Breadcrumb">
      <ol className="inline-flex items-center space-x-1 md:space-x-3">
        {breadcrumbs.map((crumb, index) => (
          <li key={index} className="inline-flex items-center">
            {index > 0 && (
              <span className="mx-2 text-gray-400">/</span>
            )}
            <a
              href={crumb.href}
              className="text-gray-700 hover:text-primary-600"
            >
              {crumb.label}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

function CategoryGrid({ items, lang }: { items: Category[]; lang: string }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((category) => (
        <CategoryCard 
          key={category.slug}
          category={category}
          lang={lang}
        />
      ))}
    </div>
  );
}

function CountryGrid({ items, categorySlug, lang }: { items: Country[]; categorySlug?: string; lang: string }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((country) => (
        <div key={country.code} className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
          <h3 className="text-lg font-semibold mb-2">{country.name}</h3>
          <p className="text-gray-600 mb-3">{country.count} {translate('common.businesses', lang as Language)}</p>
          <a
            href={categorySlug ? `/${lang}/${country.code}/${categorySlug}` : `/${lang}/${country.code}`}
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            {translate('common.view', lang as Language)} →
          </a>
        </div>
      ))}
    </div>
  );
}

function CityGrid({ items, categorySlug, countryCode, lang }: { items: City[]; categorySlug?: string; countryCode?: string; lang: string }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {items.map((city) => (
        <div key={city.slug} className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
          <h3 className="font-semibold mb-1">{city.name}</h3>
          <p className="text-gray-600 text-sm mb-2">{city.count} {translate('common.businesses', lang as Language)}</p>
          <a
            href={`/${lang}/${countryCode}/${city.slug}/${categorySlug}`}
            className="text-primary-600 hover:text-primary-700 text-sm font-medium"
          >
            {translate('common.view', lang as Language)} →
          </a>
        </div>
      ))}
    </div>
  );
}

function TownGrid({ items, categorySlug, countryCode, citySlug, lang }: { 
  items: Town[]; 
  categorySlug?: string; 
  countryCode?: string; 
  citySlug?: string;
  lang: string;
}) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">
      {items.map((town) => (
        <div key={town.slug} className="bg-white rounded-lg shadow p-3 hover:shadow-md transition-shadow">
          <h4 className="font-medium mb-1">{town.name}</h4>
          <p className="text-gray-600 text-xs mb-2">{town.count} {translate('common.businesses', lang as Language)}</p>
          <a
            href={`/${lang}/${countryCode}/${citySlug}/${town.slug}/${categorySlug}`}
            className="text-primary-600 hover:text-primary-700 text-xs font-medium"
          >
            {translate('common.view', lang as Language)} →
          </a>
        </div>
      ))}
    </div>
  );
}

function BusinessGrid({ items, lang }: { items: Business[]; lang: string }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((business) => (
        <div key={business.slug} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
          <h3 className="text-xl font-semibold mb-2">{business.name}</h3>
          <div className="text-gray-600 space-y-1 mb-4">
            <p>{business.city_name}{business.town_name && `, ${business.town_name}`}</p>
            {business.street && <p>{business.street}</p>}
            {business.postcode && <p>{business.postcode}</p>}
            {business.phone && <p>{translate('common.phone', lang as Language)}: {business.phone}</p>}
            {business.email && <p>{translate('common.email', lang as Language)}: {business.email}</p>}
          </div>
          {business.website && (
            <a
              href={business.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              {translate('common.visit_website', lang as Language)} →
            </a>
          )}
        </div>
      ))}
    </div>
  );
}

function EmptyState({ level, lang }: { level: string; lang: string }) {
  return (
    <div className="text-center py-12">
      <div className="mb-6">
        <h3 className="text-xl font-medium text-gray-900 mb-2">
          {translate('common.no_results_found', lang as Language)}
        </h3>
        <p className="text-gray-600">
          {translate('common.no_businesses_found', lang as Language)}
        </p>
      </div>
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-md mx-auto">
        <h4 className="font-medium text-blue-900 mb-2">
          {translate('common.add_business_free', lang as Language)}
        </h4>
        <p className="text-blue-700 text-sm mb-4">
          {translate('common.add_business_help', lang as Language)}
        </p>
        <button className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 transition-colors">
          {translate('common.add_business', lang as Language)}
        </button>
      </div>
    </div>
  );
}

export default function Listing({ data, lang }: ListingProps) {
  const { level, breadcrumbs, items } = data;

  // Extract URL parameters from breadcrumbs for navigation
  const categorySlug = breadcrumbs.find(b => b.href.includes('/categories/'))?.href.split('/').pop();
  const countryCode = breadcrumbs.find(b => b.href.match(/\/[A-Z]{2}\//))?.href.match(/\/([A-Z]{2})\//)?.[1];
  const citySlug = breadcrumbs.find(b => b.href.split('/').length >= 5)?.href.split('/')[4];

  return (
    <div className="container mx-auto px-4 py-8">
      <BreadcrumbNav breadcrumbs={breadcrumbs} />
      
      {items.length === 0 ? (
        <EmptyState level={level} lang={lang} />
      ) : (
        <>
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">
              {breadcrumbs[breadcrumbs.length - 1]?.label || translate('common.results', lang as Language)}
            </h1>
            <p className="text-gray-600">
              {items.length} {level === 'categories' ? translate('common.categories', lang as Language) : level === 'results' ? translate('common.businesses', lang as Language) : translate('common.locations', lang as Language)} {translate('common.found', lang as Language)}
            </p>
          </div>

          {level === 'categories' && <CategoryGrid items={items as Category[]} lang={lang} />}
          {level === 'category' && <CountryGrid items={items as Country[]} categorySlug={categorySlug} lang={lang} />}
          {level === 'country' && <CityGrid items={items as City[]} categorySlug={categorySlug} countryCode={countryCode} lang={lang} />}
          {level === 'city' && <TownGrid items={items as Town[]} categorySlug={categorySlug} countryCode={countryCode} citySlug={citySlug} lang={lang} />}
          {level === 'town' && <BusinessGrid items={items as Business[]} lang={lang} />}
          {level === 'results' && <BusinessGrid items={items as Business[]} lang={lang} />}
        </>
      )}
    </div>
  );
}