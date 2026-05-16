'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { t, type TranslationDict } from '@/lib/ui-translations';

interface PageProps {
  params: Promise<{ lang: string }>;
}

const API_BASE = typeof window === 'undefined' 
  ? (process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') 
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

interface FormData {
  service_description: string;
  contract_date: string;
  consumer_name: string;
  consumer_address: string;
  account_id: string;
  email: string;
  submission_date: string;
}

interface FormErrors {
  service_description?: string;
  contract_date?: string;
  consumer_name?: string;
  consumer_address?: string;
  email?: string;
  submission_date?: string;
}

export default function WithdrawalPage({ params }: PageProps) {
  const [lang, setLang] = useState<string>(DEFAULT_LANGUAGE);
  const [dict, setDict] = useState<TranslationDict>({});
  const [formData, setFormData] = useState<FormData>({
    service_description: '',
    contract_date: '',
    consumer_name: '',
    consumer_address: '',
    account_id: '',
    email: '',
    submission_date: new Date().toISOString().split('T')[0]
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    params.then(({ lang: paramLang }) => {
      const normalizedLang = SUPPORTED_LANGUAGES.includes(paramLang) ? paramLang : DEFAULT_LANGUAGE;
      setLang(normalizedLang);

      fetch(`${API_BASE}/api/v1/translations/withdrawal?lang=${normalizedLang}`)
        .then(res => res.json())
        .then(data => setDict(data))
        .catch(err => console.error('Fetch error:', err));
    });
  }, [params]);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.service_description.trim()) {
      newErrors.service_description = t(dict, 'error_service_description_required', 'Service description is required');
    }
    if (!formData.contract_date) {
      newErrors.contract_date = t(dict, 'error_contract_date_required', 'Contract date is required');
    }
    if (!formData.consumer_name.trim()) {
      newErrors.consumer_name = t(dict, 'error_consumer_name_required', 'Consumer name is required');
    }
    if (!formData.consumer_address.trim()) {
      newErrors.consumer_address = t(dict, 'error_consumer_address_required', 'Consumer address is required');
    }
    if (!formData.email.trim()) {
      newErrors.email = t(dict, 'error_email_required', 'Email is required');
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = t(dict, 'error_email_invalid', 'Invalid email format');
    }
    if (!formData.submission_date) {
      newErrors.submission_date = t(dict, 'error_submission_date_required', 'Submission date is required');
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(`${API_BASE}/api/v1/legal/withdrawal`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          lang: lang
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Submission failed');
      }

      setSubmitSuccess(true);
      setFormData({
        service_description: '',
        contract_date: '',
        consumer_name: '',
        consumer_address: '',
        account_id: '',
        email: '',
        submission_date: new Date().toISOString().split('T')[0]
      });
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  if (submitSuccess) {
    return (
      <div className="min-h-screen bg-white">
        <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-100">
          <Link href={`/${lang}`} className="inline-flex items-center">
            <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
          </Link>
          <Link href={`/${lang}`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
            {t(dict, 'back_to_home', 'Back to home')}
          </Link>
        </nav>

        <main className="max-w-3xl mx-auto px-4 py-12">
          <div className="bg-green-50 border border-green-200 rounded-md p-8 text-center">
            <svg className="mx-auto h-16 w-16 text-green-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="text-2xl font-bold text-green-900 mb-2">
              {t(dict, 'success_title', 'Form Submitted Successfully')}
            </h2>
            <p className="text-green-700 mb-6">
              {t(dict, 'success_message', 'Your withdrawal form has been submitted and sent to our legal team.')}
            </p>
            <Link
              href={`/${lang}`}
              className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              {t(dict, 'back_to_home', 'Back to home')}
            </Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-100">
        <Link href={`/${lang}`} className="inline-flex items-center">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </Link>
        <Link href={`/${lang}`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          {t(dict, 'back_to_home', 'Back to home')}
        </Link>
      </nav>

      <main className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {t(dict, 'page_title', 'Withdrawal Form')}
        </h1>
        <p className="text-gray-600 mb-8">
          {t(dict, 'page_description', 'Complete this form to withdraw from your contract with Nevumo.')}
        </p>

        {submitError && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-900 text-sm mb-6">
            {submitError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Service Description */}
          <div>
            <label htmlFor="service_description" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_service_description', 'Service Description')} <span className="text-red-500">*</span>
            </label>
            <textarea
              id="service_description"
              name="service_description"
              value={formData.service_description}
              onChange={handleChange}
              rows={4}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.service_description ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.service_description && (
              <p className="mt-1 text-sm text-red-600">{errors.service_description}</p>
            )}
          </div>

          {/* Contract Date */}
          <div>
            <label htmlFor="contract_date" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_contract_date', 'Contract Date')} <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              id="contract_date"
              name="contract_date"
              value={formData.contract_date}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.contract_date ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.contract_date && (
              <p className="mt-1 text-sm text-red-600">{errors.contract_date}</p>
            )}
          </div>

          {/* Consumer Name */}
          <div>
            <label htmlFor="consumer_name" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_consumer_name', 'Consumer Name')} <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="consumer_name"
              name="consumer_name"
              value={formData.consumer_name}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.consumer_name ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.consumer_name && (
              <p className="mt-1 text-sm text-red-600">{errors.consumer_name}</p>
            )}
          </div>

          {/* Consumer Address */}
          <div>
            <label htmlFor="consumer_address" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_consumer_address', 'Consumer Address')} <span className="text-red-500">*</span>
            </label>
            <textarea
              id="consumer_address"
              name="consumer_address"
              value={formData.consumer_address}
              onChange={handleChange}
              rows={3}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.consumer_address ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.consumer_address && (
              <p className="mt-1 text-sm text-red-600">{errors.consumer_address}</p>
            )}
          </div>

          {/* Account ID (Optional) */}
          <div>
            <label htmlFor="account_id" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_account_id', 'Account ID')} ({t(dict, 'optional', 'optional')})
            </label>
            <input
              type="text"
              id="account_id"
              name="account_id"
              value={formData.account_id}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_email', 'Email')} <span className="text-red-500">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.email ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email}</p>
            )}
          </div>

          {/* Submission Date */}
          <div>
            <label htmlFor="submission_date" className="block text-sm font-medium text-gray-700 mb-2">
              {t(dict, 'label_submission_date', 'Submission Date')} <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              id="submission_date"
              name="submission_date"
              value={formData.submission_date}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                errors.submission_date ? 'border-red-500' : 'border-gray-300'
              }`}
              required
            />
            {errors.submission_date && (
              <p className="mt-1 text-sm text-red-600">{errors.submission_date}</p>
            )}
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-end gap-4">
            <Link
              href={`/${lang}/terms`}
              className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
            >
              {t(dict, 'cancel', 'Cancel')}
            </Link>
            <button
              type="submit"
              disabled={isSubmitting}
              className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? t(dict, 'submitting', 'Submitting...') : t(dict, 'submit', 'Submit Form')}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
