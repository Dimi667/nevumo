-- SQL Script for Safe Delete of duplicate translation keys
-- This script deletes keys without namespace ONLY if an equivalent with namespace already exists

-- Delete provider_dashboard duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'provider_dashboard.' || t1.key
    AND t2.lang = t1.lang
);

-- Delete pwa duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'pwa.' || t1.key
    AND t2.lang = t1.lang
);

-- Delete common duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'common.' || t1.key
    AND t2.lang = t1.lang
);

-- Delete homepage duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'homepage.' || t1.key
    AND t2.lang = t1.lang
);

-- Delete client_dashboard duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'client_dashboard.' || t1.key
    AND t2.lang = t1.lang
);

-- Delete auth duplicates
DELETE FROM translations t1
WHERE t1.key NOT LIKE '%.%'
AND EXISTS (
    SELECT 1 FROM translations t2
    WHERE t2.key = 'auth.' || t1.key
    AND t2.lang = t1.lang
);
