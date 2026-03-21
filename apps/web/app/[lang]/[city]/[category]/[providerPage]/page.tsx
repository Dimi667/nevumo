import { notFound } from 'next/navigation';
import { getProviderBySlug, getCategories } from '@/lib/api';
import LeadForm from '@/components/LeadForm';

type ProviderRouteParams = {
  lang: string;
  city: string;
  category: string;
  providerPage: string;
};

function formatPrice(price: number | null, priceType: string): string {
  if (priceType === 'request' || price === null) return 'Price on request';
  if (priceType === 'hourly') return `${price} лв./h`;
  return `${price} лв.`;
}

export async function generateMetadata(props: { params: Promise<ProviderRouteParams> }) {
  const { lang, category, providerPage } = await props.params;
  try {
    const [provider, categories] = await Promise.all([
      getProviderBySlug(providerPage),
      getCategories(lang),
    ]);
    if (!provider) return { title: 'Nevumo' };
    const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
    return { title: `${provider.business_name} | ${categoryName} | Nevumo` };
  } catch {
    return { title: 'Nevumo' };
  }
}

export default async function Page(props: { params: Promise<ProviderRouteParams> }) {
  const { city, category, providerPage } = await props.params;
  const provider = await getProviderBySlug(providerPage);
  if (!provider) return notFound();

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto space-y-5">

        {/* Provider info */}
        <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {provider.business_name}
          </h1>
          {provider.description && (
            <p className="text-gray-600 mb-4">{provider.description}</p>
          )}
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-amber-500 font-semibold text-lg">
              ★ {provider.rating.toFixed(1)}
            </span>
            {provider.verified && (
              <span className="inline-flex items-center gap-1 text-sm font-semibold text-green-700 bg-green-50 border border-green-200 px-3 py-1 rounded-full">
                ✓ Verified
              </span>
            )}
          </div>
        </section>

        {/* Services */}
        {provider.services.length > 0 && (
          <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Services</h2>
            <ul className="divide-y divide-gray-50">
              {provider.services.map((service) => (
                <li key={service.id} className="flex justify-between items-start py-3 first:pt-0 last:pb-0">
                  <div className="flex-1 min-w-0 pr-4">
                    <p className="font-semibold text-gray-800">{service.title}</p>
                    {service.description && (
                      <p className="text-sm text-gray-500 mt-0.5">{service.description}</p>
                    )}
                  </div>
                  <span className="text-sm font-semibold text-gray-700 whitespace-nowrap">
                    {formatPrice(service.base_price, service.price_type)}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Contact form */}
        <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Contact Provider</h2>
          <LeadForm
            categorySlug={category}
            citySlug={city}
            providerSlug={provider.slug}
          />
        </section>

      </div>
    </main>
  );
}
