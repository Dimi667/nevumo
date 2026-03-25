'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import type { ProviderProfile, UpdateProfileInput, PriceType } from '@/types/provider';
import type { CategoryOut, CityOut } from '@/lib/api';
import { getCategories, getCities } from '@/lib/api';
import {
  getProviderProfile,
  updateProviderProfile,
  uploadProviderImage,
  createService,
  getProviderDashboard,
} from '@/lib/provider-api';
import SearchableSelect from '@/components/dashboard/SearchableSelect';

// ─── Constants ────────────────────────────────────────────────────────────────

const PRICE_TYPES: { value: PriceType; label: string }[] = [
  { value: 'fixed', label: 'Fixed price' },
  { value: 'hourly', label: 'Per hour' },
  { value: 'request', label: 'Per request (quote)' },
  { value: 'per_sqm', label: 'Per sq.m.' },
];

const CURRENCIES = ['EUR', 'BGN', 'USD', 'GBP', 'CHF', 'CZK', 'DKK', 'HUF', 'PLN', 'RON', 'SEK', 'NOK', 'TRY'];

// ─── Types ────────────────────────────────────────────────────────────────────

interface Step1Form {
  business_name: string;
  description: string;
}

interface Step2Form {
  title: string;
  category_slug: string;
  city_id: number | null;
  price_type: PriceType;
  base_price: string;
  currency: string;
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
}: {
  imageUrl: string | null;
  uploading: boolean;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  const ref = useRef<HTMLInputElement>(null);
  return (
    <div className="flex items-center gap-3">
      <div className="w-14 h-14 rounded-full bg-gray-100 overflow-hidden flex-shrink-0 flex items-center justify-center text-gray-400">
        {imageUrl ? (
          <img src={imageUrl} alt="Profile" className="w-full h-full object-cover" />
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        )}
      </div>
      <div>
        <input ref={ref} type="file" accept="image/jpeg,image/png,image/webp" className="hidden" onChange={onFileChange} />
        <button
          type="button"
          onClick={() => ref.current?.click()}
          disabled={uploading}
          className="px-3 py-1.5 border border-gray-300 text-gray-600 hover:bg-gray-100 text-xs font-medium rounded-lg transition-colors disabled:opacity-50"
        >
          {uploading ? 'Uploading…' : imageUrl ? 'Change photo' : 'Upload photo'}
        </button>
        <p className="text-xs text-gray-400 mt-0.5">JPG, PNG or WebP · max 5 MB</p>
      </div>
    </div>
  );
}

// ─── Step Indicator ───────────────────────────────────────────────────────────

