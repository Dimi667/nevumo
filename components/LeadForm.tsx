'use client';
import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { themes } from "@repo/ui";

interface ProviderInfo {
  name: string;
  category: string;
  category_key: string;
  job_title: string;
  job_title_key: string;
  rating: number;
  jobs_completed: number;
  is_verified: boolean;
  profile_image_url?: string | null;
}

interface Props {
  initialProvider: ProviderInfo;
  initialT: Record<string, string>;
  currentLang: string;
}

export default function LeadWidget({ initialProvider, initialT, currentLang }: Props) {
  const [provider] = useState(initialProvider);
  const [t, setT] = useState(initialT);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [mounted, setMounted] = useState(false);

  const fontStyle = { fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' };
  const inputStyle = { width: '100%', padding: '1rem', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1.1rem', boxSizing: 'border-box' as const, backgroundColor: '#ffffff', color: '#333' };
  const labelStyle = { fontSize: '0.9rem', fontWeight: '700', marginBottom: '0.4rem', color: '#444', display: 'block' };

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/translations/${currentLang}`)
      .then(res => res.json())
      .then(data => setT(data));
  }, [currentLang]);

  useEffect(() => {
    setMounted(true);

    const updateIsMobile = () => {
      const ua = navigator.userAgent;
      const isMobileUA = /Mobile|iPhone|iPad|iPod|Android|BlackBerry|IEMobile|Opera Mini/i.test(ua);
      setIsMobile(window.innerWidth < 769 || isMobileUA);
    };

    updateIsMobile();

    // Delay to allow viewport meta to apply in dev tools
    setTimeout(updateIsMobile, 100);

    window.addEventListener('resize', updateIsMobile);
    return () => window.removeEventListener('resize', updateIsMobile);
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.currentTarget);
    try {
      const response = await fetch('http://127.0.0.1:8000/leads/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          client_name: "Client", 
          phone: formData.get('phone'), 
          notes: formData.get('notes'), 
          service_type: "Lead Capture Widget" 
        }),
      });
      if (response.ok) setSubmitted(true);
      else alert(t?.errGeneral || 'Error');
    } catch { alert(t?.errGeneral || 'Error'); } finally { setLoading(false); }
  };

  return (
    <div style={{ ...fontStyle, backgroundColor: '#f9f9f9', minHeight: '100dvh', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingBottom: '100px', width: '100%', overflowX: 'hidden' }}>
      <main style={{ padding: '2.5rem 2rem', maxWidth: '440px', width: '100%', backgroundColor: '#ffffff', borderRadius: '16px', boxShadow: '0 10px 25px rgba(0,0,0,0.05)', border: '1px solid #eee', marginTop: '2rem' }}>
        
        {submitted ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <h2 style={{ color: '#27ae60', marginBottom: '1rem', fontSize: '1.5rem' }}>{t.success_title}</h2>
            <p style={{ marginBottom: '2rem', color: '#555', fontSize: '1.1rem' }}>{t.success_message}</p>
            <button onClick={() => setSubmitted(false)} style={{ width: '100%', padding: '1.1rem', background: themes.fixvell.primary, color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1.2rem', fontWeight: '800' }}>
              {t.new_request_button}
            </button>
          </div>
        ) : (
          <>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <img src="/Nevumo_logo.svg" alt="Nevumo" style={{ height: '50px', margin: '0 auto' }} />
              {provider.profile_image_url && <img src={provider.profile_image_url} alt={provider.name} style={{ width: '120px', height: '120px', borderRadius: '50%', objectFit: 'cover', margin: '1.5rem auto 0.5rem auto', border: '4px solid #ffffff', boxShadow: '0 4px 10px rgba(0,0,0,0.1)' }} />}
              <h1 style={{ color: '#333', fontSize: '1.25rem', fontWeight: '700', marginTop: '15px', marginBottom: '0' }}>{provider.name}</h1>
              <p style={{ color: '#666', fontSize: '0.85rem', marginTop: '0', marginBottom: '0' }}>{provider.job_title}</p>
              
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', fontSize: '0.95rem', color: '#444', marginTop: '10px', fontWeight: '600' }}>
                <span>⭐ {provider.rating} {t.rating_label}</span> • <span>{provider.jobs_completed} {t.jobs_label}</span>
              </div>
              
              {provider.is_verified && (
                <p style={{ color: '#27ae60', fontSize: '0.85rem', fontWeight: 'bold', marginTop: '2px', marginBottom: '0' }}>
                  {t.verified_label}
                </p>
              )}
            </div>

            <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#333', marginBottom: '0.5rem' }}>{t.button_text}</h2>
            </div>

            <form id="lead-form" onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
              <div>
                <label style={labelStyle}>{t.phone_label}</label>
                <input name="phone" type="tel" required placeholder={t.phone_placeholder} style={inputStyle} />
              </div>
              <div>
                <label style={labelStyle}>{t.notes_label}</label>
                <textarea name="notes" placeholder={t.notes_placeholder} style={{ ...inputStyle, height: '110px', resize: 'none' }} />
              </div>
              
              <p style={{ fontSize: '0.85rem', color: '#666', textAlign: 'center', fontStyle: 'italic', margin: '0' }}>{t.response_time}</p>
              
              {!isMobile && (
                <button 
                  disabled={loading} 
                  type="submit" 
                  className="desktop-only-button"
                  style={{ padding: '1.1rem', background: themes.fixvell.primary, color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1.2rem', fontWeight: '800' }}
                >
                  {loading ? '...' : t.button_text}
                </button>
              )}
              
              <p style={{ fontSize: '0.8rem', color: '#999', textAlign: 'center', marginTop: '0.5rem' }}>
                {t.disclaimer}
              </p>
            </form>
          </>
        )}
      </main>

      {mounted && isMobile && !submitted && createPortal(
        <div style={{
          position: 'fixed',
          inset: 'auto 0 0 0',
          bottom: 'env(safe-area-inset-bottom, 0)',
          left: 0,
          right: 0,
          backgroundColor: '#ffffff',
          padding: '1rem',
          paddingBottom: 'calc(1rem + env(safe-area-inset-bottom))',
          boxShadow: '0 -4px 10px rgba(0,0,0,0.1)',
          display: 'flex',
          justifyContent: 'center',
          zIndex: 10000,
          transform: 'translateZ(0)',
          WebkitTransform: 'translateZ(0)',
          willChange: 'transform',
        }}>
          <button 
            onClick={() => (document.getElementById('lead-form') as HTMLFormElement | null)?.requestSubmit()}
            disabled={loading}
            style={{ 
              width: '100%', 
              maxWidth: '400px', 
              padding: '1.1rem', 
              background: themes.fixvell.primary, 
              color: 'white', 
              border: 'none', 
              borderRadius: '8px', 
              fontSize: '1.2rem', 
              fontWeight: '800',
              cursor: 'pointer'
            }}
          >
            {loading ? '...' : t.button_text}
          </button>
        </div>,
        document.body
      )}

      <style jsx>{`
        @media (max-width: 768px) { .desktop-only-button { display: none !important; } }
        * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
      `}</style>
    </div>
  );
}