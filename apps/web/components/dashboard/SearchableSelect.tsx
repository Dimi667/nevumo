'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';

interface Option {
  value: string;
  label: string;
}

interface SearchableSelectProps {
  options: Option[];
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}

export default function SearchableSelect({
  options,
  value,
  onChange,
  placeholder,
}: SearchableSelectProps) {
  const { t } = useDashboardI18n();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedLabel = options.find(o => o.value === value)?.label ?? '';

  const filtered = query
    ? options.filter(o => o.label.toLowerCase().includes(query.toLowerCase()))
    : options;

  const handleOpen = useCallback(() => {
    setOpen(true);
    setQuery('');
  }, []);

  const handleSelect = useCallback(
    (opt: Option) => {
      onChange(opt.value);
      setOpen(false);
      setQuery('');
    },
    [onChange],
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        if (filtered.length > 0 && filtered[0]) handleSelect(filtered[0]);
      } else if (e.key === 'Escape') {
        setOpen(false);
        setQuery('');
      }
    },
    [filtered, handleSelect],
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

  return (
    <div ref={containerRef} className="relative">
      {open ? (
        <input
          ref={inputRef}
          autoFocus
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t('placeholder_type_to_search', 'Type to search…')}
          className="w-full px-3 py-2 text-sm border border-orange-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 bg-white"
        />
      ) : (
        <button
          type="button"
          onClick={handleOpen}
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-left flex items-center justify-between hover:border-gray-400 transition-colors focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
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
      )}

      {open && (
        <div className="absolute z-50 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-52 overflow-y-auto">
          {filtered.length === 0 ? (
            <p className="px-3 py-2 text-sm text-gray-400">{t('msg_no_results', 'No results')}</p>
          ) : (
            filtered.map(opt => (
              <button
                key={opt.value}
                type="button"
                onMouseDown={e => {
                  e.preventDefault();
                  handleSelect(opt);
                }}
                className={`w-full text-left px-3 py-2 text-sm transition-colors hover:bg-orange-50 hover:text-orange-700 ${
                  opt.value === value ? 'bg-orange-50 text-orange-700 font-medium' : 'text-gray-700'
                }`}
              >
                {opt.label}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
