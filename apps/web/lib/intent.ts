export function getStoredIntent(): { intent: string | null; lang: string | null } {
  if (typeof window === "undefined") return { intent: null, lang: null };
  return {
    intent: localStorage.getItem("nevumo_intent"),
    lang: localStorage.getItem("nevumo_lang"),
  };
}

export function clearStoredIntent(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("nevumo_intent");
  localStorage.removeItem("nevumo_lang");
}

export function setStoredIntent(intent: 'client' | 'provider'): void {
  if (typeof window === 'undefined') return;
  const current = localStorage.getItem('nevumo_intent');
  if (!current) {
    localStorage.setItem('nevumo_intent', intent);
  }
}
