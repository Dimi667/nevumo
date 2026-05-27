'use client';

import { useState } from 'react';

interface LegalModalProps {
  isOpen: boolean;
  onClose: () => void;
  lang: string;
  type: 'terms' | 'terms-provider' | 'privacy' | 'cookies' | 'withdrawal' | 'contact-dsa';
  authDict: Record<string, string>;
  docDict: Record<string, string>;
}

export default function LegalModal({ isOpen, onClose, lang, type, authDict, docDict }: LegalModalProps) {

  if (!isOpen) return null;

  const getTitle = () => {
    // Use page_title from document namespace (s1_title for cookies)
    if (type === 'cookies') {
      return docDict['s1_title'] || docDict['page_title'] || 'Cookie Policy';
    }
    return docDict['page_title'] || getTitleFallback();
  };

  const getTitleFallback = () => {
    switch (type) {
      case 'terms':
        return 'Terms of Service';
      case 'terms-provider':
        return 'Provider Terms of Service';
      case 'privacy':
        return 'Privacy Policy';
      case 'cookies':
        return 'Cookie Policy';
      case 'withdrawal':
        return 'Withdrawal Form';
      case 'contact-dsa':
        return 'DSA Contact Point';
      default:
        return '';
    }
  };

  return (
    <>
      {/* Modal Overlay */}
      <div
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[85vh] flex flex-col pointer-events-auto">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">
              {getTitle()}
            </h2>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Close"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          {/* Body */}
          <div className="overflow-y-auto flex-1 p-6">
            <iframe
              src={type === 'terms'
                ? `/${lang}/terms?modal=true`
                : type === 'terms-provider'
                ? `/${lang}/terms-provider?modal=true`
                : type === 'privacy'
                ? `/${lang}/privacy?modal=true`
                : type === 'cookies'
                ? `/${lang}/cookies?modal=true`
                : type === 'withdrawal'
                ? `/${lang}/withdrawal?modal=true`
                : `/${lang}/contact-dsa?modal=true`}
              width="100%"
              height="100%"
              style={{ border: 'none', minHeight: '60vh' }}
            />
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl">
            <button
              onClick={onClose}
              className="w-full px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {authDict['dismiss_button'] || 'Got it'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
