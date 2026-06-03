import re

def align_svg(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []
    # Find the maximum key length to align to
    # Actually, we know the max key length is "Languages.Programming:" which is 22.
    # Let's align all values at column 24.
    ALIGN_COL = 24

    for line in lines:
        if '<tspan x="390"' in line and '<tspan class="key">' in line and '<tspan class="value"' in line:
            # Parse the line
            # Pattern to extract:
            # 1. Prefix before key
            # 2. Key part (can contain multiple tspans)
            # 3. Dots part
            # 4. Value part
            
            # Using a simpler approach: split by '<tspan class="cc"' for the dots.
            # But there are multiple class="cc". 
            # The dots always come right before the value.
            
            # Let's use regex to find the dots span.
            # It usually looks like: <tspan class="cc" id="..."> ... </tspan> or <tspan class="cc"> ... </tspan>
            # right before <tspan class="value" or <a href...
            
            # Find the text of the key part (strip tags) to calculate its length
            key_part_match = re.search(r'(</tspan>)(<tspan class="key">.*?)(<tspan class="cc")', line)
            if key_part_match:
                key_html = key_part_match.group(2)
                # calculate raw text length of key
                raw_key = re.sub(r'<[^>]+>', '', key_html)
                key_len = len(raw_key)
                
                # We need dots length to be ALIGN_COL - key_len
                dots_needed = ALIGN_COL - key_len
                if dots_needed < 2:
                    dots_needed = 2 # at least space dot space
                
                # Create new dots string
                new_dots = " " + "." * (dots_needed - 2) + " "
                
                # Replace the old dots string inside the dots span
                # The dots span is right after key_html
                # Let's replace the content of the specific <tspan class="cc" ...> ... </tspan>
                # It's the one containing only spaces and dots.
                line = re.sub(r'(<tspan class="cc"[^>]*>)[ \.]+(</tspan>)', r'\1' + new_dots + r'\2', line, count=1)
                
        out_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print(f"Processed {file_path}")

align_svg("c:/dev/shawnsony07/light_mode.svg")
align_svg("c:/dev/shawnsony07/dark_mode.svg")
