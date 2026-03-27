#!/usr/bin/env python3
import json
import shutil
import os

# Read restore plan
with open('.windsurf/restore_plan.json', 'r') as f:
    plan = json.load(f)

print("=" * 70)
print("RESTORING FILES TO 13:28 STATE")
print("=" * 70)

restored = []
for item in plan:
    src = item['entry_file']
    dst = item['target_file']
    
    if os.path.exists(src):
        # Backup current file just in case
        backup = dst + '.bak'
        if os.path.exists(dst):
            shutil.copy2(dst, backup)
        
        # Copy historical version
        shutil.copy2(src, dst)
        restored.append(item)
        print(f"✓ {item['rel_file']}")
        print(f"  <- {item['entry_id']} ({item['mins_before']} min before 13:28)")
    else:
        print(f"✗ {item['rel_file']} -> source not found: {src}")

print(f"\n{'='*70}")
print(f"RESTORED: {len(restored)} files")
print("=" * 70)

# Save report
report = {
    'timestamp': 'Mar 27, 2026 13:28:00 UTC+02:00',
    'total_restored': len(restored),
    'files': restored
}
with open('.windsurf/RESTORE_REPORT.json', 'w') as f:
    json.dump(report, f, indent=2)

print("\nReport saved to .windsurf/RESTORE_REPORT.json")
