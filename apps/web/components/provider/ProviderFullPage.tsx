'use client';

import { useState, useCallback } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import AboutSection from './AboutSection';
import LeadPanel from './LeadPanel';
import StickyProviderCTA from './StickyProviderCTA';
import BottomSheetForm from './BottomSheetForm';
import { ShareButton } from '@/components/shared/ShareButton';

interface GalleryImage {
  id: number;
  url: string;
  position: number;
}

interface ProviderService {
  id: number;
  title: string;
  base_price: number | null;
  price_type: string;
  currency: string;
  description: string | null;
}

interface Review {
  id: string;
  rating: number;
  comment: string | null;
  client_name: string;
  created_at: string;
  provider_reply: string | null;
}

interface ProviderFullPageProps {
  provider: {
    id: string;
    slug: string;
    business_name: string;
    description: string | null;
    profile_image_url: string | null;
    rating: number;
    verification_level: number;
    gallery: GalleryImage[];
    services: ProviderService[];
    reviews: Review[];
    review_count: number;
    jobs_completed: number;
    cities: string[];
    city_name: string;
    category_name: string;
    category_slug: string;
    city_slug: string;
    lang: string;
    leads_received?: number;
    city_leads?: number;
    latest_review?: Review | null;
    latest_lead_city?: string | null;
    latest_lead_client_name?: string | null;
  };
  translations: Record<string, string>;
  lang: string;
}

