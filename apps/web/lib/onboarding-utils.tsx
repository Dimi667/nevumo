import React from 'react';

// ─── Step 1 Draft Persistence (sessionStorage) ───────────────────────────────

const STEP1_DRAFT_KEY = 'onboarding_step1_draft';

export interface Step1Draft {
  business_name: string;
  description: string;
  slug: string;
  slugManual: boolean;
  slugEditing: boolean;
  providerId: string; // To prevent cross-account leakage
  savedAt: string;
}

/**
 * Get the scoped storage key for a specific provider
 */
function getDraftKey(providerId: string): string {
  return `${STEP1_DRAFT_KEY}_${providerId}`;
}

/**
 * Save Step 1 draft to sessionStorage
 */
export function saveStep1Draft(
  providerId: string,
  draft: Omit<Step1Draft, 'providerId' | 'savedAt'>
): void {
  if (typeof window === 'undefined') return;
  
  const data: Step1Draft = {
    ...draft,
    providerId,
    savedAt: new Date().toISOString(),
  };
  
  try {
    sessionStorage.setItem(getDraftKey(providerId), JSON.stringify(data));
  } catch {
    // Silently fail if storage is unavailable
  }
}

/**
 * Load Step 1 draft from sessionStorage
 * Returns null if no draft exists or if draft belongs to different provider
 */
export function loadStep1Draft(providerId: string): Step1Draft | null {
  if (typeof window === 'undefined') return null;
  
  try {
    const raw = sessionStorage.getItem(getDraftKey(providerId));
    if (!raw) return null;
    
    const draft: Step1Draft = JSON.parse(raw);
    
    // Safety check: verify the draft belongs to current provider
    if (draft.providerId !== providerId) return null;
    
    return draft;
  } catch {
    return null;
  }
}

/**
 * Clear Step 1 draft from sessionStorage
 */
export function clearStep1Draft(providerId: string): void {
  if (typeof window === 'undefined') return;
  
  try {
    sessionStorage.removeItem(getDraftKey(providerId));
  } catch {
    // Silently fail
  }
}

// ─── Onboarding State Types ───────────────────────────────────────────────────

export interface OnboardingState {
  isProfileComplete: boolean;
  isServiceComplete: boolean;
  stepsRemaining: number;
  missingProfile: boolean;
  missingService: boolean;
}

export function deriveOnboardingState(missingFields: string[] | undefined): OnboardingState {
  const missing = missingFields ?? [];
  
  // Profile is incomplete if business_name is in missing_fields
  const missingProfile = missing.includes('business_name');
  
  // Service is incomplete if service and/or city is in missing_fields
  const missingService = missing.includes('service') || missing.includes('city');
  
  const isProfileComplete = !missingProfile;
  const isServiceComplete = !missingService;
  
  // Count remaining steps
  let stepsRemaining = 0;
  if (missingProfile) stepsRemaining++;
  if (missingService) stepsRemaining++;
  
  return {
    isProfileComplete,
    isServiceComplete,
    stepsRemaining,
    missingProfile,
    missingService,
  };
}

export interface HeroContent {
  headline: string;
  description: string;
  ctaLabel: string;
}

export function getHeroContent(state: OnboardingState, t: (key: string, fallback?: string) => string): HeroContent {
  if (state.missingProfile) {
    // Step 1 incomplete - user skipped without entering business name
    return {
      headline: t('onboarding_hero_2steps_title', "You're 2 steps away from getting clients"),
      description: t('onboarding_hero_2steps_desc', 'Complete your profile to start receiving requests'),
      ctaLabel: t('onboarding_hero_2steps_cta', 'Complete your profile'),
    };
  }
  
  if (state.missingService) {
    // Profile complete, service missing
    return {
      headline: t('onboarding_hero_1step_title', "You're 1 step away from getting clients"),
      description: t('onboarding_hero_1step_desc', 'Add your first service to start receiving requests'),
      ctaLabel: t('onboarding_hero_1step_cta', 'Add your first service'),
    };
  }
  
  // Should not reach here if called correctly (only when incomplete)
  return {
    headline: t('onboarding_hero_2steps_title', "You're 2 steps away from getting clients"),
    description: t('onboarding_hero_2steps_desc', 'Complete your profile to start receiving requests'),
    ctaLabel: t('onboarding_hero_2steps_cta', 'Complete your profile'),
  };
}

