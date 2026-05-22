'use client';

import { useState } from 'react';

interface LeadPanelProps {
  providerName: string;
  services: Array<{ id: number; title: string }>;
  verificationLevel: number;
  reviewCount: number;
  jobsCompleted: number;
  cityLeads?: number;
  cityName?: string;
  categoryName?: string;
  latestReview?: { rating: number; comment: string | null; client_name: string } | null;
  latestLeadClientName?: string | null;
  latestLeadCity?: string | null;
  leadsReceived?: number;
  translations: Record<string, string>;
  lang: string;
}

export default function LeadPanel({
  providerName,
  services,
  verificationLevel,
  reviewCount,
  jobsCompleted,
  cityLeads,
  cityName,
  categoryName,
  latestReview,
  latestLeadClientName,
  latestLeadCity,
  leadsReceived,
  translations,
  lang,
}: LeadPanelProps) {
  const t = translations;
  const [selectedService, setSelectedService] = useState<number | null>(null);

  // Social proof signal cascade logic
  const getSocialProofSignal = () => {
    // 1. reviewCount > 0 && latestReview
    if (reviewCount > 0 && latestReview) {
      const shortComment = latestReview.comment
        ? latestReview.comment.slice(0, 80) + (latestReview.comment.length > 80 ? '...' : '')
        : '';
      const initials = latestReview.client_name.split(' ').map(n => n[0]).join('.');
      return (
        <div className="flex items-start gap-2">
          <span className="text-yellow-400">★★★★★</span>
          <div>
            <p className="text-gray-700">"{shortComment}"</p>
            <p className="text-gray-500 text-xs mt-1">— {initials}</p>
          </div>
        </div>
      );
    }
    // 2. reviewCount === 0 && jobsCompleted > 0
    if (reviewCount === 0 && jobsCompleted > 0) {
      return <p>✓ {jobsCompleted} завършени услуги</p>;
    }
    // 3. reviewCount === 0 && jobsCompleted === 0 && cityLeads > 0
    if (reviewCount === 0 && jobsCompleted === 0 && cityLeads && cityLeads > 0) {
      return <p>{cityLeads} заявки за {categoryName} в {cityName} тази година</p>;
    }
    // 4. leadsReceived > 0 && latestLeadClientName
    if (leadsReceived && leadsReceived > 0 && latestLeadClientName) {
      return <p>{latestLeadClientName} от {latestLeadCity} поръча наскоро</p>;
    }
    // 5. Fallback
    return <p>✓ Безплатна заявка • Без ангажимент • Директен контакт</p>;
  };

  return (
    <div className="rounded-xl border border-gray-100 bg-white shadow-sm overflow-hidden max-h-[calc(100vh-48px)] overflow-y-auto">
      {/* 1. Header */}
      <div className="px-5 py-4 border-b border-gray-100">
        <h2 className="text-sm font-semibold text-gray-900">
          {t['request_panel_title'] ?? 'Изпратете заявка на'} {providerName}
        </h2>
        <p className="text-xs text-gray-400 mt-0.5">
          ✓ {t['request_panel_free'] ?? 'Безплатно'} • {t['request_panel_no_commitment'] ?? 'Без ангажимент'}
        </p>
      </div>

      {/* 2. Panel Body */}
      <div className="px-5 py-4 flex flex-col gap-3">
        {/* ServiceChips */}
        {(services ?? []).length > 0 && (
          <div>
            <div className="flex flex-wrap gap-2 mb-2">
              {(services ?? []).map((service) => (
                <button
                  key={service.id}
                  onClick={() => setSelectedService(service.id)}
                  className={`text-xs px-3 py-1.5 border rounded-full cursor-pointer transition-colors ${
                    selectedService === service.id
                      ? 'bg-orange-500 text-white border-orange-500'
                      : 'border-gray-200 text-gray-600 bg-white hover:border-orange-400 hover:text-orange-600'
                  }`}
                >
                  {service.title}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500">
              {t['or_general_request'] ?? 'Или изпратете обща заявка ↓'}
            </p>
          </div>
        )}

        {/* PhoneField */}
        <input
          type="tel"
          placeholder={t['phone_placeholder'] ?? 'Вашият телефон'}
          className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm bg-white text-gray-900 outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-400/20"
        />

        {/* NotesField */}
        <textarea
          rows={3}
          placeholder={t['notes_placeholder'] ?? 'Опишете накратко какво ви трябва...'}
          className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm bg-white text-gray-900 outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-400/20 resize-none"
        />

        {/* SocialProofSignal */}
        <div className="bg-gray-50 rounded-xl p-3 text-xs text-gray-600">
          {getSocialProofSignal()}
        </div>

        {/* CTAButton */}
        <button className="w-full py-3.5 bg-orange-500 hover:bg-orange-600 text-white text-base font-semibold rounded-xl transition-colors">
          {t['cta_button'] ?? 'Заявете услуга'}
        </button>
      </div>

      {/* TrustRow */}
      <div className="grid grid-cols-3 border-t border-gray-100">
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400">
          <span>✓ {t['trust_verified'] ?? 'Верифициран'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {t['trust_free'] ?? 'Без такса'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {t['trust_direct'] ?? 'Директен контакт'}</span>
        </div>
      </div>
    </div>
  );
}
