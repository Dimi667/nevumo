'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { t } from '@/lib/ui-translations';

interface Option {
  value: string;
  label: string;
}

interface SearchInputProps {
  options: Option[];
  value?: string;           // For mode='single'
  values?: string[];        // For mode='multi'
  onChange: (value: string | string[]) => void;
  placeholder: string;
  mode?: 'single' | 'multi';
  label?: string;
  required?: boolean;
  error?: string;
}

export default function SearchInput({
  options,
  value,
  values,
  onChange,
  placeholder,
  mode = 'single',
  label,
  required,
  error,
}: SearchInputProps) {
  const { dict } = useDashboardI18n();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const isMulti = mode === 'multi';
  const selectedValues = isMulti ? (values || []) : (value ? [value] : []);
  const selectedOptions = options.filter(o => selectedValues.includes(o.value));

  const filtered = query
    ? options.filter(o => o.label.toLowerCase().includes(query.toLowerCase()))
    : options;

  const toggleMulti = useCallback(
    (val: string) => {
      const current = values || [];
      const newValues = current.includes(val)
        ? current.filter(v => v !== val)
        : [...current, val];
      onChange(newValues);
    },
    [values, onChange],
  );

  const removeMulti = useCallback(
    (val: string, e: React.MouseEvent) => {
      e.stopPropagation();
      const current = values || [];
      onChange(current.filter(v => v !== val));
    },
    [values, onChange],
  );

  const handleSelectSingle = useCallback(
    (opt: Option) => {
      onChange(opt.value);
      setOpen(false);
      setQuery('');
    },
    [onChange],
  );

  const handleOpen = useCallback(() => {
    setOpen(true);
    setQuery('');
    setTimeout(() => inputRef.current?.focus(), 0);
  }, []);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        if (isMulti) {
          if (filtered.length > 0 && filtered[0]) {
            toggleMulti(filtered[0].value);
          }
        } else {
          if (filtered.length > 0 && filtered[0]) {
            handleSelectSingle(filtered[0]);
          }
        }
      } else if (e.key === 'Escape') {
        setOpen(false);
        setQuery('');
      }
    },
    [filtered, isMulti, toggleMulti, handleSelectSingle],
  );

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        setQuery('');
      }
    }
    if (open) {
      document.addEventListener('mousedown', onClickOutside);
      return () => document.removeEventListener('mousedown', onClickOutside);
    }
  }, [open]);

  const renderTrigger = () => {
    if (open) {
      return (
        <input
          ref={inputRef}
          autoFocus
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t(dict, 'placeholder_type_to_search', 'Type to search…')}
          className="w-full px-3 py-2 text-sm border border-orange-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 bg-white"
        />
      );
    }

    if (isMulti) {
      return (
        <div
          onClick={handleOpen}
          className={`w-full min-h-[38px] px-3 py-2 text-sm border rounded-lg bg-white flex flex-wrap gap-1.5 items-center cursor-pointer transition-colors ${
            error ? 'border-red-400' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          {selectedOptions.length === 0 ? (
            <span className="text-gray-400">{placeholder}</span>
          ) : (
            selectedOptions.map(opt => (
              <span
                key={opt.value}
                className="inline-flex items-center gap-1 bg-orange-100 text-orange-700 text-xs font-medium px-2 py-0.5 rounded-full"
              >
                {opt.label}
                <button
                  type="button"
                  onMouseDown={e => { e.preventDefault(); removeMulti(opt.value, e); }}
                  className="hover:text-orange-900 leading-none"
                  aria-label={`${t(dict, 'aria_remove_item', 'Remove')} ${opt.label}`}
                >
                  ×
                </button>
              </span>
            ))
          )}
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setOpen(v => !v);
            }}
            aria-label={t(dict, 'aria_open_menu', 'Open menu')}
            className="ml-auto flex-shrink-0 text-gray-400 hover:text-gray-600"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>
        </div>
      );
    }

    // Single mode trigger
    const selectedLabel = options.find(o => o.value === value)?.label ?? '';
    return (
      <button
        type="button"
        onClick={handleOpen}
        className={`w-full px-3 py-2 text-sm border rounded-lg bg-white text-left flex items-center justify-between hover:border-gray-400 transition-colors focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
          error ? 'border-red-400' : 'border-gray-300'
        }`}
      >
        <span className={selectedLabel ? 'text-gray-900' : 'text-gray-400'}>
          {selectedLabel || placeholder}
        </span>
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-gray-400 flex-shrink-0"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>
    );
  };

  return (
    <div ref={containerRef} className="relative">
      {label && (
        <label className="block text-xs font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-400">*</span>}
        </label>
      )}
      
      {renderTrigger()}

      {open && (
        <div className="absolute z-50 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-52 overflow-y-auto">
          {filtered.length === 0 ? (
            <p className="px-3 py-2 text-sm text-gray-400">{t(dict, 'msg_no_results', 'No results')}</p>
          ) : (
            filtered.map(opt => {
              const selected = selectedValues.includes(opt.value);
              return (
                <button
                  key={opt.value}
                  type="button"
                  onMouseDown={e => {
                    e.preventDefault();
                    if (isMulti) {
                      toggleMulti(opt.value);
                    } else {
                      handleSelectSingle(opt);
                    }
                  }}
                  className={`w-full text-left px-3 py-2 text-sm flex items-center gap-2.5 transition-colors hover:bg-orange-50 hover:text-orange-700 ${
                    selected ? 'bg-orange-50 text-orange-700 font-medium' : 'text-gray-700'
                  }`}
                >
                  {isMulti && (
                    <span className={`w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 ${
                      selected ? 'bg-orange-500 border-orange-500' : 'border-gray-300'
                    }`}>
                      {selected && (
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </span>
                  )}
                  {opt.label}
                </button>
              );
            })
          )}
        </div>
      )}

      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}
