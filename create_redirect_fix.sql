-- Create redirect record for et-111proba -> et-111proba-new
INSERT INTO url_redirects (provider_id, old_slug, new_slug, active, created_at)
SELECT p.id, 'et-111proba', 'et-111proba-new', true, NOW()
FROM providers p 
WHERE p.slug = 'et-111proba-new'
AND NOT EXISTS (
    SELECT 1 FROM url_redirects ur 
    WHERE ur.provider_id = p.id AND ur.old_slug = 'et-111proba'
);
