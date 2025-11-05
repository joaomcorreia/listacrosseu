import { NextResponse } from 'next/server';
import type { UpgradeSubmission } from '@/types/listing';
import { saveUpgrade } from '@/server/mockDb';

export async function POST(req: Request) {
  const body = (await req.json()) as UpgradeSubmission;
  if (!body.listingId || !body.targetPlan || !body.contactEmail) {
    return NextResponse.json({ ok:false, error:'Missing fields' }, { status: 400 });
  }
  if (!['growth','premium'].includes(body.targetPlan)) {
    return NextResponse.json({ ok:false, error:'Invalid plan' }, { status: 400 });
  }
  saveUpgrade(body);
  return NextResponse.json({ ok: true });
}