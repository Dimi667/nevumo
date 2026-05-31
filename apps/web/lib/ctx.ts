interface CtxData {
  city?: string;
  category?: string;
}

const CTX_KEY = 'nevumo_ctx';

function getStoredCtx(): CtxData {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(CTX_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function getCtx(): CtxData {
  return getStoredCtx();
}

export function setCtx(partial: Partial<CtxData>): void {
  if (typeof window === 'undefined') return;
  const current = getStoredCtx();
  const updated = { ...current, ...partial };
  localStorage.setItem(CTX_KEY, JSON.stringify(updated));
}

export function clearCtx(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(CTX_KEY);
}

export function clearCityCtx(): void {
  if (typeof window === 'undefined') return;
  const current = getStoredCtx();
  const { city, ...rest } = current;
  if (Object.keys(rest).length > 0) {
    localStorage.setItem(CTX_KEY, JSON.stringify(rest));
  } else {
    localStorage.removeItem(CTX_KEY);
  }
}

export function clearCategoryCtx(): void {
  if (typeof window === 'undefined') return;
  const current = getStoredCtx();
  const { category, ...rest } = current;
  if (Object.keys(rest).length > 0) {
    localStorage.setItem(CTX_KEY, JSON.stringify(rest));
  } else {
    localStorage.removeItem(CTX_KEY);
  }
}
