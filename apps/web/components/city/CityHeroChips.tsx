'use client'

import { useState } from 'react'
import LeadForm from '@/components/category/LeadForm'

interface CityHeroChipsProps {
  categories: { id: number; slug: string; name: string }[]
  categoryTranslations: Record<string, string>
  citySlug: string
  lang: string
  countryCode?: string
}

const categoryIcons: Record<string, React.ReactNode> = {
  cleaning: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
    </svg>
  ),
  plumbing: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
    </svg>
  ),
  massage: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
    </svg>
  ),
};

export default function CityHeroChips({
  categories,
  categoryTranslations,
  citySlug,
  lang,
  countryCode,
}: CityHeroChipsProps) {
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null)

  return (
    <div className="w-full">
      <div id="city-hero-chips" className="flex flex-wrap gap-2 justify-center">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => {
              setSelectedSlug(category.slug)
              setTimeout(() => {
                document.getElementById('city-lead-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
              }, 100)
            }}
            className={`px-5 py-2 rounded-full text-sm font-medium transition ${
              selectedSlug === category.slug
                ? 'bg-white text-orange-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            <span className="flex items-center gap-2">
              {categoryIcons[category.slug] || null}
              {category.name}
            </span>
          </button>
        ))}
      </div>

      {selectedSlug && (
        <div id="city-lead-form" className="mt-6 bg-white rounded-2xl shadow-xl px-6 py-8 max-w-2xl mx-auto text-left">
          <LeadForm
            translations={categoryTranslations}
            categorySlug={selectedSlug}
            citySlug={citySlug}
            lang={lang}
            countryCode={countryCode}
            onReset={() => {
              setSelectedSlug(null);
              setTimeout(() => {
                document.getElementById('city-hero-chips')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }, 100);
            }}
          />
        </div>
      )}
    </div>
  )
}
