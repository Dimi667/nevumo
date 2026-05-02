-- Check for FAQ translation keys in the translations table
-- Looking for category namespace keys related to FAQ for cleaning

-- 1. Check all FAQ-related keys in category namespace
SELECT lang, key, value 
FROM translations 
WHERE key LIKE 'category.faq%' 
ORDER BY lang, key;

-- 2. Specifically check for cleaning FAQ keys
SELECT lang, key, value 
FROM translations 
WHERE key LIKE 'category.faq_cleaning%' 
ORDER BY lang, key;

-- 3. Check for Bulgarian (bg) FAQ translations
SELECT lang, key, value 
FROM translations 
WHERE lang = 'bg' AND key LIKE 'category.faq%' 
ORDER BY key;

-- 4. Count FAQ keys per language
SELECT lang, COUNT(*) as count
FROM translations 
WHERE key LIKE 'category.faq%'
GROUP BY lang
ORDER BY lang;

-- 5. Check if there are any category namespace keys at all
SELECT lang, key, value 
FROM translations 
WHERE key LIKE 'category.%' 
ORDER BY lang, key
LIMIT 50;
