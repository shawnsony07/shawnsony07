import re

def widen_svg(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Widen SVG width
    content = content.replace('width="985px"', 'width="1100px"')
    
    # Extend separators by 12 characters
    content = content.replace('———————————————————————————————————————————-—-', '———————————————————————————————————————————————————————-—-')
    content = content.replace('——————————————————————————————————————————————-—-', '——————————————————————————————————————————————————————————-—-')
    content = content.replace('—————————————————————————————————————————-—-', '————————————————————————————————————————————————————-—-')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Widened {file_path}")

widen_svg("c:/dev/shawnsony07/light_mode.svg")
widen_svg("c:/dev/shawnsony07/dark_mode.svg")
