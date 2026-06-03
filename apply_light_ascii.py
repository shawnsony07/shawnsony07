import re

def xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

with open('light_ascii.txt', 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]

tspans = []
y = 30
for line in lines:
    escaped_line = xml_escape(line)
    tspans.append(f'<tspan x="15" y="{y}">{escaped_line}</tspan>')
    y += 7.5

tspan_str = '\n'.join(tspans)

with open('light_mode.svg', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(<text x="15" y="30"[^>]*class="ascii"[^>]*>\s*\n)(.*?)(</text>)'

def repl(m):
    open_tag = m.group(1)
    if 'font-size="6px"' not in open_tag:
        open_tag = open_tag.replace('class="ascii"', 'font-size="6px" class="ascii"')
    return open_tag + tspan_str + '\n' + m.group(3)

new_content = re.sub(pattern, repl, content, flags=re.DOTALL)

with open('light_mode.svg', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated light_mode.svg")
