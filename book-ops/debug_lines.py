# Print lines for debugging
with open('sites/taiwan_library.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Print lines around 330-345 to see current state
for i in range(328, min(345, len(lines))):
    print(f"Line {i+1}: {lines[i][:80]}")