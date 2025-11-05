import { NextResponse } from 'next/server';
import { v4 as uuid } from 'uuid';
import type { Listing } from '@/types/listing';
import { saveFreeListing } from '@/server/mockDb';

export async function POST(req: Request) {
  const body = await req.json();
  const now = new Date().toISOString();
  const listing: Listing = {
    id: uuid(),
    businessName: body.businessName,
    country: body.country,
    city: body.city,
    category: body.category,
    address: body.address || '',
    website: body.website || '',
    email: body.email,
    phone: body.phone || '',
    description: body.description || '',
    plan: 'free',
    status: 'pending',
    ownerUserId: null,
    claimedByEmail: null,
    createdAt: now,
    updatedAt: now
  };
  saveFreeListing(listing);
  return NextResponse.json({ ok: true, listingId: listing.id }, { status: 201 });
}