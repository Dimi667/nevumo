'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams } from 'next/navigation';
import type { CategoryOut, CityOut } from '@/lib/api';
import { getCategories, getCities } from '@/lib/api';
import ServiceCard from '@/components/dashboard/ServiceCard';
import SearchableSelect from '@/components/dashboard/SearchableSelect';
import MultiSelect from '@/components/dashboard/MultiSelect';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import type { Service, PriceType } from '@/types/provider';
import { getProviderServices, createService, updateService, deleteService } from '@/lib/provider-api';
import { t, type TranslationDict } from '@/lib/ui-translations';

// ─── Constants ────────────────────────────────────────────────────────────────

function getPriceTypes(dict: TranslationDict): { value: PriceType; label: string }[] {
  return [
    { value: 'fixed', label: t(dict, 'price_type_fixed', 'Fixed price') },
    { value: 'hourly', label: t(dict, 'price_type_hourly', 'Per hour') },
    { value: 'request', label: t(dict, 'price_type_request', 'Per request (quote)') },
    { value: 'per_sqm', label: t(dict, 'price_type_per_sqm', 'Per sq.m.') },
  ];
}

const CURRENCIES = ['EUR', 'USD', 'GBP', 'CHF', 'CZK', 'DKK', 'HUF', 'PLN', 'RON', 'SEK', 'NOK', 'TRY'];

// ─── Types ────────────────────────────────────────────────────────────────────

interface ServiceForm {
  title: string;
  description: string;
  category_slug: string;
  city_ids: string[];   // string[] for MultiSelect; converted to number[] on submit
  price_type: PriceType;
  base_price: string;
}

type FormMode = 'new' | 'edit';

interface FormErrors {
  title?: string;
  category_slug?: string;
  city_ids?: string;
}

const EMPTY_FORM: ServiceForm = {
  title: '',
  description: '',
  category_slug: '',
  city_ids: [],
  price_type: 'request',
  base_price: '',
};

// ─── Toast ────────────────────────────────────────────────────────────────────

function Toast({ message, onDone }: { message: string; onDone: () => void }) {
  useEffect(() => {
    const id = setTimeout(onDone, 3000);
    return () => clearTimeout(id);
  }, [onDone]);

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-gray-900 text-white text-sm px-4 py-2.5 rounded-xl shadow-lg">
      {message}
    </div>
  );
}

// ─── Delete confirmation modal ────────────────────────────────────────────────