function StepIndicator({ step }: { step: 1 | 2 }) {
  return (
    <div className="flex items-center gap-3">
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
        step === 1 ? 'bg-orange-500 text-white' : 'bg-orange-100 text-orange-600'
      }`}>
        {step > 1 ? (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        ) : '1'}
      </div>
      <div className={`flex-1 h-0.5 ${step === 2 ? 'bg-orange-300' : 'bg-gray-200'}`} />
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
        step === 2 ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-400'
      }`}>
        2
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ProfilePage() {
  const params = useParams();
  const router = useRouter();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

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

  // Wizard
  const [step, setStep] = useState<1 | 2>(1);
  const [step1, setStep1] = useState<Step1Form>({ business_name: '', description: '' });
  const [step1Errors, setStep1Errors] = useState<Partial<Step1Form>>({});
  const [step2, setStep2] = useState<Step2Form>({
    title: '',
    category_slug: '',
    city_id: null,
    price_type: 'fixed',
    base_price: '',
    currency: 'EUR',
  });
  const [step2Errors, setStep2Errors] = useState<{ title?: string; category_slug?: string; city_id?: string }>({});
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Edit mode
  const [editForm, setEditForm] = useState<EditForm>({ business_name: '', description: '' });
  const [editSaving, setEditSaving] = useState(false);
  const [editSuccess, setEditSuccess] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      getProviderProfile(),
      getCategories('en'),
      getCities('BG'),
      getProviderDashboard(),
    ])
      .then(([p, cats, citiesData, dashboard]) => {
        setProfile(p);
        setCategories(cats);
        setCities(citiesData);
        setIsComplete(dashboard.profile.is_complete);
        const nameIsEmail = !p.business_name || p.business_name.includes('@');
        setStep1({ business_name: nameIsEmail ? '' : p.business_name, description: p.description ?? '' });
        setEditForm({ business_name: nameIsEmail ? '' : p.business_name, description: p.description ?? '' });
        setImageUrl(p.profile_image_url);
      })
      .catch((e: Error) => setLoadError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleImageChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const result = await uploadProviderImage(file);
      setImageUrl(result.image_url);
    } catch {
      // silently ignore
    } finally {
      setUploading(false);
    }
  }

  // ─── Step 1 submit ──────────────────────────────────────────────────────────

  async function handleStep1Next() {
    const errors: Partial<Step1Form> = {};
    if (step1.business_name.trim().length < 2) {
      errors.business_name = 'Business name must be at least 2 characters';
    }
    setStep1Errors(errors);
    if (Object.keys(errors).length > 0) return;

    setSaving(true);
    setSaveError(null);
    try {
      const input: UpdateProfileInput = {
        business_name: step1.business_name.trim(),
        description: step1.description.trim() || undefined,
      };
      const updated = await updateProviderProfile(input);
      setProfile(updated);
      setStep(2);
    } catch (e: unknown) {
      setSaveError(e instanceof Error ? e.message : 'Failed to save profile');
    } finally {
      setSaving(false);
    }
  }

  // ─── Step 2 submit ──────────────────────────────────────────────────────────

  async function handleCompleteSetup() {
    const errors: { title?: string; category_slug?: string; city_id?: string } = {};
    if (!step2.title.trim()) errors.title = 'Title is required';
    if (!step2.category_slug) errors.category_slug = 'Category is required';
    if (!step2.city_id) errors.city_id = 'City is required';
    setStep2Errors(errors);
    if (Object.keys(errors).length > 0) return;

    const category = categories.find(c => c.slug === step2.category_slug);
    if (!category || !step2.city_id) return;

    setSaving(true);
    setSaveError(null);
    try {
      await createService({
        title: step2.title.trim(),
        category_id: category.id,
        city_ids: [step2.city_id],
        price_type: step2.price_type,
        base_price: step2.base_price ? Number(step2.base_price) : undefined,
        currency: step2.currency,
      });
      setSaveSuccess(true);
      setTimeout(() => router.push(`/${lang}/provider/dashboard`), 1000);
    } catch (e: unknown) {
      setSaveError(e instanceof Error ? e.message : 'Failed to create service');
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
      setEditError(e instanceof Error ? e.message : 'Failed to save');
    } finally {
      setEditSaving(false);
    }
  }

  // ─── Derived ────────────────────────────────────────────────────────────────

  const categoryOptions = categories.map(c => ({ value: c.slug, label: c.name }));
  // City options: value is the numeric id stringified for SearchableSelect
  const cityOptions = cities.map(c => ({ value: String(c.id), label: c.name }));

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
        Failed to load profile: {loadError}
      </div>
    );
  }

  // ─── WIZARD MODE ─────────────────────────────────────────────────────────────

  if (isComplete === false) {
    return (
      <div className="max-w-lg space-y-6">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Complete your profile</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            Step {step} of 2 — {step === 1 ? 'Profile Setup' : 'Add Your First Service'}
          </p>
        </div>

        <StepIndicator step={step} />

        {/* ── Step 1: Profile ── */}
        {step === 1 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
            <h2 className="text-sm font-semibold text-gray-800">Profile Setup</h2>

            {/* Photo */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-2">
                Profile photo <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              <AvatarUpload imageUrl={imageUrl} uploading={uploading} onFileChange={handleImageChange} />
            </div>

            {/* Business name */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Business name <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={step1.business_name}
                onChange={e => setStep1(f => ({ ...f, business_name: e.target.value }))}
                placeholder="e.g. Sofia Plumbing Pro"
                className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                  step1Errors.business_name ? 'border-red-400' : 'border-gray-300'
                }`}
              />
              {step1Errors.business_name && (
                <p className="text-xs text-red-500 mt-1">{step1Errors.business_name}</p>
              )}
            </div>

            {/* Description */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Description <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              <textarea
                value={step1.description}
                onChange={e => setStep1(f => ({ ...f, description: e.target.value }))}
                rows={3}
                placeholder="Describe your business…"
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 resize-none"
              />
            </div>

            {saveError && <p className="text-xs text-red-600">{saveError}</p>}

            <div className="pt-1">
              <button
                type="button"
                onClick={handleStep1Next}
                disabled={saving}
                className="px-5 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
              >
                {saving ? 'Saving…' : 'Next →'}
              </button>
            </div>
          </div>
        )}

        {/* ── Step 2: First Service ── */}
        {step === 2 && (
          <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
            <h2 className="text-sm font-semibold text-gray-800">Add Your First Service</h2>

            {/* Title */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Service title <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={step2.title}
                onChange={e => setStep2(f => ({ ...f, title: e.target.value }))}
                placeholder="e.g. Pipe repair, Massage 60 min…"
                className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                  step2Errors.title ? 'border-red-400' : 'border-gray-300'
                }`}
              />
              {step2Errors.title && <p className="text-xs text-red-500 mt-1">{step2Errors.title}</p>}
            </div>

            {/* Category */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Category <span className="text-red-400">*</span>
              </label>
              <SearchableSelect
                options={categoryOptions}
                value={step2.category_slug}
                onChange={v => setStep2(f => ({ ...f, category_slug: v }))}
                placeholder="Select a category"
              />
              {step2Errors.category_slug && (
                <p className="text-xs text-red-500 mt-1">{step2Errors.category_slug}</p>
              )}
            </div>

            {/* City */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                City <span className="text-red-400">*</span>
              </label>
              <SearchableSelect
                options={cityOptions}
                value={step2.city_id !== null ? String(step2.city_id) : ''}
                onChange={v => setStep2(f => ({ ...f, city_id: v ? Number(v) : null }))}
                placeholder="Select a city"
              />
              {step2Errors.city_id && (
                <p className="text-xs text-red-500 mt-1">{step2Errors.city_id}</p>
              )}
            </div>

            {/* Price type + Price + Currency in a row */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Price type</label>
                <select
                  value={step2.price_type}
                  onChange={e => setStep2(f => ({ ...f, price_type: e.target.value as PriceType }))}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 bg-white"
                >
                  {PRICE_TYPES.map(pt => (
                    <option key={pt.value} value={pt.value}>{pt.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Price <span className="text-gray-400 font-normal">(optional)</span>
                </label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={step2.base_price}
                  onChange={e => setStep2(f => ({ ...f, base_price: e.target.value }))}
                  placeholder="0.00"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
                />
              </div>
            </div>

            {/* Currency */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Currency</label>
              <select
                value={step2.currency}
                onChange={e => setStep2(f => ({ ...f, currency: e.target.value }))}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 bg-white"
              >
                {CURRENCIES.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {saveError && <p className="text-xs text-red-600">{saveError}</p>}

            {saveSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center">
                Setup complete! Redirecting…
              </div>
            )}

            <div className="flex items-center gap-3 pt-1">
              <button
                type="button"
                onClick={() => setStep(1)}
                disabled={saving}
                className="px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-50 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
              >
                ← Back
              </button>
              <button
                type="button"
                onClick={handleCompleteSetup}
                disabled={saving}
                className="px-5 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
              >
                {saving ? 'Saving…' : 'Complete Setup'}
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  // ─── EDIT MODE ────────────────────────────────────────────────────────────────

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Profile</h1>
        <p className="text-sm text-gray-500 mt-0.5">Your public business profile</p>
      </div>

      {/* Photo */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-800 mb-4">Profile photo</h2>
        <AvatarUpload imageUrl={imageUrl} uploading={uploading} onFileChange={handleImageChange} />
      </div>

      {/* Details */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-800">Business details</h2>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Business name</label>
          <input
            type="text"
            value={editForm.business_name}
            onChange={e => setEditForm(f => ({ ...f, business_name: e.target.value }))}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Description</label>
          <textarea
            value={editForm.description}
            onChange={e => setEditForm(f => ({ ...f, description: e.target.value }))}
            rows={4}
            placeholder="Describe your business and services…"
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
            {editSaving ? 'Saving…' : 'Save changes'}
          </button>
          {editSuccess && <span className="text-xs text-green-600 font-medium">Saved!</span>}
        </div>
      </div>
    </div>
  );
}
