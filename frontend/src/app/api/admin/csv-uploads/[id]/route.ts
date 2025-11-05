import { NextRequest, NextResponse } from 'next/server';

// Get CSV upload status by ID
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const uploadId = params.id;
    
    const djangoResponse = await fetch(`http://127.0.0.1:8000/api/v1/api/csv-upload/${uploadId}/status/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!djangoResponse.ok) {
      if (djangoResponse.status === 404) {
        return NextResponse.json({ error: 'CSV upload not found' }, { status: 404 });
      }
      throw new Error(`Django API error: ${djangoResponse.status}`);
    }

    const data = await djangoResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('CSV upload status fetch error:', error);
    return NextResponse.json({ 
      error: 'Failed to fetch CSV upload status',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}