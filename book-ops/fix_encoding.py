# Script to fix ALL encoding issues in taiwan_library.py
# Read the file
with open('sites/taiwan_library.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

content = ''.join(lines)
lines = content.split('\n')

# Let's just do direct line replacements for each problematic area

output = []
for i, line in enumerate(lines):
    # Fix line 326 - _guess_title_from_text split pattern (0-indexed = 325)
    if i == 325 and 're.split' in line:
        output.append('    chunks = [c.strip() for c in re.split(r"[|｜\\n]", text) if c.strip()]')
    # Replace _guess_author function entirely 
    elif i == 330 and 'def _guess_author(text):' in line:
        output.append('def _guess_author(text):')
        output.append('    if not text:')
        output.append('        return ""')
        output.append('    patterns = [')
        output.append('        r"作者[:：]\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",')
        output.append('        r"Author[:：]?\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",')
        output.append('    ]')
    elif i == 337:
        output.append('    for pattern in patterns:')
    elif i == 338:
        output.append('        m = re.search(pattern, text, re.IGNORECASE)')
    elif i == 339:
        output.append('        if m:')
    elif i == 340:
        output.append('            return _clean_text(m.group(1))')
    elif i == 341:
        output.append('    return ""')
    # blocked_terms lines (368-372)
    elif i == 368:
        output.append('    blocked_terms = [')
    elif i == 369:
        output.append('        "首頁", "home", "登入", "login", "註冊", "register",')
    elif i == 370:
        output.append('        "facebook", "instagram", "copyright", "聯絡", "privacy",')
    elif i == 371:
        output.append('        "條款", "terms", "menu", "導航", "search",')
    elif i == 372:
        output.append('    ]')
    else:
        output.append(line)

# Write back
with open('sites/taiwan_library.py', 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(output))

print("All encoding fixes applied!")