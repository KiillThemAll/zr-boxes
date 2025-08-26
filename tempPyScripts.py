import csv
import re

def replace_underscore_in_cyrillic_inplace(csv_path):
    """
    Iterates through a CSV file with columns 'msgid' and 'msgstr'.
    For each msgstr that matches the regex '^[\u0400-\u04FF]+(?:_[\u0400-\u04FF]+)+$',
    replaces '_' with ' ' and overwrites the original CSV file in place.
    Preserves any surrounding double quotes in msgstr.
    """
    pattern = re.compile(r'^[\u0400-\u04FF]+(?:_[\u0400-\u04FF]+)+$')
    rows = []
    with open(csv_path, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                rows.append(row)
                continue
            msgid, msgstr = row[0], row[1]
            # Check for surrounding double quotes and preserve them
            has_quotes = msgstr.startswith('"') and msgstr.endswith('"') and len(msgstr) >= 2
            core_msgstr = msgstr[1:-1] if has_quotes else msgstr
            if pattern.match(core_msgstr):
                core_msgstr = core_msgstr.replace('_', ' ')
            # Re-add quotes if they were present
            new_msgstr = f'"{core_msgstr}"' if has_quotes else core_msgstr
            rows.append([msgid, new_msgstr])

    # Always overwrite the original file
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Replace underscores with spaces in Cyrillic msgstr fields in a CSV file (in place).")
    parser.add_argument("csv_path", help="Path to the input CSV file (will be modified in place)")
    args = parser.parse_args()

    replace_underscore_in_cyrillic_inplace(args.csv_path)

if __name__ == "__main__":
    main()