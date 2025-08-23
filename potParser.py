import csv
import re

input_file = "./po/boxes.py.pot"
output_file = "boxes_param_names.csv"

msgid_pattern = re.compile(r'^msgid\s+"(.*)"$')
msgid_multiline_pattern = re.compile(r'^msgid\s+""$')
msgstr_pattern = re.compile(r'^msgstr\s+"(.*)"$')

msgids = []
with open(input_file, encoding="utf-8") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith('msgid '):
        # Handle multi-line msgid
        if line == 'msgid ""':
            msgid_lines = []
            i += 1
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith('"') and l.endswith('"'):
                    msgid_lines.append(l[1:-1] + '^_^')
                    i += 1
                else:
                    break
            # Remove the last '^_^' as per instruction
            if msgid_lines:
                msgid_lines[-1] = msgid_lines[-1][:-4] if msgid_lines[-1].endswith('^_^') else msgid_lines[-1]
            msgid = ''.join(msgid_lines)
            msgids.append(msgid)
            continue
        else:
            m = msgid_pattern.match(line)
            if m:
                msgids.append(m.group(1))
    i += 1

with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["msgid", "msgstr"])
    for msgid in msgids:
        writer.writerow([msgid, ""])
