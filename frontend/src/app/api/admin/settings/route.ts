import { NextResponse } from 'next/server';
import { getSiteSettings, updateSiteSettings } from '@/server/mockDb';

export async function GET() {
  const settings = getSiteSettings();
  return NextResponse.json(settings);
}

export async function POST(req: Request) {
  try {
    const updates = await req.json();
    const settings = updateSiteSettings(updates);
    return NextResponse.json({ ok: true, settings });
  } catch (error) {
    return NextResponse.json({ ok: false, error: 'Failed to update settings' }, { status: 400 });
  }
}