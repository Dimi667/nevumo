'use client';

import Link from 'next/link';

interface FooterProps {
  lang: string;
  citySlug: string;
  footerTitle: string;
  footerLinkCleaning: string;
  footerLinkPlumbing: string;
  footerLinkMassage: string;
  footerPopular: string;
}

export default function Footer({ 
  lang, 
  citySlug, 
  footerTitle,
  footerLinkCleaning,
  footerLinkPlumbing,
  footerLinkMassage,
  footerPopular,
}: FooterProps) {
  return (
    <footer className="py-12 px-6 bg-gray-50 border-t border-gray-200">
      <div className="max-w-4xl mx-auto text-center">
        <p className="mb-6 text-gray-700">{footerTitle}</p>
        <div className="flex flex-wrap justify-center gap-4 mb-6 text-sm">
          <Link href={`/${lang}/${citySlug}/cleaning`} className="text-gray-700 transition-colors">
            {footerLinkCleaning}
          </Link>
          <span className="text-gray-500">|</span>
          <Link href={`/${lang}/${citySlug}/plumbing`} className="text-gray-700 transition-colors">
            {footerLinkPlumbing}
          </Link>
          <span className="text-gray-500">|</span>
          <Link href={`/${lang}/${citySlug}/massage`} className="text-gray-700 transition-colors">
            {footerLinkMassage}
          </Link>
        </div>
        <p className="text-gray-500 text-sm">
          {footerPopular}
        </p>
      </div>
    </footer>
  );
}
