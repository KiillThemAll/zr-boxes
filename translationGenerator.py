import csv
import re

def load_csv_translations(csv_path, multiline=False):
    translations = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            msgid = row[0]
            msgstr = row[1]
            if multiline:
                translations[msgid] = msgstr
            else:
                translations[msgid] = msgstr
    return translations

def find_multiline_match(po_msgid, multiline_dict):
    for csv_msgid, csv_msgstr in multiline_dict.items():
        candidate = csv_msgid.replace('^_^', '')
        if candidate.strip() == po_msgid.strip():
            return csv_msgstr
    return None

def update_po_file_inplace(po_path, single_dict, multiline_dict):

    with open(po_path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # need add ignor for '#, fuzzy'

        # Only alter msgstr lines, leave everything else untouched
        if line.startswith('msgid '):
            # Check for '#. parameter name' in the comment line above
            is_parameter_name = False
            if i > 2:
                prev_line = lines[i-1]
                if prev_line.startswith('#: '):
                    prev_line = lines[i-2]
                if prev_line.startswith('#. parameter name'):
                    is_parameter_name = True

            msgid_match = re.match(r'msgid\s+"(.*)"', line)
            if msgid_match:
                msgid_val = msgid_match.group(1)
                if msgid_val == '':
                    # Multiline msgid
                    msgid_val = ''
                    msgid_block_lines = []
                    msgid_block_lines.append(line)  # msgid ""\n
                    i += 1
                    msgid_lines = []
                    # Collect all msgid quoted lines (as in original)
                    while i < len(lines):
                        l = lines[i]
                        if l.startswith('"') and l.rstrip().endswith('"'):
                            msgid_block_lines.append(l)
                            msgid_lines.append(l.strip()[1:-1])
                            i += 1
                        else:
                            break
                    msgid_val = ''.join(msgid_lines)
                    translation = find_multiline_match(msgid_val, multiline_dict)
                    # Write msgid block as in original, unmodified
                    for l in msgid_block_lines:
                        new_lines.append(l)
                    # Now, alter only msgstr part
                    if i < len(lines) and lines[i].startswith('msgstr'):
                        # Write msgstr header
                        if is_parameter_name:
                            new_lines.append('msgstr ""\n')
                            i += 1
                            # Skip all following quoted lines (original msgstr)
                            while i < len(lines) and lines[i].startswith('"'):
                                i += 1
                            # Write the msgid value as msgstr, split by ^_^ if multiline
                            msgid_parts = msgid_val.split('^_^')
                            for t in msgid_parts:
                                new_lines.append(f'"{t}"\n')
                        else:
                            new_lines.append('msgstr ""\n')
                            i += 1
                            # Skip all following quoted lines (original msgstr)
                            while i < len(lines) and lines[i].startswith('"'):
                                i += 1
                            if translation is not None:
                                translation_lines = translation.split('^_^')
                                for t in translation_lines:
                                    new_lines.append(f'"{t}"\n')
                        # else: leave msgstr "" (already written)
                    else:
                        # If no msgstr found, just add empty msgstr
                        if is_parameter_name:
                            new_lines.append('msgstr ""\n')
                            # Write the msgid value as msgstr, split by ^_^ if multiline
                            msgid_parts = msgid_val.split('^_^')
                            for t in msgid_parts:
                                new_lines.append(f'"{t}"\n')
                        else:
                            new_lines.append('msgstr ""\n')
                    continue
                else:
                    # Single line msgid
                    translation = single_dict.get(msgid_val)
                    if translation is None:
                        translation = find_multiline_match(msgid_val, multiline_dict)
                    new_lines.append(line)
                    i += 1
                    # Only alter msgstr part
                    if i < len(lines) and lines[i].startswith('msgstr'):
                        if is_parameter_name:
                            new_lines.append(f'msgstr "{msgid_val}"\n')
                            i += 1
                            # Skip any original quoted msgstr lines
                            while i < len(lines) and lines[i].startswith('"'):
                                i += 1
                        elif translation is not None:
                            if '^_^' in translation:
                                translation_lines = translation.split('^_^')
                                new_lines.append('msgstr ""\n')
                                for t in translation_lines:
                                    new_lines.append(f'"{t}"\n')
                            else:
                                new_lines.append(f'msgstr "{translation}"\n')
                            i += 1
                            # Skip any original quoted msgstr lines
                            while i < len(lines) and lines[i].startswith('"'):
                                i += 1
                        else:
                            # No translation, leave msgstr as empty
                            new_lines.append('msgstr ""\n')
                            i += 1
                            while i < len(lines) and lines[i].startswith('"'):
                                i += 1
                    continue
        # For all other lines (not msgid/msgstr), just copy
        new_lines.append(line)
        i += 1

    with open(po_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    single_csv = 'boxes_translated-mix.csv'
    multiline_csv = 'boxes_multiline_translated.csv'
    po_file = 'po/ru.po'

    single_dict = load_csv_translations(single_csv, multiline=False)
    multiline_dict = load_csv_translations(multiline_csv, multiline=True)

    update_po_file_inplace(po_file, single_dict, multiline_dict)