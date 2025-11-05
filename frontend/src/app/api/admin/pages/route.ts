import { NextResponse } from 'next/server';
import { createPage, listPages } from '@/server/mockDb';

export async function GET() {
  return NextResponse.json(listPages());
}

export async function POST(req: Request) {
  const body = await req.json();
  const page = createPage({
    name: body.name,
    path: body.path,
    type: body.type || 'static',
    langs: body.langs || ['NL','PT','EN','FR','DE','ES']
  });
  return NextResponse.json(page, { status: 201 });
}