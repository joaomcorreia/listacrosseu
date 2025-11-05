export type Plan = 'free'|'growth'|'premium';
export type ListingStatus = 'pending'|'approved'|'rejected';

export type Listing = {
  id: string;
  businessName: string;
  country: string;
  city: string;
  category: string;
  address?: string;
  website?: string;
  email: string;
  phone?: string;
  description?: string;
  plan: Plan;
  status: ListingStatus;
  ownerUserId?: string | null; // null for unclaimed
  claimedByEmail?: string | null;
  createdAt: string; updatedAt: string;
};

export type ClaimSubmission = {
  listingId: string;
  claimantEmail: string;
  message?: string;
};

export type UpgradeSubmission = {
  listingId: string;
  targetPlan: Plan; // 'growth' or 'premium'
  contactEmail: string;
  notes?: string;
};