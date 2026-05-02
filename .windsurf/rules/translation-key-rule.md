# Translation Key & Price Handling Rule
1. **Seeding Requirement**: When adding or modifying translation keys in any frontend component, you MUST update the corresponding seed script in `apps/api/scripts/` with the new key for all 34 languages. Never add a `t()` call with a new key without a matching seed script update.
2. **Price Fallback Standard**: In FAQ or marketing sections, if price data is missing (`null priceData`), the entire price-related phrase (e.g., "Prices from... to...") must be replaced with the "Price on request" translation.
3. **Currency Cleanup**: When a price is missing, the `{currency}` placeholder must be removed completely from the resulting text to avoid showing raw tags or dangling symbols.
4. **Bulgaria 2026**: Always assume EUR for Bulgaria (BG) from 01.01.2026 in all currency-related logic.
