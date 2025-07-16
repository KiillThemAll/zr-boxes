import csv

def escape_po_string(s):
    """
    Escape a string for .po format:
    - Backslashes as \\
    - Double quotes as \"
    - Newlines as \n (but only as actual newlines in .po, not as literal \n)
    """
    # .po files use real newlines, not \n, so don't replace \n with \\n
    # Only escape backslashes and double quotes
    return s.replace('\\', '\\\\').replace('"', '\\"')

def main():
    po_path = 'po/ru.po'
    csv_path = 'boxes_translated-mix.csv'

    # Read translations from CSV into a dict: msgid -> msgstr
    translations = {}
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        lol = 10
        for row in reader:
            msgid = row['msgid'].strip()
            msgstr = row['msgstr'].strip()
            if msgid:
                translations[msgid] = msgstr
            else print(msgid)

    # Read the .po file lines
    with open(po_path, encoding='utf-8') as f:
        lines = f.readlines()

    # Only update msgstr sections, do not touch msgid sections
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid '):
            # Copy msgid and any multiline msgid lines as is
            msgid_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith('"') and not lines[j].startswith('msgstr'):
                msgid_lines.append(lines[j])
                j += 1
            new_lines.extend(msgid_lines)
            # Now at msgstr line (or not)
            if j < len(lines) and lines[j].startswith('msgstr'):
                # Reconstruct full msgid for lookup
                msgid_full = ""
                for l in msgid_lines:
                    if l.startswith('msgid '):
                        part = l[len('msgid '):].strip()
                        if part.startswith('"') and part.endswith('"'):
                            part = part[1:-1]
                        msgid_full += part
                    elif l.startswith('"') and l.rstrip().endswith('"'):
                        msgid_full += l.strip()[1:-1]
                # If translation exists, replace msgstr, else keep as is
                if msgid_full in translations:
                    new_msgstr = translations[msgid_full]
                    # Write msgstr in the same multiline style as msgid if msgid was multiline or translation contains newlines
                    if len(msgid_lines) > 1 or '\n' in new_msgstr:
                        new_lines.append('msgstr ""\n')
                        # If multiline msgid, try to match line lengths
                        if len(msgid_lines) > 1:
                            msgid_line_lengths = []
                            for l in msgid_lines:
                                if l.startswith('msgid '):
                                    part = l[len('msgid '):].strip()
                                    if part.startswith('"') and part.endswith('"'):
                                        part = part[1:-1]
                                    msgid_line_lengths.append(len(part))
                                elif l.startswith('"') and l.rstrip().endswith('"'):
                                    msgid_line_lengths.append(len(l.strip()[1:-1]))
                            idx = 0
                            for length in msgid_line_lengths:
                                part = new_msgstr[idx:idx+length]
                                new_lines.append(f'"{escape_po_string(part)}"\n')
                                idx += length
                            if idx < len(new_msgstr):
                                # Add any remaining part
                                new_lines.append(f'"{escape_po_string(new_msgstr[idx:])}"\n')
                        else:
                            # Fallback: split by newlines in translation
                            for l in new_msgstr.split('\n'):
                                new_lines.append(f'"{escape_po_string(l)}"\n')
                    else:
                        new_lines.append(f'msgstr "{escape_po_string(new_msgstr)}"\n')
                else:
                    new_lines.append(lines[j])
                i = j + 1
                continue
        else:
            new_lines.append(line)
        i += 1

    # Write back to the .po file (or to a new file)
    with open(po_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    main()