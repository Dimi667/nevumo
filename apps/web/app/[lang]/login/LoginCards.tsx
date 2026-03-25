'use client';

import { useEffect } from "react";
import { ActionCard } from "@/components/ui/ActionCard";
import { trackPageEvent } from "@/lib/tracking";
import { isAuthenticated, getAuthUser } from "@/lib/auth-store";

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
  useEffect(() => {
    if (isAuthenticated()) {
      const user = getAuthUser();
      window.location.href = user?.role === "provider"
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
