# ProviderWidget JSON-LD Integrity Rule

## CRITICAL: JSON-LD Structure Preservation

When modifying the ProviderWidget component (`apps/web/components/provider/ProviderWidget.tsx`), you MUST preserve the integrity of the JSON-LD structured data.

## Required Schemas

The ProviderWidget MUST include both:
1. **LocalBusiness Schema** - Represents the provider as a local business entity
2. **Service Schema** - Represents individual services offered by the provider

## Required Fields

### LocalBusiness Schema
- `@type`: LocalBusiness
- `name`: Provider business name
- `description`: Provider description
- `address`: Address object with `addressLocality` (localized city name)
- `telephone`: Provider phone number
- `url`: Absolute provider profile URL
- `areaServed`: City and country information
- `priceRange`: Dynamic price range based on services

### Service Schema
- `@type`: Service
- `name`: Service title
- `description`: Service description
- `provider`: Link to LocalBusiness schema
- `areaServed`: City and country information
- `priceCurrency`: Currency code (determined by fallback chain)
- `price`: Service price

## Currency Handling

Currency MUST be determined using the fallback chain:
1. Service currency (`service.currency`)
2. City country code (`city.country_code`)
3. Country default (RSD for RS, PLN for PL, etc.)
4. EUR as final fallback

Special rule: Bulgaria (BG) always uses EUR (effective 01.01.2026).

## Validation

After any modification to ProviderWidget:
1. Verify JSON-LD structure is still valid using Google's Rich Results Test
2. Ensure all required fields are present
3. Confirm currency fallback logic is intact
4. Test that schema data renders correctly in the HTML head

## Consequences

Breaking JSON-LD structure will:
- Reduce SEO visibility
- Lose rich snippet display in Google search results
- Disable Google Maps integration
- Fail structured data validation

## Implementation Location

- Component: `apps/web/components/provider/ProviderWidget.tsx`
- Currency utility: `apps/web/lib/currency.ts`