// Step indicator component that matches the profile wizard styling
export interface StepIndicatorProps {
  isProfileComplete: boolean;
  isServiceComplete: boolean;
  compact?: boolean;
}

export function StepIndicator({ 
  isProfileComplete, 
  isServiceComplete,
  compact = false 
}: StepIndicatorProps) {
  const sizeClasses = compact 
    ? 'w-4 h-4 text-[8px]' 
    : 'w-8 h-8 text-sm';
  
  const iconSize = compact ? 8 : 14;
  const strokeWidth = compact ? 2 : 2.5;

  return (
    <div className={`flex items-center ${compact ? 'gap-2' : 'gap-6'}`}>
      {/* Step 1 - Profile */}
      <div className="flex flex-col items-center">
        <div className={`${sizeClasses} rounded-full flex items-center justify-center font-semibold ${
          isProfileComplete ? 'bg-green-500 text-white' : 'bg-orange-500 text-white'
        }`}>
          {isProfileComplete ? (
            <svg width={iconSize} height={iconSize} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '1'}
        </div>
        <span className={`text-xs font-medium mt-1 ${
          isProfileComplete ? 'text-gray-700' : 'text-orange-600'
        }`}>
          Profile
        </span>
      </div>

      {/* Progress Line */}
      <div className={`${compact ? 'w-4' : 'flex-1 w-8'} h-0.5 ${
        isProfileComplete ? 'bg-green-500' : 'bg-gray-200'
      }`} />

      {/* Step 2 - Service */}
      <div className="flex flex-col items-center">
        <div className={`${sizeClasses} rounded-full flex items-center justify-center font-semibold ${
          isServiceComplete ? 'bg-green-500 text-white' : isProfileComplete ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-400'
        }`}>
          {isServiceComplete ? (
            <svg width={iconSize} height={iconSize} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '2'}
        </div>
        <span className={`text-xs font-medium mt-1 ${
          isProfileComplete && !isServiceComplete ? 'text-orange-600' : 'text-gray-400'
        }`}>
          Service
        </span>
      </div>
    </div>
  );
}

// Compact step indicator for hero footer
export interface CompactStepIndicatorProps {
  state: import('./onboarding-utils').OnboardingState;
  t: (key: string, fallback?: string) => string;
}

export function CompactStepIndicator({ 
  state,
  t
}: CompactStepIndicatorProps) {
  const { isProfileComplete, isServiceComplete } = state;
  return (
    <div className="flex items-center justify-center gap-3">
      {/* Step 1 - Profile */}
      <div className="flex items-center gap-1">
        <div className={`w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-semibold ${
          isProfileComplete ? 'bg-green-500 text-white' : 'bg-orange-500 text-white'
        }`}>
          {isProfileComplete ? (
            <svg width={8} height={8} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '1'}
        </div>
        <span className={`text-xs ${isProfileComplete ? 'text-gray-600' : 'text-orange-600 font-medium'}`}>
          {t('onboarding_step_profile', 'Profile')}
        </span>
      </div>

      {/* Connector */}
      <div className={`w-3 h-0.5 ${isProfileComplete ? 'bg-green-500' : 'bg-gray-200'}`} />

      {/* Step 2 - Service */}
      <div className="flex items-center gap-1">
        <div className={`w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-semibold ${
          isServiceComplete 
            ? 'bg-green-500 text-white' 
            : isProfileComplete 
              ? 'bg-orange-500 text-white' 
              : 'bg-gray-100 text-gray-400'
        }`}>
          {isServiceComplete ? (
            <svg width={8} height={8} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : '2'}
        </div>
        <span className={`text-xs ${
          isProfileComplete && !isServiceComplete 
            ? 'text-orange-600 font-medium' 
            : 'text-gray-400'
        }`}>
          {t('onboarding_step_service', 'Service')}
        </span>
      </div>
    </div>
  );
}
