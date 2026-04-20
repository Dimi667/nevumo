'use client';

import { use, useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import type { ProviderProfile, UpdateProfileInput, PriceType } from '@/types/provider';
import type { CategoryOut, CityOut } from '@/lib/api';
import { getCategories, getCities } from '@/lib/api';
import {
  ProviderApiError,
  checkSlugAvailability,
  getProviderProfile,
  updateProviderProfile,
  uploadProviderImage,
  createService,
  getProviderDashboard,
} from '@/lib/provider-api';
import SearchInput from '@/components/dashboard/SearchInput';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { getSlugValidationError, sanitizeSlug, slugify } from '@/lib/slug-utils';
import { deriveOnboardingState, getHeroContent, CompactStepIndicator, saveStep1Draft, loadStep1Draft, clearStep1Draft } from '@/lib/onboarding-utils';

// ─── Constants ────────────────────────────────────────────────────────────────

function getPriceTypes(t: (key: string, fallback?: string) => string): { value: PriceType; label: string }[] {
  return [
    { value: 'fixed', label: t('price_type_fixed', 'Fixed price') },
    { value: 'hourly', label: t('price_type_hourly', 'Per hour') },
    { value: 'request', label: t('price_type_request', 'Per request (quote)') },
    { value: 'per_sqm', label: t('price_type_per_sqm', 'Per sq.m.') },
  ];
}

const CURRENCIES = ['EUR', 'USD', 'GBP', 'CHF', 'CZK', 'DKK', 'HUF', 'PLN', 'RON', 'SEK', 'NOK', 'TRY'];
const MAX_SLUG_CHANGES = 1;

// ─── Types ────────────────────────────────────────────────────────────────────

interface Step1Form {
  business_name: string;
  description: string;
  slug: string;
}

interface Step2Form {
  title: string;
  category_slug: string;
  city_ids: string[];  // Changed from city_id: number | null for MultiSelect
  price_type: PriceType;
  base_price: string;
}

interface EditForm {
  business_name: string;
  description: string;
}

// ─── Avatar component ─────────────────────────────────────────────────────────

function AvatarUpload({
  imageUrl,
  uploading,
  onFileChange,
  t,
}: {
  imageUrl: string | null;
  uploading: boolean;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  t: (key: string, fallback?: string) => string;
}) {
  const ref = useRef<HTMLInputElement>(null);
  const [imageError, setImageError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [errorDetails, setErrorDetails] = useState<string>('');
  
  // Reset error when imageUrl changes
  useEffect(() => {
    setImageError(false);
    setRetryCount(0);
    setErrorDetails('');
  }, [imageUrl]);

  const handleImageError = () => {
    console.error('AvatarUpload: Failed to load image', {
      url: imageUrl,
      retryCount,
      timestamp: new Date().toISOString()
    });
    
    if (retryCount < 2) {
      // Retry with cache busting
      setRetryCount(prev => prev + 1);
      setTimeout(() => {
        setImageError(false);
      }, 1000);
    } else {
      setImageError(true);
      
      if (!navigator.onLine) {
        setErrorDetails(t('msg_network_error', 'Network error - check connection'));
      } else {
        setErrorDetails(t('msg_invalid_image_url', 'Failed to load image. Please try again.'));
      }
    }
  };

  const handleImageLoad = () => {
    console.log('AvatarUpload: Image loaded successfully', {
      url: imageUrl,
      retryCount,
      timestamp: new Date().toISOString()
    });
    setImageError(false);
    setRetryCount(0);
    setErrorDetails('');
  };

  const getRetryUrl = () => {
    if (!imageUrl) return undefined;
    
    const separator = imageUrl.includes('?') ? '&' : '?';
    return `${imageUrl}${separator}retry=${retryCount}&t=${Date.now()}`;
  };

  return (
    <div className="flex items-center gap-3">
      <div className="w-14 h-14 rounded-full bg-gray-100 overflow-hidden flex-shrink-0 flex items-center justify-center text-gray-400">
        {imageUrl && !imageError ? (
          <img 
            src={retryCount > 0 ? getRetryUrl() : imageUrl} 
            alt={t('label_profile', 'Profile')} 
            className="w-full h-full object-cover"
            onError={handleImageError}
            onLoad={handleImageLoad}
          />
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        )}
      </div>
      <div>
        <input ref={ref} type="file" accept=".heic,.heif,image/heic,image/heif,image/jpeg,image/png,image/webp" className="hidden" onChange={onFileChange} aria-label="Upload profile photo" />
        <button
          type="button"
          onClick={() => ref.current?.click()}
          disabled={uploading}
          className="px-3 py-1.5 border border-gray-300 text-gray-600 hover:bg-gray-100 text-xs font-medium rounded-lg transition-colors disabled:opacity-50"
        >
          {uploading ? t('msg_uploading', 'Uploading…') : imageUrl ? t('btn_change_photo', 'Change photo') : t('btn_upload_photo', 'Upload photo')}
        </button>
        <p className="text-xs text-gray-400 mt-0.5">{t('msg_supported_image_formats', 'JPG, PNG, WebP, HEIC · max 5 MB')}</p>
        {imageUrl && imageError && (
          <div className="mt-1">
            <p className="text-xs text-red-500">{t('msg_failed_load_image', 'Failed to load image')}</p>
            {errorDetails && (
              <p className="text-xs text-red-400 mt-0.5">{errorDetails}</p>
            )}
            <button
              type="button"
              onClick={() => {
                setRetryCount(0);
                setImageError(false);
                setErrorDetails('');
              }}
              className="text-xs text-orange-600 hover:text-orange-700 mt-0.5"
            >
              {t('btn_try_again', 'Try again')}
            </button>
          </div>
        )}
        {retryCount > 0 && !imageError && (
          <p className="text-xs text-orange-600 mt-0.5">{t('msg_retrying', 'Retrying...')} ({retryCount}/3)</p>
        )}
      </div>
    </div>
  );
}

// ─── Step Indicator ───────────────────────────────────────────────────────────

function StepIndicator({ 
  step, 
  step1Valid, 
  step2Valid, 
  t,
}: {
  step: number;
  step1Valid: boolean;
  step2Valid: boolean;
  t: (key: string, fallback?: string) => string;
}) {
  return (
    <div className="flex items-center gap-6">
      {/* Step 1 - Profile */}
      <div className="flex flex-col items-center">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
          step1Valid ? 'bg-green-500 text-white' : step >= 1 ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-400'
        }`}>
          {step1Valid ? (
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '1'}
        </div>
        <span className={`text-xs font-medium mt-2 ${
          step >= 1 ? 'text-gray-700' : 'text-gray-400'
        }`}>
          {t('label_profile_setup', 'Profile Setup')}
        </span>
      </div>

      {/* Progress Line */}
      <div className={`flex-1 h-0.5 ${
        step1Valid ? 'bg-green-500' : 'bg-gray-200'
      }`} />

      {/* Step 2 - Service */}
      <div className="flex flex-col items-center">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
          step2Valid ? 'bg-green-500 text-white' : step === 2 ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-400'
        }`}>
          {step2Valid ? (
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '2'}
        </div>
        <span className={`text-xs font-medium mt-2 ${
          step === 2 ? 'text-gray-700' : 'text-gray-400'
        }`}>
          {t('label_service', 'Service')}
        </span>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

interface PageProps {
  params: Promise<{ lang: string }>;
}

export default function ProfilePage({ params }: PageProps) {
  const { lang: paramsLang } = use(params);
  const router = useRouter();
  const { t, lang: contextLang } = useDashboardI18n();
  const lang = paramsLang || contextLang;

  // Load state
  const [profile, setProfile] = useState<ProviderProfile | null>(null);
  const [categories, setCategories] = useState<CategoryOut[]>([]);
  const [cities, setCities] = useState<CityOut[]>([]);
  const [isComplete, setIsComplete] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Image
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorDetails, setErrorDetails] = useState<string>('');

  // Wizard
  const [step, setStep] = useState<1 | 2>(1);
  const [step1, setStep1] = useState<Step1Form>({ business_name: '', description: '', slug: '' });
  const [step1Touched, setStep1Touched] = useState<{ business_name?: boolean; description?: boolean; slug?: boolean }>({});
  const [step1SlugManual, setStep1SlugManual] = useState(false);
  const [step1SlugEditing, setStep1SlugEditing] = useState(false);
  const [step1SlugAvailable, setStep1SlugAvailable] = useState<boolean | null>(null);
  const [step1SlugChecking, setStep1SlugChecking] = useState(false);
  const [step1SlugError, setStep1SlugError] = useState<string | null>(null);
  const [step1SlugSuggestions, setStep1SlugSuggestions] = useState<string[]>([]);
  const [step2, setStep2] = useState<Step2Form>({
    title: '',
    category_slug: '',
    city_ids: [],  // Changed from city_id: null
    price_type: 'request',
    base_price: '',
  });
  const [detectedCurrency, setDetectedCurrency] = useState<string>('EUR');
  const [step2Touched, setStep2Touched] = useState<{ title?: boolean; category_slug?: boolean; city_ids?: boolean }>({});
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Edit mode
  const [editForm, setEditForm] = useState<EditForm>({ business_name: '', description: '' });
  const [editSaving, setEditSaving] = useState(false);
  const [editSuccess, setEditSuccess] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);
  const slugCheckRequestRef = useRef(0);

  // Draft persistence
  const [providerId, setProviderId] = useState<string | null>(null);

  // PWA Install Prompt
  const hasShownPWAPromptRef = useRef(false);

  // Helper to persist current Step 1 state
  const persistStep1Draft = useCallback(() => {
    if (!providerId) return;
    saveStep1Draft(providerId, {
      business_name: step1.business_name,
      description: step1.description,
      slug: step1.slug,
      slugManual: step1SlugManual,
      slugEditing: step1SlugEditing,
    });
  }, [providerId, step1.business_name, step1.description, step1.slug, step1SlugManual, step1SlugEditing]);

  // Auto-save draft whenever Step 1 values change
  useEffect(() => {
    if (step === 1 && providerId && step1.business_name.trim()) {
      persistStep1Draft();
    }
  }, [step, providerId, step1, step1SlugManual, step1SlugEditing, persistStep1Draft]);

  useEffect(() => {
    Promise.all([
      getProviderProfile(),
      getCategories(lang),
      getCities('BG', lang),
      getCities('RS', lang),
      getCities('PL', lang),
      getProviderDashboard(),
    ])
      .then(([p, cats, bgCities, rsCities, plCities, dashboard]) => {
        setProfile(p);
        setCategories(cats);
        setCities([...bgCities, ...rsCities, ...plCities]);

        // Pre-select category from localStorage if valid and not already selected
        const categoryParam = localStorage.getItem('nevumo_selected_category');
        if (categoryParam && cats.some(c => c.slug === categoryParam)) {
          setStep2(f => {
            if (f.category_slug === '') {
              return { ...f, category_slug: categoryParam };
            }
            return f;
          });
        }
        setIsComplete(dashboard.profile.is_complete);
        setProviderId(dashboard.profile.id.toString());
        
        const nameIsEmail = !p.business_name || p.business_name.includes('@');
        const hasExistingSlug = Boolean(p.slug && !nameIsEmail);
        const isOnboardingMode = !dashboard.profile.is_complete;
        
        // Check if we should hydrate from draft
        const hasBackendStep1 = !nameIsEmail && p.business_name && p.slug;
        let step1BusinessName = nameIsEmail ? '' : p.business_name;
        let step1Description = p.description ?? '';
        let step1Slug = nameIsEmail ? '' : p.slug;
        let step1Manual = false;
        let step1Editing = hasExistingSlug && !isOnboardingMode;
        
        if (!hasBackendStep1 && isOnboardingMode) {
          // Try to hydrate from draft
          const draft = loadStep1Draft(dashboard.profile.id.toString());
          if (draft) {
            step1BusinessName = draft.business_name;
            step1Description = draft.description;
            step1Slug = draft.slug;
            step1Manual = draft.slugManual;
            step1Editing = draft.slugEditing;
          }
        } else if (hasBackendStep1) {
          // Backend has real data, clear any stale draft
          clearStep1Draft(dashboard.profile.id.toString());
        }
        
        setStep1({
          business_name: step1BusinessName,
          description: step1Description,
          slug: step1Slug,
        });
        setStep1SlugManual(step1Manual);
        setStep1SlugEditing(step1Editing);
        setEditForm({ business_name: step1BusinessName, description: step1Description });
        setImageUrl(p.profile_image_url);
        
        // Check if we should skip to Step 2 (user has profile but no services)
        if (!dashboard.profile.is_complete && 
            dashboard.profile.missing_fields?.includes('service') &&
            p.business_name && !p.business_name.includes('@')) {
          setStep(2);
        }
      })
      .catch((e: Error) => setLoadError(e.message))
      .finally(() => setLoading(false));
  }, [lang]);

  async function runStep1SlugCheck(candidate: string): Promise<boolean> {
    const trimmed = candidate.trim();
    const validationError = getSlugValidationError(trimmed);

    if (!trimmed) {
      setStep1SlugAvailable(null);
      setStep1SlugError(null);
      setStep1SlugSuggestions([]);
      setStep1SlugChecking(false);
      return false;
    }

    if (validationError) {
      setStep1SlugAvailable(false);
      setStep1SlugError(validationError);
      setStep1SlugSuggestions([]);
      setStep1SlugChecking(false);
      return false;
    }

    if (profile && trimmed === profile.slug) {
      setStep1SlugAvailable(true);
      setStep1SlugError(null);
      setStep1SlugSuggestions([]);
      setStep1SlugChecking(false);
      return true;
    }

    const requestId = slugCheckRequestRef.current + 1;
    slugCheckRequestRef.current = requestId;
    setStep1SlugChecking(true);

    try {
      const result = await checkSlugAvailability(trimmed);
      if (slugCheckRequestRef.current !== requestId) {
        return result.available;
      }

      setStep1SlugAvailable(result.available);
      setStep1SlugError(result.error ?? (result.available ? null : t('msg_url_taken', 'This URL is already taken')));
      setStep1SlugSuggestions(result.available ? [] : (result.suggestions ?? []));
      return result.available;
    } catch {
      if (slugCheckRequestRef.current === requestId) {
        setStep1SlugAvailable(null);
        setStep1SlugError(t('msg_failed_check_url', 'Failed to check URL availability'));
        setStep1SlugSuggestions([]);
      }
      return false;
    } finally {
      if (slugCheckRequestRef.current === requestId) {
        setStep1SlugChecking(false);
      }
    }
  }

  useEffect(() => {
    if (step !== 1) {
      return;
    }

    const trimmedSlug = step1.slug.trim();
    if (!trimmedSlug) {
      setStep1SlugAvailable(null);
      setStep1SlugError(null);
      setStep1SlugSuggestions([]);
      setStep1SlugChecking(false);
      return;
    }

    const timeoutId = window.setTimeout(() => {
      void runStep1SlugCheck(trimmedSlug);
    }, 300);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [profile, step, step1.slug]);

  async function handleImageChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Validate file size
    if (file.size > 5 * 1024 * 1024) {
      const error = t('msg_file_size_limit_5mb', 'File size must be less than 5 MB');
      alert(error);
      return;
    }
    
    // Validate file type
    // Some mobile browsers don't send MIME type for HEIC files, so check by extension as fallback
    const fileName = file.name.toLowerCase();
    const fileExtension = fileName.slice(fileName.lastIndexOf('.'));
    const isHeicByExtension = fileExtension === '.heic' || fileExtension === '.heif';
    
    if (!file.type.match(/^image\/(jpeg|png|webp|heic|heif)$/) && !isHeicByExtension) {
      const error = t('msg_file_type_jpg_png_webp_heic', 'File must be JPG, PNG, WebP, or HEIC');
      alert(error);
      return;
    }
    
    setUploading(true);
    setErrorDetails('');
    
    try {
      const result = await uploadProviderImage(file);
      
      // The backend now returns full URLs, so no need for cache busting
      // but we'll add it anyway for extra safety
      const imageUrlWithTimestamp = result.image_url.includes('?') 
        ? `${result.image_url}&t=${Date.now()}`
        : `${result.image_url}?t=${Date.now()}`;
      
      setImageUrl(imageUrlWithTimestamp);
    } catch (error) {
      console.error('AvatarUpload: Upload failed', {
        error,
        timestamp: new Date().toISOString()
      });
      
      let errorMessage = t('msg_failed_upload_image', 'Failed to upload image. Please try again.');
      if (error instanceof Error) {
        if (error.message.includes('413')) {
          errorMessage = t('msg_file_too_large', 'File too large. Maximum size is 5 MB.');
        } else if (error.message.includes('422')) {
          errorMessage = t('msg_invalid_file_format', 'Invalid file format. Use JPG, PNG, WebP, or HEIC.');
        } else if (error.message.includes('401')) {
          errorMessage = t('msg_authentication_error_login_again', 'Authentication error. Please log in again.');
        } else if (error.message.includes('429')) {
          errorMessage = t('msg_too_many_upload_attempts', 'Too many upload attempts. Please wait a moment.');
        }
      }
      
      setErrorDetails(errorMessage);
      alert(errorMessage);
    } finally {
      setUploading(false);
    }
  }

  // Real-time validation for step 1
  const step1SlugChangesRemaining = profile
    ? Math.max(0, MAX_SLUG_CHANGES - profile.slug_change_count)
    : MAX_SLUG_CHANGES;
  const step1Valid = step1.business_name.trim().length >= 2 && !getSlugValidationError(step1.slug.trim());
  const step1FieldValid = {
    business_name: step1.business_name.trim().length >= 2 && step1Touched.business_name,
    slug: step1Touched.slug && step1SlugAvailable === true,
  };
  const step1FieldErrors = {
    business_name: step1Touched.business_name && step1.business_name.trim().length < 2
      ? t('error_business_name_min_chars', 'Business name must be at least 2 characters')
      : undefined,
    slug: step1Touched.slug ? step1SlugError ?? undefined : undefined,
  };

  async function handleStep1Next(e?: React.MouseEvent<HTMLButtonElement>) {
    // Prevent any browser-native validation or event propagation
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    // Mark all fields as touched to show validation errors
    setStep1Touched({ business_name: true, slug: true });
    
    console.log("FRONTEND: Step1 submit started");
    console.log("FRONTEND: Current step1 state:", step1);
    console.log("FRONTEND: Current step1Touched:", step1Touched);
    console.log("FRONTEND: Current profile state:", profile);
    
    const step1Valid = step1.business_name.trim().length >= 2 && !getSlugValidationError(step1.slug.trim());
    console.log("FRONTEND: Step1 validation result:", step1Valid);
    
    if (!step1Valid) return;

    const slugAvailable = await runStep1SlugCheck(step1.slug.trim());
    console.log("FRONTEND: Slug availability check result:", slugAvailable);
    if (!slugAvailable) return;

    setSaving(true);
    setSaveError(null);
    console.log("FRONTEND: Starting API call...");
    
    try {
      const input: UpdateProfileInput = {
        business_name: step1.business_name.trim(),
        description: step1.description.trim() || undefined,
        slug: step1.slug.trim().toLowerCase(), // Уверяваме се, че е малки букви
        is_onboarding_setup: true,
      };
      console.log("FRONTEND: Sending onboarding update request:", input);
      
      const updated = await updateProviderProfile(input);
      console.log("FRONTEND: Received onboarding response:", updated);
      
      setProfile(updated);
      console.log("FRONTEND: Profile state updated");
      
      // Reset step1 state to prevent stale issues
      const newStep1 = {
        business_name: updated.business_name || '',
        description: updated.description || '',
        slug: updated.slug || '',
      };
      console.log("FRONTEND: Resetting step1 state to:", newStep1);
      setStep1(newStep1);
      
      // Clear draft on successful submission (backend is now source of truth)
      if (providerId) {
        clearStep1Draft(providerId);
      }
      
      console.log("FRONTEND: Setting step to 2");
      setStep(2);
      console.log("FRONTEND: Step1 submit completed successfully");
    } catch (e: unknown) {
      console.error("FRONTEND: ERROR: Onboarding update failed:", e);
      console.error("FRONTEND: ERROR: Type:", typeof e);
      console.error("FRONTEND: ERROR: Constructor:", e?.constructor?.name);
      
      if (e instanceof ProviderApiError && e.code === 'SLUG_TAKEN') {
        const data = (e.data ?? {}) as { suggestions?: string[] };
        setStep1SlugAvailable(false);
        setStep1SlugError(e.message);
        setStep1SlugSuggestions(Array.isArray(data.suggestions) ? data.suggestions : []);
        return;
      }
      if (e instanceof ProviderApiError && e.code === 'INVALID_SLUG') {
        setStep1SlugAvailable(false);
        setStep1SlugError(e.message);
        setStep1SlugSuggestions([]);
        return;
      }
      setSaveError(e instanceof Error ? e.message : t('msg_failed_save_profile', 'Failed to save profile'));
    } finally {
      console.log("FRONTEND: Finally block - setting saving to false");
      setSaving(false);
    }
  }

  // Real-time validation for step 2
  const step2Valid = step2.title.trim().length > 0 && step2.category_slug !== '' && step2.city_ids.length > 0;
  const step2FieldValid = {
    title: step2.title.trim().length > 0 && step2Touched.title,
    category_slug: step2.category_slug !== '' && step2Touched.category_slug,
    city_ids: step2.city_ids.length > 0 && step2Touched.city_ids
  };
  const step2FieldErrors = {
    title: step2Touched.title && !step2.title.trim() ? t('error_title_required', 'Title is required') : undefined,
    category_slug: step2Touched.category_slug && !step2.category_slug ? t('error_category_required', 'Category is required') : undefined,
    city_ids: step2Touched.city_ids && step2.city_ids.length === 0 ? t('error_city_required', 'At least one city is required') : undefined
  };

  // ─── Step 2 submit ──────────────────────────────────────────────────────────

  async function handleCompleteSetup() {
    // Mark all fields as touched to show validation errors
    setStep2Touched({ title: true, category_slug: true, city_ids: true });
    
    if (!step2Valid) return;

    const category = categories.find(c => c.slug === step2.category_slug);
    if (!category || step2.city_ids.length === 0) return;

    setSaving(true);
    setSaveError(null);
    try {
      const serviceData: any = {
        title: step2.title.trim(),
        category_id: category.id,
        city_ids: step2.city_ids.map(Number),
        price_type: step2.price_type,
      };
      
      // Only include base_price and currency if price_type is not "request"
      if (step2.price_type !== 'request') {
        serviceData.base_price = step2.base_price ? Number(step2.base_price) : undefined;
        serviceData.currency = detectedCurrency;
      }

      await createService(serviceData);
      setSaveSuccess(true);

      // Clear draft on complete onboarding
      if (providerId) {
        clearStep1Draft(providerId);
      }

      // Clear selected category from localStorage
      localStorage.removeItem('nevumo_selected_category');

      // Show PWA install prompt after onboarding complete (only once per session)
      if (!hasShownPWAPromptRef.current) {
        hasShownPWAPromptRef.current = true;
        window.dispatchEvent(new CustomEvent('nevumo:onboarding_complete'));
      }

      // Force refresh of layout state by triggering custom event
      window.dispatchEvent(new CustomEvent('force-onboarding-refresh'));

      // Navigate to dashboard which will trigger layout refresh
      setTimeout(() => {
        router.push(`/${lang}/provider/dashboard`);
      }, 1000);
    } catch (e: unknown) {
      setSaveError(e instanceof Error ? e.message : t('msg_failed_create_service', 'Failed to create service'));
      setSaving(false);
    }
  }

  // ─── Edit mode save ─────────────────────────────────────────────────────────

  async function handleEditSave() {
    setEditSaving(true);
    setEditError(null);
    setEditSuccess(false);
    try {
      const input: UpdateProfileInput = {
        business_name: editForm.business_name || undefined,
        description: editForm.description || undefined,
      };
      const updated = await updateProviderProfile(input);
      setProfile(updated);
      setEditSuccess(true);
      setTimeout(() => setEditSuccess(false), 3000);
    } catch (e: unknown) {
      setEditError(e instanceof Error ? e.message : t('msg_failed_save', 'Failed to save'));
    } finally {
      setEditSaving(false);
    }
  }

  // ─── Derived ────────────────────────────────────────────────────────────────

  const categoryOptions = categories.map(c => ({ value: c.slug, label: c.name }));
  // City options: value is the numeric id stringified for SearchableSelect
  const cityOptions = cities.map(c => ({ value: String(c.id), label: c.city }));

  // ─── Loading / error ────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (loadError && !profile) {
    return (
      <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
        {t('msg_failed_load_profile', 'Failed to load profile')}: {loadError}
      </div>
    );
  }

  // ─── WIZARD MODE ─────────────────────────────────────────────────────────────

  if (isComplete === false) {
    return (
      <div className="max-w-lg mx-auto space-y-6 pb-24 min-h-[calc(100vh+1px)]">
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t('label_complete_profile', 'Complete your profile')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            {t('msg_start_receiving', 'Start receiving client requests in minutes')}
          </p>
        </div>

        <StepIndicator step={step} step1Valid={step1Valid} step2Valid={step2Valid} t={t} />

        {/* ── Step 1: Profile ── */}
        {step === 1 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
            <h2 className="text-sm font-semibold text-gray-800">{t('label_profile_setup', 'Profile Setup')}</h2>

            {/* Photo */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-2">
                {t('label_profile_photo', 'Profile photo')} <span className="text-gray-400 font-normal">({t('label_optional', 'optional')})</span>
              </label>
              <AvatarUpload imageUrl={imageUrl} uploading={uploading} onFileChange={handleImageChange} t={t} />
            </div>

            {/* Business name */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                {t('label_business_name', 'Business name')} <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={step1.business_name}
                onChange={e => {
                  const businessName = e.target.value;
                  setStep1(f => ({
                    ...f,
                    business_name: businessName,
                    slug: step1SlugEditing ? f.slug : slugify(businessName),
                  }));
                  if (!step1Touched.business_name) {
                    setStep1Touched(t => ({ ...t, business_name: true }));
                  }
                  // Mark slug as touched when auto-generating for immediate validation
                  if (!step1SlugEditing && businessName.trim()) {
                    setStep1Touched(t => ({ ...t, slug: true }));
                  }
                  setStep1SlugAvailable(null);
                  setStep1SlugError(null);
                  setStep1SlugSuggestions([]);
                  setSaveError(null);
                }}
                placeholder={t('placeholder_business_name_example', 'e.g. Sofia Plumbing Pro')}
                className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                  step1FieldErrors.business_name ? 'border-red-400' : 
                  step1FieldValid.business_name ? 'border-green-500' : 'border-gray-300'
                }`}
              />
              {step1FieldErrors.business_name && (
                <p className="text-xs text-red-500 mt-1">{step1FieldErrors.business_name}</p>
              )}
            </div>

            {/* Description */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                {t('label_description', 'Description')} <span className="text-gray-400 font-normal">({t('label_optional', 'optional')})</span>
              </label>
              <textarea
                value={step1.description}
                onChange={e => {
                  setStep1(f => ({ ...f, description: e.target.value }));
                  if (!step1Touched.description) {
                    setStep1Touched(t => ({ ...t, description: true }));
                  }
                }}
                rows={3}
                placeholder={t('placeholder_business_description', 'Describe your services, experience and what makes you different')}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 resize-none"
              />
              <div className="text-xs text-gray-400 mt-1">
                {step1.description.length}/{t('msg_50_chars_better', 'At least 50 chars gets better results')}
              </div>
            </div>

            {/* Public URL */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                {t('label_public_url', 'Public URL')} <span className="text-red-400">*</span>
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={step1.slug}
                  onChange={e => {
                    setStep1SlugEditing(true);
                    setStep1SlugManual(true);
                    setStep1(f => ({ ...f, slug: sanitizeSlug(e.target.value) }));
                    if (!step1Touched.slug) {
                      setStep1Touched(t => ({ ...t, slug: true }));
                    }
                    setStep1SlugAvailable(null);
                    setStep1SlugError(null);
                    setStep1SlugSuggestions([]);
                    setSaveError(null);
                  }}
                  placeholder={t('placeholder_business_slug', 'your-business-name')}
                  readOnly={!step1SlugEditing}
                  className={`flex-1 px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                    step1FieldErrors.slug
                      ? 'border-red-400'
                      : step1FieldValid.slug
                      ? 'border-green-500'
                      : 'border-gray-300'
                  } ${!step1SlugEditing ? 'bg-gray-50 cursor-default' : ''}`}
                />
                {!step1SlugEditing && (
                  <button
                    type="button"
                    onClick={() => setStep1SlugEditing(true)}
                    className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                    title={t('btn_edit_url', 'Edit URL')}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
                      <path d="m15 5 4 4"/>
                    </svg>
                  </button>
                )}
                {step1SlugChecking && (
                  <span className="text-xs text-gray-400 whitespace-nowrap">{t('msg_checking', 'Checking...')}</span>
                )}
                {!step1SlugChecking && step1SlugAvailable === true && (
                  <span className="text-xs text-green-600 whitespace-nowrap">{t('msg_available', 'Available')}</span>
                )}
              </div>

              <p className="text-xs text-gray-500 mt-1 break-all">
                nevumo.com/.../{step1.slug || t('placeholder_business_slug', 'your-business-name')}
              </p>
              <p className="text-xs text-gray-500 mt-2">
                {t('msg_url_changes_remaining', 'URL changes remaining')}: {step1SlugChangesRemaining}/{MAX_SLUG_CHANGES}
              </p>
              <p className="text-xs text-orange-600 mt-2">
                {t('msg_url_change_warning', 'You can only change your URL once.')}<br />
                {t('msg_old_links_redirect', 'Old links will continue working (redirected).')}
              </p>

              {step1FieldErrors.slug && (
                <div className="mt-2 p-2 bg-red-50 rounded-lg">
                  <p className="text-xs text-red-600">{step1FieldErrors.slug}</p>
                </div>
              )}

              {!step1FieldErrors.slug && step1SlugAvailable === false && (
                <div className="mt-2 p-2 bg-red-50 rounded-lg">
                  <p className="text-xs text-red-600">{t('msg_url_taken', 'This URL is already taken')}</p>
                </div>
              )}

              {step1SlugSuggestions.length > 0 && (
                <div className="mt-2">
                  <p className="text-xs text-gray-600 mb-1">{t('label_suggestions', 'Suggestions')}:</p>
                  <div className="flex flex-wrap gap-2">
                    {step1SlugSuggestions.map(suggestion => (
                      <button
                        key={suggestion}
                        type="button"
                        onClick={() => {
                          setStep1SlugEditing(true);
                          setStep1SlugManual(true);
                          setStep1(f => ({ ...f, slug: suggestion }));
                          setStep1Touched(t => ({ ...t, slug: true }));
                          setStep1SlugAvailable(null);
                          setStep1SlugError(null);
                          setStep1SlugSuggestions([]);
                        }}
                        className="px-2 py-1 text-xs bg-orange-100 text-orange-700 rounded hover:bg-orange-200 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {saveError && <p className="text-xs text-red-600">{saveError}</p>}

            <div className="pt-1">
              <div className="flex items-center justify-between">
                <button
                  type="button"
                  formNoValidate
                  onClick={handleStep1Next}
                  disabled={saving || step1SlugChecking}
                  className="px-5 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
                >
                  {saving ? t('msg_saving', 'Saving…') : t('btn_continue', 'Continue →')}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    // Flush latest draft before navigating away
                    if (providerId) {
                      saveStep1Draft(providerId, {
                        business_name: step1.business_name,
                        description: step1.description,
                        slug: step1.slug,
                        slugManual: step1SlugManual,
                        slugEditing: step1SlugEditing,
                      });
                    }
                    router.push(`/${lang}/provider/dashboard`);
                  }}
                  className="text-xs text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {t('btn_skip_for_now', 'Skip for now')}
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-2 text-center">
                {t('msg_takes_less_than_1_minute', 'Takes less than 1 minute')}
              </p>
            </div>
          </div>
        )}

        {/* ── Step 2: First Service ── */}
        {step === 2 && (
          <form noValidate onSubmit={e => e.preventDefault()} className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
            <h2 className="text-sm font-semibold text-gray-800">{t('label_add_first_service', 'Add Your First Service')}</h2>

            {/* Title */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                {t('label_service_title', 'Service title')} <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={step2.title}
                onChange={e => {
                  setStep2(f => ({ ...f, title: e.target.value }));
                  if (!step2Touched.title) {
                    setStep2Touched(t => ({ ...t, title: true }));
                  }
                }}
                placeholder={t('placeholder_service_title_example', 'e.g. Apartment cleaning')}
                className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                  step2FieldErrors.title ? 'border-red-400' : 
                  step2FieldValid.title ? 'border-green-500' : 'border-gray-300'
                }`}
              />
              {step2FieldErrors.title && <p className="text-xs text-red-500 mt-1">{step2FieldErrors.title}</p>}
            </div>

            {/* Category */}
            <div>
              <SearchInput
                mode="single"
                options={categoryOptions}
                value={step2.category_slug}
                onChange={v => {
                  setStep2(f => ({ ...f, category_slug: v as string }));
                  if (!step2Touched.category_slug) {
                    setStep2Touched(t => ({ ...t, category_slug: true }));
                  }
                }}
                placeholder={t('placeholder_select_category', 'Select a category')}
                error={step2FieldErrors.category_slug}
              />
            </div>

            {/* Cities */}
            <div>
              <SearchInput
                mode="multi"
                options={cityOptions}
                values={step2.city_ids}
                onChange={ids => {
                  setStep2(f => ({ ...f, city_ids: ids as string[] }));
                  if (!step2Touched.city_ids) {
                    setStep2Touched(t => ({ ...t, city_ids: true }));
                  }
                  
                  // Auto-detect currency from first selected city
                  const cityIds = ids as string[];
                  if (cityIds.length > 0) {
                    const firstCityId = Number(cityIds[0]);
                    const firstCity = cities.find(c => c.id === firstCityId);
                    if (firstCity) {
                      setDetectedCurrency(firstCity.currency);
                    }
                  }
                }}
                placeholder={t('placeholder_select_cities', 'Select cities where you offer this service')}
                error={step2FieldErrors.city_ids}
              />
            </div>

            {/* Price type */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">{t('label_price_type', 'Price type')}</label>
              <select
                value={step2.price_type}
                onChange={e => setStep2(f => ({ ...f, price_type: e.target.value as PriceType }))}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 bg-white"
                aria-label="Select price type"
              >
                {getPriceTypes(t).map(pt => (
                  <option key={pt.value} value={pt.value}>{pt.label}</option>
                ))}
              </select>
            </div>

            {/* Price input - only show when price_type is not "request" */}
            {step2.price_type !== 'request' && (
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  {t('label_price_in_currency', 'Price in {currency}').replace('{currency}', detectedCurrency)}{' '}
                  <span className="text-gray-400 font-normal">({t('label_optional', 'optional')})</span>
                </label>
                <input
                  type="number"
                  min="0"
                  step="1"
                  value={step2.base_price}
                  onChange={e => setStep2(f => ({ ...f, base_price: e.target.value }))}
                  placeholder="0.00"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
                />
              </div>
            )}

            {saveError && <p className="text-xs text-red-600">{saveError}</p>}

            {saveSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center">
                {t('msg_setup_complete_redirecting', 'Setup complete! Redirecting…')}
              </div>
            )}

            <div className="flex items-center gap-3 pt-1">
              <button
                type="button"
                onClick={() => setStep(1)}
                disabled={saving}
                className="text-sm text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
              >
                {t('btn_back', '← Back')}
              </button>
              <button
                type="button"
                onClick={handleCompleteSetup}
                disabled={saving}
                className="px-5 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
              >
                {saving ? t('msg_saving', 'Saving…') : t('btn_complete_setup', 'Complete Setup')}
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2 text-center">
              {t('msg_finish_setup_to_start_getting_clients', 'Finish setup to start getting clients')}
            </p>
          </form>
        )}

      </div>
    );
  }

  // ─── EDIT MODE ────────────────────────────────────────────────────────────────

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-gray-900">{t('nav_profile', 'Profile')}</h1>
        <p className="text-sm text-gray-500 mt-0.5">{t('profile_subtitle', 'Your public business profile')}</p>
      </div>

      {/* Photo */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-800 mb-4">{t('label_profile_photo', 'Profile photo')}</h2>
        <AvatarUpload imageUrl={imageUrl} uploading={uploading} onFileChange={handleImageChange} t={t} />
      </div>

      {/* Details */}
      <form noValidate onSubmit={e => e.preventDefault()} className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-800">{t('label_business_details', 'Business details')}</h2>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">{t('label_business_name', 'Business name')}</label>
          <input
            type="text"
            value={editForm.business_name}
            onChange={e => setEditForm(f => ({ ...f, business_name: e.target.value }))}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
            aria-label="Business name"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">{t('label_description', 'Description')}</label>
          <textarea
            value={editForm.description}
            onChange={e => setEditForm(f => ({ ...f, description: e.target.value }))}
            rows={4}
            placeholder={t('placeholder_business_description', 'Describe your services, experience and what makes you different')}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 resize-none"
          />
        </div>

        {editError && <p className="text-xs text-red-600">{editError}</p>}

        <div className="flex items-center gap-3 pt-1">
          <button
            type="button"
            onClick={handleEditSave}
            disabled={editSaving}
            className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
          >
            {editSaving ? t('msg_saving', 'Saving…') : t('btn_save_changes', 'Save changes')}
          </button>
          {editSuccess && <span className="text-xs text-green-600 font-medium">{t('msg_saved', 'Saved!')}</span>}
        </div>
      </form>
    </div>
  );
}
