-- SQL Script to standardize i18n keys with namespace prefixes
-- This script renames keys without namespace to have proper namespace prefixes

-- Provider Dashboard Keys
UPDATE translations SET key = 'provider_dashboard.' || key 
WHERE key IN (
    'aria_close_menu',
    'aria_open_menu',
    'aria_remove_item',
    'aria_select_period_filter',
    'aria_close',
    'availability_active',
    'availability_busy',
    'availability_offline',
    'btn_log_out',
    'btn_edit',
    'btn_delete',
    'btn_view',
    'btn_contact',
    'btn_reject',
    'btn_save_notes',
    'btn_close',
    'btn_cancel',
    'btn_save_changes',
    'btn_send_reply',
    'btn_reply_to_review',
    'btn_delete_service',
    'btn_new_service',
    'btn_edit_service',
    'btn_create_service',
    'btn_add_service',
    'btn_view_analytics',
    'btn_view_all',
    'btn_reply_now',
    'btn_generate_qr_code',
    'btn_download',
    'btn_regenerate',
    'btn_change_photo',
    'btn_upload_photo',
    'btn_try_again',
    'label_source_seo',
    'label_source_widget',
    'label_source_qr',
    'label_source_direct',
    'label_source_other',
    'label_last_x_days',
    'label_lead_sources',
    'label_account',
    'label_email',
    'label_role',
    'label_phone',
    'label_availability',
    'label_public_url',
    'label_your_profile_link',
    'label_edit_public_slug',
    'label_suggestions',
    'label_url_locked',
    'label_account_role',
    'label_session',
    'label_all_reviews',
    'label_unreplied',
    'label_needs_reply',
    'label_your_reply',
    'label_edited',
    'label_last_30_days',
    'label_top_sources',
    'label_latest_review',
    'label_title',
    'label_description',
    'label_optional',
    'label_category',
    'label_cities',
    'label_price_type',
    'label_price_in_currency',
    'msg_saving',
    'msg_sending',
    'msg_deleting',
    'msg_generating',
    'msg_uploading'
);

-- Homepage Keys (already have namespace, but verify)
-- These should already be correct in the database

-- PWA Keys
UPDATE translations SET key = 'pwa.' || key 
WHERE key IN (
    'Got it',
    'Install Nevumo',
    'See new requests instantly',
    'Tap Share in the bottom toolbar',
    'Track requests without opening a browser'
);

-- Generic Label Keys (used in multiple contexts, add generic namespace)
UPDATE translations SET key = 'common.' || key 
WHERE key IN (
    'label_client_message',
    'label_date',
    'label_notes_privacy_disclaimer',
    'label_source',
    'label_status',
    'lead_detail_title',
    'placeholder_private_notes',
    'placeholder_type_to_search',
    'price_type_fixed',
    'price_type_hourly',
    'price_type_per_sqm',
    'price_type_request',
    'logo_pro',
    'msg_failed_switch_role',
    'msg_no_description',
    'msg_no_results',
    'msg_notes_save_failed',
    'msg_notes_saved',
    'msg_switching',
    'nav_analytics',
    'nav_dashboard',
    'nav_leads',
    'nav_profile',
    'nav_qr_code',
    'nav_reviews',
    'nav_services',
    'nav_settings'
);

-- Delete any keys that don't have a namespace prefix (cleanup)
-- This is a safety measure - only run after verifying the above updates worked
-- DELETE FROM translations WHERE key NOT LIKE '%.%';

-- Verification query
-- Run this after the updates to verify
-- SELECT key, COUNT(*) as count FROM translations GROUP BY key HAVING COUNT(*) > 1;
