# Find and replace the garbled content by searching for the specific bytes
with open('sites/taiwan_library.py', 'rb') as f:
    content = f.read()

# The garbled patterns we need to replace - look for the bytes containing those characters
# Looking at earlier output - line 334 had bytes like: \x... let's find lines with high bytes

# Let's find the line starting with "    patterns = ["
search_patterns = b'patterns = ['
idx = content.find(search_patterns)
if idx > 0:
    # Find the next few lines
    snippet = content[idx:idx+500]
    print("Found patterns = [ at:", idx)
    print("Snippet:", repr(snippet[:300]))
    
# Let's also search for the garbled "雿" character in UTF-8 which is \xE9\x9B\xBF
garbled = b'\xe9\x9b\xbf'
idx = content.find(garbled)
if idx > 0:
    print("\nFound garbled char at:", idx)
    
# Now let's do replacements by finding those bytes and replacing

# Replace the entire _guess_author section using bytes
# Find the function start
import re

# Let's rebuild the file with just the lines we need

with open('sites/taiwan_library.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
skip_until = None

for i, line in enumerate(lines):
    if skip_until and i < skip_until:
        continue
    elif skip_until and i >= skip_until:
        skip_until = None
        
    # If we see the garbled patterns, we need to replace lines 333-337 (0-index 332-336)
    if i == 332 and 'patterns = [' in line:
        # Replace lines 332-336
        output.append('    patterns = [\n')
        output.append('        r"作者[:：]\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",\n')
        output.append('        r"Author[:：]?\\s*([^\\s|｜\\n]+(?:\\s*[^\\s|｜\\n]+){0,4})",\n')
        output.append('    ]\n')
        skip_until = 337
        continue
        
    output.append(line)

# Write back
with open('sites/taiwan_library.py', 'w', encoding='utf-8', newline='') as f:
    f.write(''.join(output))

print("Done!")