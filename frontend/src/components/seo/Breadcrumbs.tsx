import { SeoPage } from '../../lib/seoApi';

interface BreadcrumbsProps {
  seoPage: SeoPage;
}

/**
 * Breadcrumbs component that renders navigation breadcrumbs
 * Only available for Premium plan pages
 */
export default function Breadcrumbs({ seoPage }: BreadcrumbsProps) {
  if (!seoPage.can_use_premium_features || !seoPage.breadcrumbs || seoPage.breadcrumbs.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Breadcrumb" className="breadcrumbs">
      <ol className="breadcrumb-list">
        {seoPage.breadcrumbs.map((crumb, index) => (
          <li key={index} className="breadcrumb-item">
            {index < seoPage.breadcrumbs!.length - 1 ? (
              <>
                <a href={crumb.url} className="breadcrumb-link">
                  {crumb.name}
                </a>
                <span className="breadcrumb-separator" aria-hidden="true">
                  /
                </span>
              </>
            ) : (
              <span className="breadcrumb-current" aria-current="page">
                {crumb.name}
              </span>
            )}
          </li>
        ))}
      </ol>
      
      <style jsx>{`
        .breadcrumbs {
          margin-bottom: 1rem;
        }
        .breadcrumb-list {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          list-style: none;
          margin: 0;
          padding: 0;
          font-size: 0.875rem;
          color: #666;
        }
        .breadcrumb-item {
          display: flex;
          align-items: center;
        }
        .breadcrumb-link {
          color: #2563eb;
          text-decoration: none;
          transition: color 0.2s;
        }
        .breadcrumb-link:hover {
          color: #1d4ed8;
          text-decoration: underline;
        }
        .breadcrumb-separator {
          margin: 0 0.5rem;
          color: #9ca3af;
        }
        .breadcrumb-current {
          color: #374151;
          font-weight: 500;
        }
      `}</style>
    </nav>
  );
}