'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { t } from '@/lib/ui-translations';

interface Option {
  value: string;
  label: string;
}

interface MultiSelectProps {
  options: Option[];
  values: string[];
  onChange: (values: string[]) => void;
  placeholder: string;
}

export default function MultiSelect({ options, values, onChange, placeholder }: MultiSelectProps) {
  const { dict } = useDashboardI18n();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);

  const filtered = query
    ? options.filter(o => o.label.toLowerCase().includes(query.toLowerCase()))
    : options;

  const toggle = useCallback(
    (val: string) => {
      onChange(values.includes(val) ? values.filter(v => v !== val) : [...values, val]);
    },
    [values, onChange],
  );

  const remove = useCallback(
    (val: string, e: React.MouseEvent) => {
      e.stopPropagation();
      onChange(values.filter(v => v !== val));
    },
    [values, onChange],
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

  const selectedOptions = options.filter(o => values.includes(o.value));

  return (
    <div ref={containerRef} className="relative">
      {/* Trigger */}
      <div
        onClick={() => setOpen(v => !v)}
        className={`w-full min-h-[38px] px-3 py-2 text-sm border rounded-lg bg-white flex flex-wrap gap-1.5 items-center cursor-pointer transition-colors ${
          open ? 'border-orange-400 ring-2 ring-orange-300' : 'border-gray-300 hover:border-gray-400'
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
                onMouseDown={e => { e.preventDefault(); remove(opt.value, e); }}
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
            <polyline points={open ? '18 15 12 9 6 15' : '6 9 12 15 18 9'} />
          </svg>
        </button>
      </div>

      {/* Dropdown */}
      {open && (
        <div className="absolute z-50 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg">
          <div className="p-2 border-b border-gray-100">
            <input
              autoFocus
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === 'Escape' && setOpen(false)}
              placeholder={t(dict, 'placeholder_type_to_search', 'Type to search…')}
              className="w-full px-2 py-1 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-1 focus:ring-orange-300 focus:border-orange-400"
            />
          </div>
          <div className="max-h-48 overflow-y-auto">
            {filtered.length === 0 ? (
              <p className="px-3 py-2 text-sm text-gray-400">{t(dict, 'msg_no_results', 'No results')}</p>
            ) : (
              filtered.map(opt => {
                const selected = values.includes(opt.value);
                return (
                  <button
                    key={opt.value}
                    type="button"
                    onMouseDown={e => { e.preventDefault(); toggle(opt.value); }}
                    className={`w-full text-left px-3 py-2 text-sm flex items-center gap-2.5 transition-colors hover:bg-orange-50 ${
                      selected ? 'text-orange-700' : 'text-gray-700'
                    }`}
                  >
                    <span className={`w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 ${
                      selected ? 'bg-orange-500 border-orange-500' : 'border-gray-300'
                    }`}>
                      {selected && (
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                          <polyline points="20 6 9 17 4 12" />
                        </svg>
                      )}
                    </span>
                    {opt.label}
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}
