'use client';

import { useState } from 'react';
import { getQRCode } from '@/lib/provider-api';

interface QRData {
  public_url: string;
  canonical_url: string;
  qr_code: string;
}

export default function QRCodePage() {
  const [qr, setQr] = useState<QRData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    try {
      const data = await getQRCode();
      setQr(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to generate QR code');
    } finally {
      setLoading(false);
    }
  }

  function handleDownload() {
    if (!qr) return;
    const link = document.createElement('a');
    link.href = qr.qr_code;
    link.download = 'nevumo-qr-code.png';
    link.click();
  }

  return (
    <div className="space-y-6 max-w-lg">
      <div>
        <h1 className="text-xl font-bold text-gray-900">QR Code</h1>
        <p className="text-sm text-gray-500 mt-0.5">Share your provider profile with a QR code</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
        <p className="text-sm text-gray-600">
          Share this QR code on your business cards, flyers, or at your location.
          Clients scan it to reach your profile directly.
        </p>

        {!qr ? (
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
                  src={qr.qr_code}
                  alt="QR Code"
                  className="w-48 h-48"
                />
              </div>
            </div>

            {/* URL */}
            <div className="bg-gray-50 rounded-lg px-4 py-3">
              <p className="text-xs text-gray-500 mb-1">Your QR URL</p>
              <a
                href={qr.public_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-orange-500 hover:underline break-all font-medium"
              >
                {qr.public_url}
              </a>
            </div>
            <div className="bg-gray-50 rounded-lg px-4 py-3">
              <p className="text-xs text-gray-500 mb-1">Canonical profile URL</p>
              <a
                href={qr.canonical_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-orange-500 hover:underline break-all font-medium"
              >
                {qr.canonical_url}
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
                onClick={() => setQr(null)}
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
