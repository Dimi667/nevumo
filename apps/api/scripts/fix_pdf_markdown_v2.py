#!/usr/bin/env python3
"""Convert markdown formatting to ReportLab HTML format in PDF seed scripts using Python eval."""

import re
import shutil
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
    # Split by ** and alternate between <b> and </b>
    parts = text.split('**')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Odd index = content between ** markers
            result.append(f'<b>{part}</b>')
        else:  # Even index = content outside ** markers
            result.append(part)
    return ''.join(result)


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


def process_file_via_exec(filepath: Path, dry_run: bool = False) -> None:
    """Process a seed file by extracting and modifying the dict."""
    print(f"\nProcessing: {filepath.name}")
    
    # Read the file
    content = filepath.read_text(encoding='utf-8')
    
    # Extract the ALL_TRANSLATIONS dict using regex
    # Find the dict definition
    dict_match = re.search(r'ALL_TRANSLATIONS: dict\[str, dict\[str, str\]\] = (\{.*?\n\})', content, re.DOTALL)
    if not dict_match:
        print("  ERROR: Could not find ALL_TRANSLATIONS dict")
        return
    
    dict_str = dict_match.group(1)
    
    # Eval just the dict
    try:
        all_translations = eval(dict_str)
    except Exception as e:
        print(f"  ERROR: Failed to parse dict: {e}")
        return
    
    if not all_translations:
        print("  No translations found")
        return
    
    # Process each translation
    modified = False
    for lang, keys in all_translations.items():
        for key, value in keys.items():
            new_value = value
            new_value = convert_markdown_to_reportlab(new_value)
            new_value = remove_blockquote_markers(new_value, key)
            
            if new_value != value:
                all_translations[lang][key] = new_value
                modified = True
    
    if not modified:
        print("  No changes needed")
        return
    
    # Reconstruct the file with modified dict
    # Find the ALL_TRANSLATIONS assignment and replace it
    lines = content.split('\n')
    new_lines = []
    in_dict = False
    dict_start = -1
    indent_level = 0
    
    for i, line in enumerate(lines):
        if 'ALL_TRANSLATIONS' in line and '=' in line and 'dict' in line:
            in_dict = True
            dict_start = i
            # Find the dict start (after the =)
            match = re.search(r'=\s*{', line)
            if match:
                indent_level = len(line) - len(line.lstrip())
        
        if in_dict:
            new_lines.append(line)
            # Check if dict ends
            if i > dict_start and line.strip() == '}' and not line.strip().startswith('#'):
                in_dict = False
                # Insert the modified dict here
                new_lines.append('')  # Empty line
        else:
            new_lines.append(line)
    
    # This approach is complex, let's use a simpler one:
    # Just replace the dict string representation
    
    # Find and replace the entire ALL_TRANSLATIONS dict
    dict_pattern = r'ALL_TRANSLATIONS: dict\[str, dict\[str, str\]\] = \{.*?\n\}'
    
    # Build the new dict string
    new_dict_str = "ALL_TRANSLATIONS: dict[str, dict[str, str]] = {\n"
    for lang, keys in all_translations.items():
        new_dict_str += f'    "{lang}": {{\n'
        for key, value in keys.items():
            # Escape the value properly for Python string literal
            escaped_value = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            new_dict_str += f'        "{key}": "{escaped_value}",\n'
        new_dict_str += '    },\n'
    new_dict_str += "}\n"
    
    # Replace in content
    match = re.search(r'ALL_TRANSLATIONS: dict\[str, dict\[str, str\]\] = \{', content)
    if match:
        start = match.start()
        # Find the end of the dict (matching closing brace)
        brace_count = 0
        in_string = False
        escape_next = False
        for i in range(start, len(content)):
            char = content[i]
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == '"':
                in_string = not in_string
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
        
        new_content = content[:start] + new_dict_str + content[end:]
        
        # Show diff
        diff = list(difflib.unified_diff(
            content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{filepath.name} (original)",
            tofile=f"{filepath.name} (modified)",
            lineterm=''
        ))
        
        if diff:
            print("  Changes:")
            for line in diff[:30]:
                print(f"  {line}")
            if len(diff) > 30:
                print(f"  ... ({len(diff) - 30} more lines)")
        
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
    else:
        print("  ERROR: Could not find ALL_TRANSLATIONS dict")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert markdown formatting to ReportLab format in PDF seed scripts")
    parser.add_argument('--dry-run', action='store_true', help='Show changes without modifying files')
    args = parser.parse_args()
    
    print("=" * 70)
    print("PDF Markdown to ReportLab Conversion Script v2")
    print("=" * 70)
    
    if args.dry_run:
        print("\nDRY RUN MODE - No files will be modified\n")
    
    for filename in FILES_TO_PROCESS:
        filepath = SCRIPTS_DIR / filename
        if not filepath.exists():
            print(f"WARNING: File not found: {filename}")
            continue
        
        process_file_via_exec(filepath, dry_run=args.dry_run)
    
    print("\n" + "=" * 70)
    if args.dry_run:
        print("Dry run complete. Review changes above.")
        print("Run without --dry-run to apply changes.")
    else:
        print("Conversion complete. Backup files created with .bak extension.")
    print("=" * 70)


if __name__ == "__main__":
    main()
