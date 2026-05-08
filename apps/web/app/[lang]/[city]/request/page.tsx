import Link from 'next/link';
import { generateHreflangAlternates } from '@/lib/seo';
import { Metadata } from 'next';

interface Props {
  params: Promise<{ lang: string; city: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang, city } = await params;

  return {
    title: `Request Services in ${city} | Nevumo`,
    description: `Submit a service request in ${city}. Connect with local service providers.`,
    alternates: {
      canonical: `/${lang}/${city}/request`,
      languages: generateHreflangAlternates(`/${city}/request`),
    },
    robots: { index: false, follow: true },
  };
}

export default async function RequestPage({ params }: Props) {
  const { lang, city } = await params;
  return (
    <div className="p-4 text-center min-h-screen flex flex-col items-center justify-center">
      <h1>Lead Form Coming Soon for {city}</h1>
      <p>This feature is being developed. Please check back later or explore other services.</p>
      <Link href={`/${lang}/${city}`} className="mt-4 text-blue-500 underline">Back to {city} page</Link>
    </div>
  );
}
