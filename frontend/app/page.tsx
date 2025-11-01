import { redirect } from 'next/navigation';

export default function RootPage() {
  // Redirect to English by default
  // In a real app, you might want to detect the user's language preference
  redirect('/en');
}