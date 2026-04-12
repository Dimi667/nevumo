# Translation Keys Export - Provider Dashboard Lead Search & Notes Feature

## New i18n Keys for Provider Dashboard

This document lists all new internationalization keys introduced for the provider dashboard lead search enhancement and provider notes feature.

### Namespace: `provider_dashboard`

| Key | Default English Value | Usage Location |
|-----|----------------------|----------------|
| `label_search` | Search | apps/web/app/[lang]/provider/dashboard/leads/page.tsx (line 286) |
| `placeholder_search_leads` | Search name, email, phone, description or notes... | apps/web/app/[lang]/provider/dashboard/leads/page.tsx (line 298) |
| `label_private_notes` | Private Notes | apps/web/components/dashboard/LeadDetailModal.tsx (line 169) |

## Implementation Notes

- All keys are part of the `provider_dashboard` namespace
- Keys need to be seeded for all 34 supported languages
- Default English values are provided above for reference
- The search placeholder describes the 5 fields that can be searched: client_name, client_email, client_phone, description, provider_notes

## Seeding Requirement

These 3 keys × 34 languages = **102 new rows** need to be added to the `translations` table in the `provider_dashboard` namespace.
