'use client';

import { useState, useEffect } from 'react';

export default function TestApiPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function testApi() {
      try {
        const response = await fetch('/api/v1/search/businesses/?q=restaurant&limit=5');
        const result = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    testApi();
  }, []);

  if (loading) return <div className="p-8">Loading API test...</div>;
  if (error) return <div className="p-8 text-red-600">Error: {error}</div>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      <div className="bg-gray-100 p-4 rounded">
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}