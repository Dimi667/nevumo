'use client';

import { useState } from 'react';
import LeadForm from '@/components/category/LeadForm';

interface CityLeadSectionProps {
  translations: Record<string, string>;
  categoryTranslations: Record<string, string>;
  categories: { id: number; slug: string; name: string }[];
  citySlug: string;
  lang: string;
  countryCode?: string;
}

export default function CityLeadSection({
  translations,
  categoryTranslations,
  categories,
  citySlug,
  lang,
  countryCode,
}: CityLeadSectionProps) {
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

  const handleChipClick = (slug: string) => {
    setSelectedSlug(slug);
  };

  return (
    <div id="lead-form" className="bg-white py-12 px-6">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          {translations['what_need_label'] || 'What service do you need?'}
        </h2>
        
        <div className="flex flex-wrap gap-2 mb-6">
          {categories.map((category) => (
            <button
              key={category.id}
              type="button"
              onClick={() => handleChipClick(category.slug)}
              className={`px-3 py-2 rounded-full text-sm transition-colors ${
                selectedSlug === category.slug
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {selectedSlug && (
          <div className="transition-opacity duration-300 opacity-100">
            <LeadForm
              translations={categoryTranslations}
              categorySlug={selectedSlug}
              citySlug={citySlug}
              lang={lang}
              countryCode={countryCode}
            />
          </div>
        )}
      </div>
    </div>
  );
}
