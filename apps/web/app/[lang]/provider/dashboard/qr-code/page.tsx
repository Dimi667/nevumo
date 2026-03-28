'use client';

import { useState } from 'react';
import { getEnhancedQRCode, downloadEnhancedQRSVG } from '@/lib/provider-api';

interface QRData {
  public_url: string;
  canonical_url: string;
  qr_code: string;
}

interface EnhancedQRData extends QRData {
  language: string;
  business_name: string;
  service_name: string;
}

const SUPPORTED_LANGUAGES = [
  { code: 'bg', name: 'Български' },
  { code: 'en', name: 'English' },
  { code: 'de', name: 'Deutsch' },
  { code: 'fr', name: 'Français' },
  { code: 'es', name: 'Español' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Português' },
  { code: 'sv', name: 'Svenska' },
  { code: 'no', name: 'Norsk' },
  { code: 'da', name: 'Dansk' },
  { code: 'fi', name: 'Suomi' },
  { code: 'et', name: 'Eesti' },
  { code: 'lt', name: 'Lietuvių' },
  { code: 'lv', name: 'Latviešu' },
  { code: 'cs', name: 'Čeština' },
  { code: 'sk', name: 'Slovenčina' },
  { code: 'pl', name: 'Polski' },
  { code: 'hu', name: 'Magyar' },
  { code: 'ro', name: 'Română' },
  { code: 'hr', name: 'Hrvatski' },
  { code: 'sl', name: 'Slovenščina' },
  { code: 'sr', name: 'Српски' },
  { code: 'mk', name: 'Македонски' },
  { code: 'el', name: 'Ελληνικά' },
  { code: 'tr', name: 'Türkçe' },
  { code: 'sq', name: 'Shqip' },
  { code: 'ga', name: 'Gaeilge' },
  { code: 'mt', name: 'Malti' },
  { code: 'nl', name: 'Nederlands' },
];

export default function QRCodePage() {
  const [enhancedQr, setEnhancedQr] = useState<EnhancedQRData | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState('bg');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    try {
      const data = await getEnhancedQRCode(selectedLanguage);
      setEnhancedQr(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to generate QR code');
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload() {
    if (!enhancedQr) return;
    try {
      await downloadEnhancedQRSVG(selectedLanguage, `nevumo-qr-${selectedLanguage}.svg`);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to download QR code');
    }
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-gray-900">QR Code</h1>
        <p className="text-sm text-gray-500 mt-0.5">Share your provider profile with a QR code</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
        {/* Language Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            QR Code Language
          </label>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-sm"
          >
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            The QR code text and slogan will be displayed in this language
          </p>
        </div>

        <p className="text-sm text-gray-600">
          Share this QR code on your business cards, flyers, or at your location.
          Clients scan it to reach your profile directly.
          Enhanced QR codes include your business name and a call-to-action slogan.
        </p>

        {!enhancedQr ? (
          <div className="space-y-3">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-5 py-2.5 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-xl transition-colors"
            >
              {loading ? 'Generating…' : 'Generate QR Code'}
            </button>
            {error && <p className="text-xs text-red-600">{error}</p>}
          </div>
        ) : (
          <div className="space-y-5">
            {/* QR image */}
            <div className="flex justify-center">
              <div className="p-4 bg-white border border-gray-200 rounded-xl inline-block">
                <img
                  src={enhancedQr.qr_code}
                  alt="QR Code"
                  className="w-56 h-auto"
                />
              </div>
            </div>

            {/* Enhanced QR Info */}
            <div className="bg-orange-50 rounded-lg px-4 py-3">
              <p className="text-xs text-orange-600 font-medium mb-1">Enhanced QR Code</p>
              <p className="text-sm text-gray-700">
                <span className="font-medium">Business:</span> {enhancedQr.business_name}<br/>
                <span className="font-medium">Service:</span> {enhancedQr.service_name}<br/>
                <span className="font-medium">Language:</span> {SUPPORTED_LANGUAGES.find(l => l.code === enhancedQr.language)?.name}
              </p>
            </div>

            {/* URL */}
            <div className="bg-gray-50 rounded-lg px-4 py-3">
              <p className="text-xs text-gray-500 mb-1">Your QR URL</p>
              <a
                href={enhancedQr.public_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-orange-500 hover:underline break-all font-medium"
              >
                {enhancedQr.public_url}
              </a>
            </div>
            <div className="bg-gray-50 rounded-lg px-4 py-3">
              <p className="text-xs text-gray-500 mb-1">Canonical profile URL</p>
              <a
                href={enhancedQr.canonical_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-orange-500 hover:underline break-all font-medium"
              >
                {enhancedQr.canonical_url}
              </a>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-3">
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download
              </button>
              <button
                onClick={() => setEnhancedQr(null)}
                className="px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 text-sm font-medium rounded-lg transition-colors"
              >
                Regenerate
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
