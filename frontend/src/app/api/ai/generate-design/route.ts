import { NextRequest, NextResponse } from 'next/server';

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

export async function POST(request: NextRequest) {
  try {
    const { prompt, lang } = await request.json();

    if (!prompt) {
      return NextResponse.json({ error: 'Prompt is required' }, { status: 400 });
    }

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: `You are a professional web designer specializing in European business directories. Create clean, modern HTML components using Tailwind CSS. Use the brand color #1f4fff (class: bg-brand, text-brand, border-brand). Focus on accessibility, responsive design, and European design patterns. Return only valid HTML with Tailwind classes, no explanations or markdown.`
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        max_tokens: 2000,
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: `OpenAI API error: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    const generatedHTML = data.choices[0]?.message?.content || '';

    // Clean up the HTML (remove markdown code blocks if present)
    const cleanHTML = generatedHTML
      .replace(/```html\n?/g, '')
      .replace(/```\n?/g, '')
      .trim();

    return NextResponse.json({ html: cleanHTML });

  } catch (error) {
    console.error('AI Design Generator Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}