import { NextResponse } from 'next/server';
import type { ClaimSubmission } from '@/types/listing';
import { saveClaim } from '@/server/mockDb';

export async function POST(req: Request) {
  const body = (await req.json()) as ClaimSubmission;
  if (!body.listingId || !body.claimantEmail) {
    return NextResponse.json({ ok:false, error:'Missing fields' }, { status: 400 });
  }
  saveClaim(body);
  return NextResponse.json({ ok: true });
}