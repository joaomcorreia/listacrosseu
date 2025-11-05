import { NextResponse } from 'next/server';
import { getSeo, putSeo } from '@/server/mockDb';
import type { SeoByLang } from '@/types/seo';

export async function GET(_: Request, { params }: { params: { id: string } }) {
  const seo = getSeo(params.id);
  if (!seo) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(seo);
}

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  const body = (await req.json()) as SeoByLang;
  const updated = putSeo(params.id, body);
  if (!updated) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(updated.seo);
}