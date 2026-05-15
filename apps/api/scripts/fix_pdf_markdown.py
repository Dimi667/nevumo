#!/usr/bin/env python3
"""Convert markdown formatting to ReportLab HTML format in PDF seed scripts."""

import re
import shutil
import ast
from pathlib import Path
import difflib

# Files to process
FILES_TO_PROCESS = [
    "seed_pdf_group1_important_notice.py",
    "seed_pdf_group3_how_to_withdrawal.py",
    "seed_pdf_group14_how_to_submit.py",
    "seed_pdf_group15_form_template.py",
]

SCRIPTS_DIR = Path(__file__).parent


def convert_markdown_to_reportlab(text: str) -> str:
    """Convert markdown bold syntax to ReportLab HTML bold tags."""
    # Simple regex replacement that handles escaped characters
    # Replace **text** with <b>text</b>
    # Use a loop to replace all occurrences
    result = text
    iteration = 0
    max_iterations = 50
    while iteration < max_iterations:
        new_result = re.sub(r'\*\*([^*]+?)\*\*', r'<b>\1</b>', result)
        if new_result == result:
            break
        result = new_result
        iteration += 1
    return result


def remove_blockquote_markers(text: str, key: str) -> str:
    """Remove markdown blockquote markers (>) from the beginning of lines.
    
    Only applies to pdf.company_address_block key.
    """
    if key == "pdf.company_address_block":
        # Remove "> " or ">" from the beginning of each line
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove leading "> " or ">"
            line = re.sub(r'^>\s*', '', line)
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    return text


def process_file(filepath: Path, dry_run: bool = False) -> None:
    """Process a single seed file to convert markdown to ReportLab format."""
    print(f"\nProcessing: {filepath.name}")
    
    content = filepath.read_text(encoding='utf-8')
    original_content = content
    
    # Find and process translation values
    # Pattern to match dictionary values in Python
    # This regex matches quoted strings after colons in the translation dict
    lines = content.split('\n')
    modified_lines = []
    
    for line in lines:
        modified_line = line
        # Check if this line contains a translation value
        # Pattern: "key": "value"
        match = re.search(r'"(pdf\.[^"]+)":\s*"([^"]*(?:\\.[^"]*)*)"', line)
        if match:
            key = match.group(1)
            value = match.group(2)
            
            # Process the value
            new_value = value
            new_value = convert_markdown_to_reportlab(new_value)
            new_value = remove_blockquote_markers(new_value, key)
            
            # If value changed, replace it in the line
            if new_value != value:
                modified_line = line.replace(f'"{value}"', f'"{new_value}"')
        
        modified_lines.append(modified_line)
    
    new_content = '\n'.join(modified_lines)
    
    if new_content == original_content:
        print("  No changes needed")
        return
    
    # Show diff
    diff = list(difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"{filepath.name} (original)",
        tofile=f"{filepath.name} (modified)",
        lineterm=''
    ))
    
    if diff:
        print("  Changes:")
        for line in diff[:50]:  # Show first 50 lines of diff
            print(f"  {line}")
        if len(diff) > 50:
            print(f"  ... ({len(diff) - 50} more lines)")
    
    if dry_run:
        print("  [DRY RUN] No changes made")
    else:
        # Create backup
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        shutil.copy2(filepath, backup_path)
        print(f"  Backup created: {backup_path.name}")
        
        # Write modified content
        filepath.write_text(new_content, encoding='utf-8')
        print("  File updated")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert markdown formatting to ReportLab format in PDF seed scripts")
    parser.add_argument('--dry-run', action='store_true', help='Show changes without modifying files')
    args = parser.parse_args()
    
    print("=" * 70)
    print("PDF Markdown to ReportLab Conversion Script")
    print("=" * 70)
    
    if args.dry_run:
        print("\nDRY RUN MODE - No files will be modified\n")
    
    for filename in FILES_TO_PROCESS:
        filepath = SCRIPTS_DIR / filename
        if not filepath.exists():
            print(f"WARNING: File not found: {filename}")
            continue
        
        process_file(filepath, dry_run=args.dry_run)
    
    print("\n" + "=" * 70)
    if args.dry_run:
        print("Dry run complete. Review changes above.")
        print("Run without --dry-run to apply changes.")
    else:
        print("Conversion complete. Backup files created with .bak extension.")
    print("=" * 70)


if __name__ == "__main__":
    main()
