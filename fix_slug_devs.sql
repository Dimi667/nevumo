-- Fix provider slug from 'devs-1' to 'devs'
-- Run this SQL script against your PostgreSQL database

-- First, check if the provider with slug 'devs-1' exists
SELECT id, business_name, slug FROM providers WHERE slug = 'devs-1';

-- If the above query returns a row, run this UPDATE:
UPDATE providers SET slug = 'devs' WHERE slug = 'devs-1';

-- Verify the change
SELECT id, business_name, slug FROM providers WHERE slug = 'devs';

-- Also check for other providers with numeric suffixes that might need review
SELECT id, business_name, slug FROM providers WHERE slug ~ '-[0-9]+$';