function DeleteModal({
  service,
  onConfirm,
  onCancel,
  deleting,
  dict,
}: {
  service: Service;
  onConfirm: () => void;
  onCancel: () => void;
  deleting: boolean;
  dict: TranslationDict;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl p-6 shadow-xl max-w-sm w-full mx-4 space-y-4">
        <h3 className="text-base font-semibold text-gray-900">{t(dict, 'btn_delete_service', 'Delete service')}</h3>
        <p className="text-sm text-gray-500">
          {t(dict, 'msg_delete_confirm', 'Are you sure you want to delete')}{' '}
          <span className="font-medium text-gray-800">{service.title}</span>?
          {t(dict, 'msg_delete_undo_warning', 'This action cannot be undone.')}
        </p>
        <div className="flex gap-3 pt-1">
          <button
            onClick={onCancel}
            disabled={deleting}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            {t(dict, 'btn_cancel', 'Cancel')}
          </button>
          <button
            onClick={onConfirm}
            disabled={deleting}
            className="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
          >
            {deleting ? t(dict, 'msg_deleting', 'Deleting…') : t(dict, 'btn_delete', 'Delete')}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Service Form ─────────────────────────────────────────────────────────────

function ServiceForm({
  mode,
  form,
  setForm,
  errors,
  categoryOptions,
  cityOptions,
  cities,
  detectedCurrency,
  setDetectedCurrency,
  saving,
  formError,
  onSave,
  onCancel,
  dict,
}: {
  mode: FormMode;
  form: ServiceForm;
  setForm: React.Dispatch<React.SetStateAction<ServiceForm>>;
  errors: FormErrors;
  categoryOptions: { value: string; label: string }[];
  cityOptions: { value: string; label: string }[];
  cities: CityOut[];
  detectedCurrency: string;
  setDetectedCurrency: React.Dispatch<React.SetStateAction<string>>;
  saving: boolean;
  formError: string | null;
  onSave: () => void;
  onCancel: () => void;
  dict: TranslationDict;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
      <h2 className="text-sm font-semibold text-gray-800">
        {mode === 'new' ? t(dict, 'btn_new_service', 'New Service') : t(dict, 'btn_edit_service', 'Edit Service')}
      </h2>

      {/* Title */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">
          {t(dict, 'label_title', 'Title')} <span className="text-red-400">*</span>
        </label>
        <input
          type="text"
          value={form.title}
          onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
          placeholder={t(dict, 'placeholder_service_title_example', 'e.g. Apartment cleaning')}
          className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
            errors.title ? 'border-red-400' : 'border-gray-300'
          }`}
        />
        {errors.title && <p className="text-xs text-red-500 mt-1">{errors.title}</p>}
      </div>

      {/* Description */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">
          {t(dict, 'label_description', 'Description')} <span className="text-gray-400">({t(dict, 'label_optional', 'optional')})</span>
        </label>
        <textarea
          value={form.description}
          onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
          rows={2}
          placeholder={t(dict, 'placeholder_description', 'Brief description…')}
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 resize-none"
        />
      </div>

      {/* Category */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">
          {t(dict, 'label_category', 'Category')} <span className="text-red-400">*</span>
        </label>
        <SearchableSelect
          options={categoryOptions}
          value={form.category_slug}
          onChange={v => setForm(f => ({ ...f, category_slug: v }))}
          placeholder={t(dict, 'placeholder_select_category', 'Select a category')}
        />
        {errors.category_slug && <p className="text-xs text-red-500 mt-1">{errors.category_slug}</p>}
      </div>

      {/* Cities */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">
          {t(dict, 'label_cities', 'Cities')} <span className="text-red-400">*</span>
        </label>
        <MultiSelect
          options={cityOptions}
          values={form.city_ids}
          onChange={ids => {
            setForm(f => ({ ...f, city_ids: ids }));
            
            // Auto-detect currency from first selected city
            if (ids.length > 0) {
              const firstCityId = Number(ids[0]);
              const firstCity = cities.find(c => c.id === firstCityId);
              if (firstCity) {
                setDetectedCurrency(firstCity.currency);
              }
            }
          }}
          placeholder={t(dict, 'placeholder_select_cities', 'Select cities where you offer this service')}
        />
        {errors.city_ids && <p className="text-xs text-red-500 mt-1">{errors.city_ids}</p>}
      </div>

      {/* Price type */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">{t(dict, 'label_price_type', 'Price type')}</label>
        <select
          value={form.price_type}
          onChange={e => setForm(f => ({ ...f, price_type: e.target.value as PriceType }))}
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 bg-white"
          aria-label={t(dict, 'label_price_type', 'Price type')}
        >
          {getPriceTypes(dict).map(pt => (
            <option key={pt.value} value={pt.value}>{pt.label}</option>
          ))}
        </select>
      </div>

      {/* Price input - only show when price_type is not "request" */}
      {form.price_type !== 'request' && (
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">
            {t(dict, 'label_price_in_currency', 'Price in {currency}').replace('{currency}', detectedCurrency)}{' '}
            <span className="text-gray-400 font-normal">({t(dict, 'label_optional', 'optional')})</span>
          </label>
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.base_price}
            onChange={e => setForm(f => ({ ...f, base_price: e.target.value }))}
            placeholder="0.00"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
          />
        </div>
      )}

      {formError && <p className="text-xs text-red-600">{formError}</p>}

      <div className="flex items-center gap-2 pt-1">
        <button
          type="button"
          onClick={onSave}
          disabled={saving}
          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          {saving ? t(dict, 'msg_saving', 'Saving…') : (mode === 'new' ? t(dict, 'btn_create_service', 'Create Service') : t(dict, 'btn_save_changes', 'Save Changes'))}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={saving}
          className="px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
        >
          {t(dict, 'btn_cancel', 'Cancel')}
        </button>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ServicesPage() {
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const { dict } = useDashboardI18n();

  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<CategoryOut[]>([]);
  const [cities, setCities] = useState<CityOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [formMode, setFormMode] = useState<FormMode>('new');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<ServiceForm>(EMPTY_FORM);
  const [detectedCurrency, setDetectedCurrency] = useState<string>('EUR');
  const [formErrors, setFormErrors] = useState<FormErrors>({});
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const [deleteTarget, setDeleteTarget] = useState<Service | null>(null);
  const [deleting, setDeleting] = useState(false);

  const [toast, setToast] = useState<string | null>(null);
  const clearToast = useCallback(() => setToast(null), []);

  useEffect(() => {
    Promise.all([
      getProviderServices(),
      getCategories(lang),
      getCities('BG', lang),
      getCities('RS', lang),
      getCities('PL', lang),
    ])
      .then(([svcs, cats, bgCities, rsCities, plCities]) => {
        setServices(svcs);
        setCategories(cats);
        setCities([...bgCities, ...rsCities, ...plCities]);
      })
      .catch((e: Error) => setLoadError(e.message))
      .finally(() => setLoading(false));
  }, [lang]);

  function openNew() {
    setFormMode('new');
    setEditingId(null);
    setForm(EMPTY_FORM);
    setFormErrors({});
    setFormError(null);
    setShowForm(true);
  }

  function openEdit(service: Service) {
    setFormMode('edit');
    setEditingId(service.id);
    setForm({
      title: service.title,
      description: service.description ?? '',
      category_slug: service.category_slug,
      city_ids: service.cities.map(c => String(c.id)),
      price_type: service.price_type,
      base_price: service.base_price !== null ? String(service.base_price) : '',
    });
    setFormErrors({});
    setFormError(null);
    setShowForm(true);
  }

  function closeForm() {
    setShowForm(false);
    setEditingId(null);
    setFormErrors({});
    setFormError(null);
  }

  function validate(): boolean {
    const errors: FormErrors = {};
    if (!form.title.trim()) errors.title = t(dict, 'error_title_required', 'Title is required');
    if (!form.category_slug) errors.category_slug = t(dict, 'error_category_required', 'Category is required');
    if (form.city_ids.length === 0) errors.city_ids = t(dict, 'error_city_required', 'At least one city is required');
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleSave() {
    if (!validate()) return;
    const category = categories.find(c => c.slug === form.category_slug);
    if (!category) return;

    setSaving(true);
    setFormError(null);
    const payload: any = {
      title: form.title.trim(),
      category_id: category.id,
      city_ids: form.city_ids.map(Number),
      description: form.description.trim() || undefined,
      price_type: form.price_type,
    };
    
    // Only include base_price and currency if price_type is not "request"
    if (form.price_type !== 'request') {
      payload.base_price = form.base_price ? Number(form.base_price) : undefined;
      payload.currency = detectedCurrency;
    }

    try {
      if (formMode === 'new') {
        const created = await createService(payload);
        setServices(prev => [...prev, created]);
        setToast(t(dict, 'msg_service_created', 'Service created successfully'));
      } else if (editingId) {
        const updated = await updateService(editingId, payload);
        setServices(prev => prev.map(s => s.id === editingId ? updated : s));
        setToast(t(dict, 'msg_service_updated', 'Service updated successfully'));
      }
      closeForm();
    } catch (e: unknown) {
      setFormError(e instanceof Error ? e.message : t(dict, 'msg_failed_save_service', 'Failed to save service'));
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteConfirm() {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      await deleteService(deleteTarget.id);
      setServices(prev => prev.filter(s => s.id !== deleteTarget.id));
      setToast(t(dict, 'msg_service_deleted', 'Service deleted'));
      setDeleteTarget(null);
    } catch (e: unknown) {
      setToast(e instanceof Error ? e.message : t(dict, 'msg_failed_delete_service', 'Failed to delete service'));
      setDeleteTarget(null);
    } finally {
      setDeleting(false);
    }
  }

  const categoryOptions = categories.map(c => ({ value: c.slug, label: c.name }));
  const cityOptions = cities.map(c => ({ value: String(c.id), label: c.city }));

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
        {t(dict, 'msg_failed_load_services', 'Failed to load services')}: {loadError}
      </div>
    );
  }

  return (
    <>
      {toast && <Toast message={toast} onDone={clearToast} />}
      {deleteTarget && (
        <DeleteModal
          service={deleteTarget}
          onConfirm={handleDeleteConfirm}
          onCancel={() => setDeleteTarget(null)}
          deleting={deleting}
          dict={dict}
        />
      )}

      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-gray-900">{t(dict, 'nav_services', 'Services')}</h1>
            <p className="text-sm text-gray-500 mt-0.5">
              {t(dict, 'msg_services_count', '{count} services').replace('{count}', String(services.length))}
            </p>
          </div>
          {!showForm && (
            <button
              onClick={openNew}
              className="flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              {t(dict, 'btn_add_service', 'Add Service')}
            </button>
          )}
        </div>

        {/* Form */}
        {showForm && (
          <ServiceForm
            mode={formMode}
            form={form}
            setForm={setForm}
            errors={formErrors}
            categoryOptions={categoryOptions}
            cityOptions={cityOptions}
            cities={cities}
            detectedCurrency={detectedCurrency}
            setDetectedCurrency={setDetectedCurrency}
            saving={saving}
            formError={formError}
            onSave={handleSave}
            onCancel={closeForm}
            dict={dict}
          />
        )}

        {/* Empty state */}
        {services.length === 0 && !showForm ? (
          <div className="bg-white rounded-xl border border-gray-200 p-10 text-center space-y-3">
            <p className="text-sm font-medium text-gray-700">{t(dict, 'msg_no_services_yet', 'No services yet')}</p>
            <p className="text-xs text-gray-400">{t(dict, 'msg_add_services_desc', 'Add the services you offer to start receiving leads.')}</p>
            <button
              onClick={openNew}
              className="mt-2 inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              {t(dict, 'btn_add_service', 'Add Service')}
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {services.map(service => (
              <ServiceCard
                key={service.id}
                service={service}
                onEdit={openEdit}
                onDelete={setDeleteTarget}
              />
            ))}
          </div>
        )}
      </div>
    </>
  );
}
