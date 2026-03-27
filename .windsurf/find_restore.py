#!/usr/bin/env python3
"""Find and restore files from Windsurf history to 13:28 state"""
import json
import os
import glob
import shutil

target_time = 1774610880000  # Mar 27, 2026 13:28:00 local time

# The 35 modified files from git status
modified_files = [
    "apps/api/exceptions.py",
    "apps/api/main.py",
    "apps/api/models.py",
    "apps/api/routes/auth.py",
    "apps/api/routes/categories.py",
    "apps/api/routes/cities.py",
    "apps/api/routes/provider.py",
    "apps/api/routes/providers.py",
    "apps/api/schemas.py",
    "apps/api/services/provider_service.py",
    "apps/web/app/[lang]/[city]/[category]/[providerPage]/page.tsx",
    "apps/web/app/[lang]/auth/LoginClient.tsx",
    "apps/web/app/[lang]/provider/dashboard/layout.tsx",
    "apps/web/app/[lang]/provider/dashboard/page.tsx",
    "apps/web/app/[lang]/provider/dashboard/profile/page.tsx",
    "apps/web/app/[lang]/provider/dashboard/qr-code/page.tsx",
    "apps/web/app/[lang]/provider/dashboard/services/page.tsx",
    "apps/web/app/[lang]/provider/dashboard/settings/page.tsx",
    "apps/web/components/dashboard/SearchableSelect.tsx",
    "apps/web/lib/api.ts",
    "apps/web/lib/auth-api.ts",
    "apps/web/lib/locales.ts",
    "apps/web/lib/provider-api.ts",
    "apps/web/package.json",
    "apps/web/types/provider.ts",
    "docs/api_contracts.md",
    "docs/architecture.md",
    "docs/db_schema.md",
    "docs/models.py",
    "docs/nevumo_master_context.md",
    ".env.example",
]

history_base = "/Users/dimitardimitrov/Library/Application Support/Windsurf/User/History"
project_base = "/Users/dimitardimitrov/nevumo"

# Build map of history directories to files
hist_map = {}
for hist_dir in glob.glob(os.path.join(history_base, "*/")):
    entries_file = os.path.join(hist_dir, "entries.json")
    if os.path.exists(entries_file):
        try:
            with open(entries_file, 'r') as f:
                data = json.load(f)
            resource = data.get('resource', '').replace('file://', '').replace('%5B', '[').replace('%5D', ']')
            if '/nevumo/' in resource:
                rel_path = resource.split('/nevumo/')[-1]
                hist_map[rel_path] = (hist_dir, data)
        except:
            pass

print("=" * 70)
print("FILES TO RESTORE TO 13:28 STATE")
print("=" * 70)

restore_plan = []
for rel_file in modified_files:
    if rel_file in hist_map:
        hist_dir, data = hist_map[rel_file]
        # Find best version (closest before 13:28)
        best_entry = None
        best_diff = float('inf')
        for entry in data.get('entries', []):
            ts = entry.get('timestamp', 0)
            if ts <= target_time:
                diff = target_time - ts
                if diff < best_diff:
                    best_diff = diff
                    best_entry = entry
        
        if best_entry:
            mins_before = round((target_time - best_entry['timestamp']) / 60000, 1)
            entry_file = os.path.join(hist_dir, best_entry['id'])
            target_file = os.path.join(project_base, rel_file)
            if os.path.exists(entry_file):
                restore_plan.append({
                    'rel_file': rel_file,
                    'entry_file': entry_file,
                    'target_file': target_file,
                    'entry_id': best_entry['id'],
                    'mins_before': mins_before,
                    'timestamp': best_entry['timestamp']
                })
                print(f"✓ {rel_file}")
                print(f"  -> {best_entry['id']} ({mins_before} min before 13:28)")
            else:
                print(f"✗ {rel_file} -> entry file not found: {best_entry['id']}")
        else:
            print(f"✗ {rel_file} -> no version before 13:28")
    else:
        print(f"✗ {rel_file} -> no history found")

print(f"\n{'='*70}")
print(f"TOTAL: {len(restore_plan)} files can be restored")
print("=" * 70)

# Save restore plan
with open('/Users/dimitardimitrov/nevumo/.windsurf/restore_plan.json', 'w') as f:
    json.dump(restore_plan, f, indent=2)

print("\nRestore plan saved to .windsurf/restore_plan.json")
