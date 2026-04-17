# Fix the _guess_author function properly

with open('sites/taiwan_library.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole _guess_author function
old_func = '''def _guess_author(text):
    if not text:
        return ""
    patterns = [
        r"雿?:嚗?\\s*([^\\s|嚚+?(?:\\s*[^\\s|嚚+){0,4})",
        r"Author[:嚗?\\s*([^\\s|嚚+?(?:\\s*[^\\s|嚚+){0,4})",
    ]
    for pattern in patterns:
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return _clean_text(m.group(1))
    return ""'''

new_func = '''def _guess_author(text):
    if not text:
        return ""
    patterns = [
        r"作者[:：]\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",
        r"Author[:：]?\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return _clean_text(m.group(1))
    return ""'''

if old_func in content:
    content = content.replace(old_func, new_func)
    print("Fixed _guess_author!")
else:
    print("Old function not found - trying different pattern")

# Write back
with open('sites/taiwan_library.py', 'w', encoding='utf-8') as f:
    f.write(content)