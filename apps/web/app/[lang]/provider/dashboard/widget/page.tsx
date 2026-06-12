'use client';

import { useState, useEffect, useRef } from 'react';
import { Copy, Check } from 'lucide-react';
import { getEnhancedQRCode } from '@/lib/provider-api';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';

interface QRData {
  public_url: string;
  canonical_url: string;
  qr_code: string;
}

export default function WidgetPage() {
  const { t, lang } = useDashboardI18n();

  const [qrData, setQrData] = useState<QRData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [iframeWidth, setIframeWidth] = useState(360);
  const [copied, setCopied] = useState(false);
  const [bioCopied, setBioCopied] = useState(false);
  const [tiktokCopied, setTiktokCopied] = useState(false);

  const previewContainerRef = useRef<HTMLDivElement>(null);
  const [previewScale, setPreviewScale] = useState<number>(1);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);
      try {
        const data = await getEnhancedQRCode(lang);
        setQrData({
          public_url: data.public_url,
          canonical_url: data.canonical_url,
          qr_code: data.qr_code,
        });
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : t('msg_failed_load_widget'));
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [t, lang]);

  useEffect(() => {
    const calcScale = () => {
      if (!previewContainerRef.current) return;
      const padding = 32; // 16px each side
      const available = previewContainerRef.current.offsetWidth - padding;
      setPreviewScale(Math.min(1, available / iframeWidth));
    };

    calcScale();

    const observer = new ResizeObserver(calcScale);
    if (previewContainerRef.current) observer.observe(previewContainerRef.current);

    return () => observer.disconnect();
  }, [iframeWidth]);

  // Extract relative path from absolute URL for local network compatibility
  const getRelativeUrl = (url: string): string => {
    try {
      const urlObj = new URL(url);
      return urlObj.pathname + urlObj.search;
    } catch {
      return url;
    }
  };

  const relativeUrl = qrData ? getRelativeUrl(qrData.public_url) : '';
  
  // For embed code, use current origin to work across domains
  const embedCode = qrData
    ? `<iframe src="${typeof window !== 'undefined' ? window.location.origin : ''}${relativeUrl}" width="${iframeWidth}" height="600" style="border:none;border-radius:12px;" title="Nevumo Widget"></iframe>`
    : '';

  async function handleCopy() {
    if (!embedCode) return;
    try {
      await navigator.clipboard.writeText(embedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error('Failed to copy:', e);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6 max-w-2xl">
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t('widget_title')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t('widget_subtitle')}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !qrData) {
    return (
      <div className="space-y-6 max-w-2xl">
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t('widget_title')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t('widget_subtitle')}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-sm text-red-600">{error || t('msg_no_widget_data')}</p>
        </div>
      </div>
    );
  }

  const publicUrl = qrData.public_url;
  const shareUrl = qrData.canonical_url;

  return (
    <div className="space-y-6 max-w-2xl">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-gray-900">{t('widget_title')}</h1>
        <p className="text-sm text-gray-500 mt-0.5">{t('widget_subtitle')}</p>
      </div>

      {/* Size Selector */}
      <div className="flex gap-3">
        <button
          onClick={() => setIframeWidth(360)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            iframeWidth === 360
              ? 'bg-orange-500 text-white'
              : 'border border-gray-300 text-gray-600 hover:border-orange-400'
          }`}
        >
          {t('widget_size_standard')}
        </button>
        <button
          onClick={() => setIframeWidth(480)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            iframeWidth === 480
              ? 'bg-orange-500 text-white'
              : 'border border-gray-300 text-gray-600 hover:border-orange-400'
          }`}
        >
          {t('widget_size_wide')}
        </button>
      </div>

      {/* Live Preview */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">{t('widget_preview_title')}</h2>
        <div
          ref={previewContainerRef}
          className="bg-gray-50 rounded-xl p-4 flex justify-center w-full"
        >
          <div
            style={{
              width: Math.round(iframeWidth * previewScale),
              height: Math.round(600 * previewScale),
              overflow: 'hidden',
              borderRadius: '12px',
              boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
              position: 'relative',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: iframeWidth,
                height: 600,
                transform: `scale(${previewScale})`,
                transformOrigin: 'top left',
              }}
            >
              <iframe
                src={relativeUrl}
                width={iframeWidth}
                height={600}
                style={{ border: 'none', display: 'block' }}
                title={t('widget_preview_title')}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Embed Code */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-semibold text-gray-900">{t('widget_code_title')}</h2>
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {copied ? (
              <>
                <Check size={16} />
                {t('widget_code_copied')}
              </>
            ) : (
              <>
                <Copy size={16} />
                {t('widget_code_copy')}
              </>
            )}
          </button>
        </div>
        <textarea
          readOnly
          rows={4}
          value={embedCode}
          className="w-full font-mono text-sm bg-gray-50 border border-gray-200 rounded-lg p-3 resize-none"
        />
      </div>

      {/* How It Works */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('widget_how_title')}</h2>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 flex flex-col items-center text-center">
            <div className="w-10 h-10 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-lg mb-3">
              1
            </div>
            <p className="text-sm text-gray-600">{t('widget_how_step1')}</p>
          </div>
          <div className="flex-1 flex flex-col items-center text-center">
            <div className="w-10 h-10 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-lg mb-3">
              2
            </div>
            <p className="text-sm text-gray-600">{t('widget_how_step2')}</p>
          </div>
          <div className="flex-1 flex flex-col items-center text-center">
            <div className="w-10 h-10 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-lg mb-3">
              3
            </div>
            <p className="text-sm text-gray-600">{t('widget_how_step3')}</p>
          </div>
        </div>
      </div>

      {/* Add the widget to your website */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('widget_site_title')}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="font-semibold text-gray-900 mb-2">WordPress</div>
            <p className="text-sm text-gray-600">{t('widget_site_wordpress')}</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="font-semibold text-gray-900 mb-2">Wix</div>
            <p className="text-sm text-gray-600">{t('widget_site_wix')}</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="font-semibold text-gray-900 mb-2">Squarespace</div>
            <p className="text-sm text-gray-600">{t('widget_site_squarespace')}</p>
          </div>
        </div>
      </div>

      {/* Link in bio */}
      <div className="bg-orange-50 border border-orange-100 rounded-xl p-5">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">{t('widget_bio_title')}</h2>
        <p className="text-sm text-gray-600">{t('widget_bio_description')}</p>
      </div>

      {/* Share your public page */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('widget_share_title')}</h2>
        <div className="flex gap-3">
          <button
            onClick={() => window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`, '_blank')}
            className="bg-[#1877F2] text-white rounded-lg px-5 py-2.5 flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
            <span className="text-sm font-medium">{t('widget_share_facebook')}</span>
          </button>
          <button
            onClick={async () => {
              try {
                await navigator.clipboard.writeText(shareUrl);
                setBioCopied(true);
                setTimeout(() => setBioCopied(false), 2000);
              } catch (e) {
                console.error('Failed to copy:', e);
              }
            }}
            className="bg-gradient-to-r from-[#833AB4] via-[#FD1D1D] to-[#F77737] text-white rounded-lg px-5 py-2.5 flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>
            </svg>
            <span className="text-sm font-medium">{bioCopied ? t('widget_code_copied') : t('widget_share_instagram')}</span>
          </button>
          <button
            onClick={async () => {
              try {
                await navigator.clipboard.writeText(shareUrl);
                setTiktokCopied(true);
                setTimeout(() => setTiktokCopied(false), 2000);
              } catch (e) {
                console.error('Failed to copy:', e);
              }
            }}
            className="bg-black text-white rounded-lg px-5 py-2.5 flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V8.69a8.22 8.22 0 0 0 4.79 1.52V6.75a4.85 4.85 0 0 1-1.02-.06z"/>
            </svg>
            <span className="text-sm font-medium">{tiktokCopied ? t('widget_code_copied') : t('widget_share_tiktok')}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
