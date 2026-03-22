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

function trackClick(intent: string, lang: string): void {
  trackPageEvent("login_card_click", "login", { intent, lang });
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
        onClick={() => trackClick("client", lang)}
      />
      <ActionCard
        href={`/${lang}/auth?role=provider`}
        label={offerLabel}
        subtext={offerSubtext}
        onClick={() => trackClick("provider", lang)}
      />
    </>
  );
}