// Star rating component
function StarRating({ rating }: { rating: number }) {
  return (
    <span className="inline-flex items-center">
      {[1, 2, 3, 4, 5].map((star) => (
        <svg
          key={star}
          className={`w-4 h-4 ${star <= Math.round(rating) ? 'text-yellow-400' : 'text-gray-200'}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </span>
  );
}

// Breadcrumb Section
function BreadcrumbSection({ provider, lang }: { provider: ProviderFullPageProps['provider']; lang: string }) {
  return (
    <nav className="max-w-6xl mx-auto px-4 py-4">
      <ol className="flex items-center gap-2 text-sm text-gray-500">
        <li>
          <Link 
            href={`/${lang}/${provider.city_slug}`}
            className="hover:text-gray-700"
          >
            {provider.city_name}
          </Link>
        </li>
        <li className="text-gray-400">›</li>
        <li>
          <Link 
            href={`/${lang}/${provider.city_slug}/${provider.category_slug}`}
            className="hover:text-gray-700"
          >
            {provider.category_name}
          </Link>
        </li>
        <li className="text-gray-400">›</li>
        <li className="text-gray-900 font-medium">
          {provider.business_name}
        </li>
      </ol>
    </nav>
  );
}

// Hero Section
function HeroSection({ provider, translations }: { provider: ProviderFullPageProps['provider']; translations: Record<string, string> }) {
  const t = translations;
  const coverImage = (provider.gallery ?? []).length > 0 ? (provider.gallery ?? []).find(img => img.position === 0) || (provider.gallery ?? [])[0] : null;

  // Badge logic
  const getBadge = () => {
    if (provider.verification_level === 0) {
      return (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-blue-50 text-blue-400 text-sm font-medium">
          ⚡ {t['badge_new_provider'] ?? 'Нов в Nevumo'}
        </span>
      );
    }
    if (provider.verification_level === 1) {
      return (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-medium">
          ✓ {t['badge_verified'] ?? 'Верифициран'}
        </span>
      );
    }
    if (provider.verification_level === 2) {
      const displayText = (t['badge_top_specialist'] ?? 'Top specialist') + ' – ' + provider.city_name;
      return (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-orange-100 text-orange-700 text-sm font-medium">
          ★ {displayText}
        </span>
      );
    }
    return null;
  };

  return (
    <section className="rounded-xl border border-gray-100 bg-white shadow-sm p-5">
      {/* Cover Image */}
      {(provider.gallery ?? []).length > 0 && (
        <div className="h-48 w-full rounded-xl overflow-hidden mb-4">
          <img
            src={provider.gallery[0].url}
            alt={`${provider.business_name} cover`}
            className="w-full h-full object-cover object-top"
          />
        </div>
      )}

      {/* Avatar + Info */}
      <div className="flex gap-4 mb-4">
        {/* Avatar */}
        <div className="w-16 h-16 rounded-full bg-orange-100 flex items-center justify-center overflow-hidden shrink-0">
          {provider.profile_image_url ? (
            <img
              src={provider.profile_image_url}
              alt={provider.business_name}
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-orange-600 text-lg font-bold">
              {provider.business_name.charAt(0).toUpperCase()}
            </span>
          )}
        </div>

        {/* Name + Category + City */}
        <div className="flex-1">
          <h1 className="text-xl font-bold text-gray-900">{provider.business_name}</h1>
          <p className="text-sm text-gray-600">{provider.category_name}</p>
          <p className="text-xs text-gray-500">{provider.city_name}</p>
        </div>
      </div>

      {/* Badge */}
      <div className="mb-4">
        {getBadge()}
      </div>

      {/* Rating Row */}
      {provider.rating > 0 && provider.review_count > 0 && (
        <div className="flex items-center gap-2 mb-4">
          <StarRating rating={provider.rating} />
          <span className="font-semibold text-gray-900">{provider.rating.toFixed(1)}</span>
          <span className="text-gray-500">
            ({provider.review_count} {t['reviews_count'] ?? 'ревюта'})
          </span>
        </div>
      )}

      {/* Meta Row */}
      <div className="grid grid-cols-4 gap-0 mt-4 pt-4 border-t border-gray-100">
        <div className="text-center">
          <div className="text-base font-semibold text-gray-900">{(provider.services ?? []).length}</div>
          <div className="text-xs text-gray-500">{t['meta_services'] ?? 'Услуги'}</div>
        </div>
        {provider.jobs_completed > 0 && (
          <div className="text-center">
            <div className="text-base font-semibold text-gray-900">{provider.jobs_completed}</div>
            <div className="text-xs text-gray-500">{t['completed_jobs']?.replace('{count}', String(provider.jobs_completed)) ?? 'Завършени'}</div>
          </div>
        )}
        {(provider.cities ?? []).length > 1 && (
          <div className="text-center">
            <div className="text-base font-semibold text-gray-900">{(provider.cities ?? []).length}</div>
            <div className="text-xs text-gray-500">{t['meta_cities'] ?? 'Града'}</div>
          </div>
        )}
        {provider.review_count > 0 && (
          <div className="text-center">
            <div className="text-base font-semibold text-gray-900">{provider.review_count}</div>
            <div className="text-xs text-gray-500">{t['reviews_count'] ?? 'Ревюта'}</div>
          </div>
        )}
      </div>

      {/* Action Row */}
      <div className="mt-4 pt-4 border-t border-gray-100">
        <ShareButton
          title={provider.business_name}
          text={provider.category_name}
          linkCopiedLabel={t['link_copied'] ?? 'Линкът е копиран!'}
          label={t['share_button'] ?? 'Сподели'}
          className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
        />
      </div>
    </section>
  );
}

// Gallery Section
function GallerySection({ gallery, translations }: { gallery: GalleryImage[]; translations: Record<string, string> }) {
  const t = translations;

  if (gallery.length === 0) {
    return null;
  }

  // Sort by position
  const sortedGallery = [...gallery].sort((a, b) => a.position - b.position);

  return (
    <section className="rounded-xl border border-gray-100 bg-white shadow-sm p-5">
      <h2 className="text-base font-semibold text-gray-900 mb-3">
        {t['section_gallery'] ?? 'Галерия'}
      </h2>
      <div className="grid grid-cols-4 gap-2">
        {sortedGallery.map((image, index) => (
          <div 
            key={image.id} 
            className={`rounded-lg overflow-hidden ${index === 0 ? 'col-span-2 row-span-2' : 'aspect-square'}`}
          >
            <img
              src={image.url}
              alt={`Gallery image ${index + 1}`}
              className="w-full h-full object-cover"
            />
          </div>
        ))}
      </div>
    </section>
  );
}

// Services Section
function ServicesSection({ 
  services, 
  translations, 
  selectedService, 
  onServiceSelect 
}: { 
  services: ProviderService[]; 
  translations: Record<string, string>;
  selectedService: number | null;
  onServiceSelect: (serviceId: number) => void;
}) {
  const t = translations;

  if (services.length === 0) {
    return null;
  }

  const formatPrice = (service: ProviderService) => {
    if (!service.base_price || service.price_type === 'request') {
      return t['price_on_request'] ?? 'По запитване';
    }
    if (service.price_type === 'hourly') {
      return `${service.base_price} ${service.currency}${t['price_per_hour'] ?? '/ч'}`;
    }
    if (service.price_type === 'per_sqm') {
      return `${service.base_price} ${service.currency}/m²`;
    }
    return `${service.base_price} ${service.currency}`;
  };

  return (
    <section className="rounded-xl border border-gray-100 bg-white shadow-sm p-5">
      <h2 className="text-base font-semibold text-gray-900 mb-3">
        {t['section_services'] ?? 'Услуги и цени'}
      </h2>
      <div className="space-y-2">
        {services.map((service) => (
          <div
            key={service.id}
            onClick={() => onServiceSelect(service.id)}
            className={`group relative px-4 py-3 bg-gray-50 rounded-lg border transition-all cursor-pointer ${
              selectedService === service.id
                ? 'border-orange-400 bg-orange-50'
                : 'border-transparent hover:border-orange-300 hover:bg-orange-50/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-gray-700">{service.title}</h3>
                {service.description && (
                  <p className="text-xs text-gray-500 mt-0.5">{service.description}</p>
                )}
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <p className="text-sm font-semibold text-gray-900">
                  {formatPrice(service)}
                </p>
                {/* Desktop: Request button on hover OR deselect button when selected */}
                {selectedService === service.id ? (
                  <button className="hidden md:block opacity-0 group-hover:opacity-100 transition-opacity px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">
                    {t['service_deselect'] ?? '✕ Премахни'}
                  </button>
                ) : (
                  <button className="hidden md:block opacity-0 group-hover:opacity-100 transition-opacity px-3 py-1.5 text-xs font-medium text-white bg-orange-500 rounded-lg hover:bg-orange-600">
                    {t['request_service'] ?? 'Заяви услуга'}
                  </button>
                )}
              </div>
            </div>
            {/* Mobile: Select hint based on selection state */}
            <p className="md:hidden text-xs text-orange-600 mt-2">
              {selectedService === service.id
                ? (t['service_selected_confirm'] ?? '✓ Избрана')
                : (t['select_this_service'] ?? 'Избери тази услуга →')
              }
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

// Reviews Section
function ReviewsSection({ reviews, reviewCount, businessName, translations }: { 
  reviews: Review[]; 
  reviewCount: number; 
  businessName: string;
  translations: Record<string, string>;
}) {
  const t = translations;

  if (reviewCount === 0) {
    return null;
  }

  // Calculate average rating
  const averageRating = reviews.length > 0 
    ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length 
    : 0;

  // Display max 5 reviews
  const displayReviews = reviews.slice(0, 5);

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('bg-BG', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  return (
    <section className="rounded-xl border border-gray-100 bg-white shadow-sm p-5">
      <h2 className="text-base font-semibold text-gray-900 mb-3">
        {t['section_reviews'] ?? 'Ревюта'} ({reviewCount})
      </h2>

      {/* Rating overview */}
      <div className="bg-gray-50 rounded-xl p-4 mb-4 flex items-center gap-4">
        <div className="text-3xl font-bold text-gray-900">
          {averageRating.toFixed(1)}
        </div>
        <div>
          <StarRating rating={averageRating} />
          <p className="text-sm text-gray-500 mt-1">{reviewCount} {t['reviews_count'] ?? 'ревюта'}</p>
        </div>
      </div>

      {/* Review cards */}
      <div className="space-y-3">
        {displayReviews.map((review) => (
          <div key={review.id} className="p-4 bg-gray-50 rounded-xl">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center">
                  <span className="text-orange-600 text-sm font-bold">
                    {review.client_name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">{review.client_name}</p>
                  <p className="text-xs text-gray-500">{formatDate(review.created_at)}</p>
                </div>
              </div>
              <StarRating rating={review.rating} />
            </div>
            {review.comment && (
              <p className="text-sm text-gray-600 mt-2">"{review.comment}"</p>
            )}
            {review.provider_reply && (
              <div className="mt-3 pl-3 border-l-2 border-gray-200">
                <p className="text-xs font-medium text-gray-900">
                  Отговор на {businessName}:
                </p>
                <p className="text-xs text-gray-600 mt-1">{review.provider_reply}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

export default function ProviderFullPage({ provider, translations, lang }: ProviderFullPageProps) {
  const t = translations;
  const [selectedService, setSelectedService] = useState<number | null>(null);
  const [isSheetOpen, setIsSheetOpen] = useState(false);

  const formatServicePrice = (service: ProviderService) => {
    if (!service.base_price || service.price_type === 'request') {
      return t['price_on_request'] ?? 'По запитване';
    }
    if (service.price_type === 'hourly') {
      return `${service.base_price} ${service.currency}${t['price_per_hour'] ?? '/ч'}`;
    }
    if (service.price_type === 'per_sqm') {
      return `${service.base_price} ${service.currency}/m²`;
    }
    return `${service.base_price} ${service.currency}`;
  };

  const handleServiceSelect = (serviceId: number) => {
    const isSelecting = selectedService !== serviceId;
    setSelectedService(prev => prev === serviceId ? null : serviceId);
    // Scroll to form only when selecting (not deselecting)
    if (isSelecting) {
      const formElement = document.getElementById('provider-lead-form');
      if (formElement) {
        formElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      // Pre-fill notes
      const serviceText = handleServicePreFill(serviceId);
      if (serviceText) {
        handleNotesPreFill(serviceText);
      }
    }
  };

  const handleNotesPreFill = (text: string) => {
    // This will be passed to LeadPanel/BottomSheetForm to pre-fill their notes state
    // Components will handle adding this text to their local notes state
  };

  const handleServicePreFill = useCallback((serviceId: number) => {
    const service = provider.services.find(s => s.id === serviceId);
    if (!service) return;
    const serviceText = `${service.title} - ${formatServicePrice(service)}`;
    return serviceText;
  }, [provider.services]);

  const handleServiceDeselect = () => {
    setSelectedService(null);
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Breadcrumb */}
      <BreadcrumbSection provider={provider} lang={lang} />
      
      {/* Two-column layout */}
      <div className="max-w-6xl mx-auto px-4 py-6 flex flex-col md:flex-row gap-6">
        {/* LEFT COLUMN */}
        <div className="flex-1 space-y-4">
          <HeroSection provider={provider} translations={t} />
          {(provider.gallery ?? []).length > 1 && <GallerySection gallery={(provider.gallery ?? []).slice(1)} translations={t} />}
          <AboutSection description={provider.description} translations={t} />
          {(provider.services ?? []).length > 0 && (
            <ServicesSection 
              services={provider.services ?? []} 
              translations={t} 
              selectedService={selectedService}
              onServiceSelect={handleServiceSelect}
            />
          )}
          {provider.review_count > 0 && (
            <ReviewsSection 
              reviews={provider.reviews} 
              reviewCount={provider.review_count} 
              businessName={provider.business_name}
              translations={t}
            />
          )}
        </div>
        
        {/* RIGHT COLUMN (sticky) */}
        <div id="provider-lead-form" className="hidden md:block w-[340px] shrink-0 self-start sticky top-6">
          <LeadPanel
            providerName={provider.business_name}
            providerSlug={provider.slug}
            categorySlug={provider.category_slug}
            citySlug={provider.city_slug}
            services={provider.services}
            verificationLevel={provider.verification_level}
            reviewCount={provider.review_count}
            jobsCompleted={provider.jobs_completed}
            cityLeads={provider.city_leads}
            cityName={provider.city_name}
            categoryName={provider.category_name}
            latestReview={provider.latest_review}
            latestLeadClientName={provider.latest_lead_client_name}
            latestLeadCity={provider.latest_lead_city}
            leadsReceived={provider.leads_received}
            translations={translations}
            lang={lang}
            selectedService={selectedService}
            onServiceSelect={handleServiceSelect}
            onServiceDeselect={handleServiceDeselect}
            onServicePreFill={handleServicePreFill}
            onNotesPreFill={handleNotesPreFill}
          />
        </div>
      </div>

      <StickyProviderCTA lang={lang} translations={translations} providerName={provider.business_name} onOpenSheet={() => setIsSheetOpen(true)} />

      <BottomSheetForm
        providerName={provider.business_name}
        providerSlug={provider.slug}
        categorySlug={provider.category_slug}
        citySlug={provider.city_slug}
        services={provider.services}
        verificationLevel={provider.verification_level}
        reviewCount={provider.review_count}
        jobsCompleted={provider.jobs_completed}
        cityLeads={provider.city_leads}
        cityName={provider.city_name}
        categoryName={provider.category_name}
        latestReview={provider.latest_review}
        latestLeadClientName={provider.latest_lead_client_name}
        latestLeadCity={provider.latest_lead_city}
        leadsReceived={provider.leads_received}
        translations={translations}
        lang={lang}
        selectedService={selectedService}
        onServiceSelect={handleServiceSelect}
        onServiceDeselect={handleServiceDeselect}
        onServicePreFill={handleServicePreFill}
        onNotesPreFill={handleNotesPreFill}
        isOpen={isSheetOpen}
        onClose={() => setIsSheetOpen(false)}
      />
    </div>
  );
}
