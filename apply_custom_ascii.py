import re

def xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

with open('ascii.txt', 'r', encoding='utf-8') as f:
    lines = [line.rstrip('\n') for line in f]

tspans = []
y = 30
for line in lines:
    escaped = xml_escape(line)
    # Using 7.5 increment for y
    tspans.append(f'<tspan x="15" y="{y}">{escaped}</tspan>')
    y += 7.5

tspan_str = '\n'.join(tspans)

for svg_file in ['dark_mode.svg', 'light_mode.svg']:
    with open(svg_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ASCII text block
    # It might already have font-size if we ran it before, so match optionally
    pattern = r'(<text x="15" y="30"[^>]*class="ascii"[^>]*>\s*\n)(.*?)(</text>)'
    
    # We also want to inject font-size="6px" into the <text> tag if it doesn't exist
    def repl(m):
        open_tag = m.group(1)
        if 'font-size="6px"' not in open_tag:
            # Insert font-size just before class="ascii"
            open_tag = open_tag.replace('class="ascii"', 'font-size="6px" class="ascii"')
        return open_tag + tspan_str + '\n' + m.group(3)

    new_content = re.sub(pattern, repl, content, count=1, flags=re.DOTALL)

    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {svg_file}")
