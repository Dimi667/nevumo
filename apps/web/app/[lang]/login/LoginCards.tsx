'use client';

import { ActionCard } from "@/components/ui/ActionCard";
import { trackPageEvent } from "@/lib/tracking";

interface LoginCardsProps {
  lang: string;
  findLabel: string;
  findSubtext: string;
  offerLabel: string;
  offerSubtext: string;
}

function trackClick(intent: "client" | "provider", cta: string, lang: string): void {
  localStorage.setItem("nevumo_intent", intent);
  localStorage.setItem("nevumo_lang", lang);
  trackPageEvent("login_intent_selected", "login", { intent, cta, lang });
}

export function LoginCards({
  lang,
  findLabel,
  findSubtext,
  offerLabel,
  offerSubtext,
}: LoginCardsProps) {
  return (
    <>
      <ActionCard
        href={`/${lang}/auth?role=client`}
        label={findLabel}
        subtext={findSubtext}
        onClick={() => trackClick("client", "find_service", lang)}
      />
      <ActionCard
        href={`/${lang}/auth?role=provider`}
        label={offerLabel}
        subtext={offerSubtext}
        onClick={() => trackClick("provider", "offer_service", lang)}
      />
    </>
  );
}
