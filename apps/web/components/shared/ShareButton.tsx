'use client';

import React, { useState } from 'react';

interface ShareButtonProps {
  title: string;
  text?: string;
  linkCopiedLabel: string;
  label: string;
  className?: string;
}

export const ShareButton: React.FC<ShareButtonProps> = ({
  title,
  text,
  linkCopiedLabel,
  label,
  className = '',
}) => {
  const [showToast, setShowToast] = useState(false);

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title,
          text,
          url: window.location.href,
        });
      } catch (error) {
        // User cancelled share - ignore
      }
    } else {
      // Desktop / no Web Share API: copy URL to clipboard
      const url = window.location.href;
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(url);
          setShowToast(true);
          setTimeout(() => setShowToast(false), 2000);
        } catch (error) {
          console.error('Failed to copy URL:', error);
        }
      } else {
        // Fallback for HTTP / non-secure context (e.g. local network)
        const textArea = document.createElement('textarea');
        textArea.value = url;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        textArea.style.top = '-9999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
          document.execCommand('copy');
          setShowToast(true);
          setTimeout(() => setShowToast(false), 2000);
        } catch (error) {
          console.error('Failed to copy URL:', error);
        }
        document.body.removeChild(textArea);
      }
    }
  };

  return (
    <div className="relative inline-block">
      {showToast && (
        <div
          className="absolute -top-10 left-1/2 -translate-x-1/2 bg-green-500 text-white text-xs px-2 py-1 rounded transition-opacity duration-300"
          style={{ opacity: showToast ? 1 : 0 }}
        >
          {linkCopiedLabel}
        </div>
      )}
      <button
        onClick={handleShare}
        className={`inline-flex items-center gap-2 ${className}`}
        type="button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
          <polyline points="16 6 12 2 8 6" />
          <line x1="12" y1="2" x2="12" y2="15" />
        </svg>
        <span>{label}</span>
      </button>
    </div>
  );
};
