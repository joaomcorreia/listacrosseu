import { useState, useEffect } from 'react';

interface DjangoAdminProps {
  path?: string;
  height?: string;
}

export default function DjangoAdmin({ path = '', height = '800px' }: DjangoAdminProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const djangoAdminUrl = `http://127.0.0.1:8000/admin/${path}`;

  return (
    <div className="w-full">
      {isLoading && (
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading Django Admin...</span>
        </div>
      )}
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 m-4">
          <h3 className="text-red-800 font-medium">Django Admin Error</h3>
          <p className="text-red-600 text-sm mt-1">{error}</p>
          <a 
            href={djangoAdminUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-2 text-blue-600 hover:text-blue-800 underline"
          >
            Open Django Admin in new tab
          </a>
        </div>
      )}
      
      <iframe
        src={djangoAdminUrl}
        width="100%"
        height={height}
        style={{ border: 'none' }}
        className={`rounded-lg shadow-sm ${isLoading ? 'hidden' : 'block'}`}
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setError('Failed to load Django Admin. Make sure Django server is running on port 8000.');
          setIsLoading(false);
        }}
        title="Django Admin"
      />
      
      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="font-medium text-blue-900">Django Admin Integration</h4>
        <p className="text-blue-700 text-sm mt-1">
          This iframe shows the Django admin interface. You can also access it directly at:{' '}
          <a 
            href={djangoAdminUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="underline hover:text-blue-900"
          >
            {djangoAdminUrl}
          </a>
        </p>
      </div>
    </div>
  );
}