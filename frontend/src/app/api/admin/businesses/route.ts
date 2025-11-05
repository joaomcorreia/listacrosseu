import { NextRequest, NextResponse } from 'next/server';

// Business Management API
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = searchParams.get('page') || '1';
    const limit = searchParams.get('limit') || '20';
    const search = searchParams.get('search') || '';
    const category = searchParams.get('category') || '';
    const imported_from_csv = searchParams.get('imported_from_csv') || '';
    
    // Build query parameters
    const params = new URLSearchParams({
      page,
      limit,
    });
    
    if (search) params.append('search', search);
    if (category) params.append('category', category);
    if (imported_from_csv) params.append('imported_from_csv', imported_from_csv);

    const djangoResponse = await fetch(`http://127.0.0.1:8000/api/v1/businesses/?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!djangoResponse.ok) {
      throw new Error(`Django API error: ${djangoResponse.status}`);
    }

    const data = await djangoResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Businesses fetch error:', error);
    return NextResponse.json({ 
      error: 'Failed to fetch businesses',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}