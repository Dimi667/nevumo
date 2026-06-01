-- Delete hardcoded city name translation keys from all 34 languages
-- This allows the code fallback to generate dynamic text with {city} placeholder
-- Expected deletion: 238 rows (7 keys × 34 languages)

DELETE FROM translations WHERE key IN (
  'category.h1_cleaning',
  'category.h1_plumbing',
  'category.h1_massage',
  'category.subtitle_cleaning',
  'category.subtitle_plumbing',
  'category.subtitle_massage',
  'category.provider_cta_suffix'
);
