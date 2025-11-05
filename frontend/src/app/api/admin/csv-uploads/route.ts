import { NextRequest, NextResponse } from 'next/server';

// CSV Upload Management API
export async function GET(request: NextRequest) {
  try {
    const djangoResponse = await fetch('http://127.0.0.1:8000/api/v1/api/csv-upload/', {
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
    console.error('CSV uploads fetch error:', error);
    return NextResponse.json({ 
      error: 'Failed to fetch CSV uploads',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    // Get the form data from the request
    const formData = await request.formData();
    
    // Forward the form data to Django
    const djangoResponse = await fetch('http://127.0.0.1:8000/api/v1/api/csv-upload/', {
      method: 'POST',
      headers: {
        'Authorization': request.headers.get('authorization') || '',
      },
      body: formData,
    });

    if (!djangoResponse.ok) {
      const errorData = await djangoResponse.json().catch(() => ({}));
      throw new Error(errorData.error || `Django API error: ${djangoResponse.status}`);
    }

    const data = await djangoResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('CSV upload error:', error);
    return NextResponse.json({ 
      error: 'Failed to upload CSV file',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}