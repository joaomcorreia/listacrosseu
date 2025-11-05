import { NextRequest, NextResponse } from 'next/server';

// Get CSV upload progress
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const uploadId = params.id;
    
    // Get progress from Django backend
    const djangoResponse = await fetch(`http://127.0.0.1:8000/api/v1/api/csv-upload/${uploadId}/progress/`, {
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
    console.error('CSV upload progress fetch error:', error);
    return NextResponse.json({ 
      error: 'Failed to fetch CSV upload progress',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}