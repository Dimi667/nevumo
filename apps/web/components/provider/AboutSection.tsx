'use client';

import { useState } from 'react';

interface AboutSectionProps {
  description: string | null;
  translations: Record<string, string>;
}

export default function AboutSection({ description, translations }: AboutSectionProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const t = translations;

  if (!description || description.trim() === '') {
    return null;
  }

  const shouldTruncate = description.length > 300;
  const displayText = shouldTruncate && !isExpanded 
    ? description.slice(0, 300) + '...' 
    : description;

  return (
    <section>
      <h2 className="text-xl font-bold text-gray-900 mb-4">
        {t['provider_page.section_about'] ?? 'За специалиста'}
      </h2>
      <p className="text-gray-700 leading-relaxed">
        {displayText}
      </p>
      {shouldTruncate && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-2 text-orange-600 hover:text-orange-700 font-medium text-sm"
        >
          {isExpanded 
            ? (t['provider_page.read_less'] ?? 'Покажи по-малко')
            : (t['provider_page.read_more'] ?? 'Прочети повече')
          }
        </button>
      )}
    </section>
  );
}
