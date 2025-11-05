import { NextResponse } from 'next/server';
import { getPage, updatePage } from '@/server/mockDb';

export async function GET(_: Request, { params }: { params: { id: string } }) {
  const page = getPage(params.id);
  if (!page) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(page);
}

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  const patch = await req.json();
  const page = updatePage(params.id, patch);
  if (!page) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(page);
}