const API_BASE = '';

export function trackPageEvent(
  eventType: string,
  page: string,
  metadata: Record<string, string> = {}
): void {
  const data = JSON.stringify({
    event_type: eventType,
    page,
    metadata,
  });

  const url = `${API_BASE}/api/v1/page-events`;

  // DB tracking
  const sent = navigator.sendBeacon(
    url,
    new Blob([data], { type: "application/json" })
  );
  if (!sent) {
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: data,
      keepalive: true,
    }).catch(() => {});
  }

  // GA4 tracking
  if (typeof window !== "undefined" && typeof window.gtag === "function") {
    window.gtag("event", eventType, metadata);
  }
}
